#!/usr/bin/env python
"""
Native Arrow Integration Test Script

This script properly integrates with the native Rust implementation of Arrow
support in fast-inverted-index. This demonstrates the ideal way to use Arrow
with the library once the PyIndex class methods are properly exposed.

NOTE: This script will not work until the changes in src/python/mod_integration.rs
are integrated into the main codebase.
"""

import pyarrow as pa
import numpy as np
import time
import sys
import argparse
from typing import Dict, List, Any, Optional, Tuple

import fast_inverted_index as fii
from fast_inverted_index import Index

# Check if the Arrow functions are available
try:
    # Direct access through _fast_inverted_index
    add_documents_from_pyarrow = getattr(fii._fast_inverted_index, 'add_documents_from_pyarrow', None)
    add_documents_from_pyarrow_parallel = getattr(fii._fast_inverted_index, 'add_documents_from_pyarrow_parallel', None)

    ARROW_FUNCTIONS_AVAILABLE = add_documents_from_pyarrow is not None
    print(f"Arrow functions found in module: {ARROW_FUNCTIONS_AVAILABLE}")
except (ImportError, AttributeError) as e:
    print(f"Error checking for Arrow functions: {e}")
    ARROW_FUNCTIONS_AVAILABLE = False


class ArrowNativeIndex:
    """
    Wrapper for using native Arrow integration with fast-inverted-index.
    
    This class demonstrates how to properly use Arrow with fast-inverted-index
    once the native functions are exposed.
    """
    
    def __init__(self, use_parallel: bool = True):
        """
        Initialize a new index with Arrow integration.
        
        Args:
            use_parallel: Whether to use parallel processing for Arrow batches
        """
        self.index = Index.builder().build()
        self.use_parallel = use_parallel
        
    def add_documents_from_arrow(
        self, 
        batch: pa.RecordBatch,
        id_field: str,
        content_fields: List[str],
        metadata_fields: Optional[List[str]] = None
    ) -> Dict[str, Any]:
        """
        Add documents from an Arrow RecordBatch.
        
        This method uses the native implementation when available, and falls back
        to a Python implementation when not.
        
        Args:
            batch: PyArrow RecordBatch containing documents
            id_field: Field name containing document IDs
            content_fields: List of field names to use as content
            metadata_fields: Optional list of field names to store as metadata
            
        Returns:
            Dict with stats about the indexing operation
        """
        if ARROW_FUNCTIONS_AVAILABLE:
            # Use the native implementation
            if self.use_parallel:
                return add_documents_from_pyarrow_parallel(
                    self.index,
                    batch,
                    id_field,
                    content_fields,
                    metadata_fields
                )
            else:
                return add_documents_from_pyarrow(
                    self.index,
                    batch,
                    id_field,
                    content_fields,
                    metadata_fields
                )
        else:
            # Fall back to Python implementation
            print("Warning: Native Arrow functions not available. Using Python fallback.")
            return self._python_add_documents_from_arrow(
                batch,
                id_field,
                content_fields,
                metadata_fields
            )
            
    def _python_add_documents_from_arrow(
        self,
        batch: pa.RecordBatch,
        id_field: str,
        content_fields: List[str],
        metadata_fields: Optional[List[str]] = None
    ) -> Dict[str, Any]:
        """
        Python implementation of Arrow batch processing.
        
        This is a fallback when the native implementation is not available.
        It's less efficient but provides the same functionality.
        
        Args:
            batch: PyArrow RecordBatch containing documents
            id_field: Field name containing document IDs
            content_fields: List of field names to use as content
            metadata_fields: Optional list of field names to store as metadata
            
        Returns:
            Dict with stats about the indexing operation
        """
        start_time = time.time()
        
        # Get indices for fields
        id_idx = batch.schema.get_field_index(id_field)
        content_indices = [batch.schema.get_field_index(f) for f in content_fields]
        meta_indices = None
        if metadata_fields:
            meta_indices = [batch.schema.get_field_index(f) for f in metadata_fields]
            
        # Extract arrays
        id_array = batch.column(id_idx).to_pylist()
        
        # Option 1: Process documents one by one
        if not self.use_parallel:
            docs_indexed = errors = 0
            tokens_indexed = 0
            
            for i in range(batch.num_rows):
                try:
                    # Get document ID
                    doc_id = id_array[i]
                    
                    # Get content
                    content_parts = []
                    for idx in content_indices:
                        value = batch.column(idx)[i].as_py()
                        if value is not None:
                            content_parts.append(str(value))
                    content = " ".join(content_parts)
                    
                    # Get metadata if needed
                    metadata = None
                    if meta_indices:
                        metadata = {}
                        for j, idx in enumerate(meta_indices):
                            value = batch.column(idx)[i].as_py()
                            if value is not None:
                                metadata[metadata_fields[j]] = str(value)
                    
                    # Add document
                    if metadata:
                        self.index.add_document_with_metadata(doc_id, content, metadata)
                    else:
                        self.index.add_document(doc_id, content)
                        
                    docs_indexed += 1
                    tokens_indexed += len(content.split())
                except Exception as e:
                    errors += 1
                    print(f"Error processing document {i}: {e}")
        
        # Option 2: Prepare batch for parallel processing
        else:
            # Extract all arrays at once
            content_arrays = [batch.column(idx).to_pylist() for idx in content_indices]
            
            # Prepare document batch
            doc_batch = []
            for i in range(batch.num_rows):
                try:
                    doc_id = id_array[i]
                    
                    # Combine content fields
                    content_parts = []
                    for arr in content_arrays:
                        value = arr[i]
                        if value is not None:
                            content_parts.append(str(value))
                    content = " ".join(content_parts)
                    
                    doc_batch.append((doc_id, content))
                except Exception as e:
                    print(f"Error preparing document {i}: {e}")
            
            # Process in parallel
            self.index.add_documents_parallel(doc_batch)
            
            docs_indexed = len(doc_batch)
            tokens_indexed = sum(len(content.split()) for _, content in doc_batch)
            errors = batch.num_rows - docs_indexed
        
        elapsed_ms = int((time.time() - start_time) * 1000)
        
        return {
            "documents_indexed": docs_indexed,
            "tokens_indexed": tokens_indexed,
            "elapsed_ms": elapsed_ms,
            "errors": errors
        }
    
    def search(self, query, **kwargs):
        """Search the index with the given query."""
        return self.index.search(query, **kwargs)


def create_test_batch(num_docs: int = 1000) -> pa.RecordBatch:
    """
    Create a test RecordBatch with the specified number of documents.
    
    Args:
        num_docs: Number of documents to include in the batch
        
    Returns:
        PyArrow RecordBatch
    """
    # Generate document data
    ids = list(range(1, num_docs + 1))
    titles = [f"Document {i}" for i in range(1, num_docs + 1)]
    contents = [
        f"This is document {i} with some random content for testing indexing performance "
        f"with words like search engine inverted index and database {i % 100}"
        for i in range(1, num_docs + 1)
    ]
    authors = [f"Author {i % 5}" for i in range(1, num_docs + 1)]
    
    # Create schema
    schema = pa.schema([
        pa.field('id', pa.int64()),
        pa.field('title', pa.string()),
        pa.field('content', pa.string()),
        pa.field('author', pa.string())
    ])
    
    # Create arrays
    id_array = pa.array(ids, type=pa.int64())
    title_array = pa.array(titles, type=pa.string())
    content_array = pa.array(contents, type=pa.string())
    author_array = pa.array(authors, type=pa.string())
    
    # Create batch
    batch = pa.RecordBatch.from_arrays(
        [id_array, title_array, content_array, author_array],
        schema=schema
    )
    
    return batch


def run_benchmark(num_docs: int = 10000, use_parallel: bool = True) -> None:
    """
    Run a benchmark of the Arrow integration.
    
    Args:
        num_docs: Number of documents to index
        use_parallel: Whether to use parallel processing
    """
    print(f"Creating test batch with {num_docs} documents...")
    batch = create_test_batch(num_docs)
    
    print(f"Creating index with {'parallel' if use_parallel else 'sequential'} processing...")
    index = ArrowNativeIndex(use_parallel=use_parallel)
    
    print("Starting batch indexing...")
    start_time = time.time()
    
    stats = index.add_documents_from_arrow(
        batch,
        id_field="id",
        content_fields=["title", "content"],
        metadata_fields=["author"]
    )
    
    elapsed = time.time() - start_time
    
    print("\nIndexing results:")
    print(f"- Documents indexed: {stats['documents_indexed']}")
    print(f"- Tokens indexed: {stats['tokens_indexed']}")
    print(f"- Time taken: {elapsed:.4f} seconds")
    print(f"- Rate: {stats['documents_indexed'] / elapsed:.2f} docs/second")
    print(f"- Token rate: {stats['tokens_indexed'] / elapsed:.2f} tokens/second")
    
    # Test search
    print("\nTesting search...")
    search_start = time.time()
    results = index.search("document")
    search_elapsed = time.time() - search_start

    print(f"Search found {len(results)} documents in {search_elapsed:.4f} seconds")
    if results:
        # Handle different result formats (tuple or dict)
        if isinstance(results[0], tuple):
            doc_id = results[0][0]  # First element is document ID
        else:
            doc_id = results[0]['document_id']

        doc = index.index.get_document(doc_id)
        print(f"First result: Document {doc_id}")
        if isinstance(doc, dict) and 'author' in doc:
            print(f"Author: {doc['author']}")
    
    print(f"\nUsed native Arrow functions: {ARROW_FUNCTIONS_AVAILABLE}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Test Arrow integration")
    parser.add_argument("--docs", type=int, default=10000, help="Number of documents")
    parser.add_argument("--sequential", action="store_true", help="Use sequential processing")
    args = parser.parse_args()
    
    run_benchmark(args.docs, not args.sequential)