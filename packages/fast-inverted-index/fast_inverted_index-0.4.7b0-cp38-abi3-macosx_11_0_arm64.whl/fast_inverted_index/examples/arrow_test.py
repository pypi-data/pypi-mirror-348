"""
Test script for Arrow integration with fast-inverted-index.

This script demonstrates how to use Arrow with the fast-inverted-index library
by implementing a small wrapper around the Index class.
"""

import fast_inverted_index as fii
import pyarrow as pa
import json
import time

class ArrowIndex:
    """Wrapper class that adds Arrow functionality to the Index class."""
    
    def __init__(self, index=None):
        """Initialize with an existing index or create a new one."""
        if index is None:
            self.index = fii.Index.builder().build()
        else:
            self.index = index
    
    def add_documents_from_arrow_batch(self, batch, id_field, content_fields, metadata_fields=None):
        """Add documents from an Arrow RecordBatch to the index.
        
        Args:
            batch: A pyarrow.RecordBatch containing documents to index
            id_field: The name of the field to use as document ID
            content_fields: List of fields to index for search
            metadata_fields: Optional list of fields to store as metadata
            
        Returns:
            Dict with stats about the indexing operation
        """
        start_time = time.time()
        
        # Get field values
        id_values = batch.column(batch.schema.get_field_index(id_field)).to_pylist()
        
        # Process each document
        content_indexes = [batch.schema.get_field_index(field) for field in content_fields]
        metadata_indexes = None
        if metadata_fields:
            metadata_indexes = [batch.schema.get_field_index(field) for field in metadata_fields]
        
        # Track stats
        docs_indexed = 0
        tokens_indexed = 0
        errors = 0
        
        for i in range(batch.num_rows):
            try:
                # Get document ID
                doc_id = id_values[i]
                
                # Get content fields
                content = " ".join(str(batch.column(idx)[i].as_py()) 
                                 for idx in content_indexes)
                
                # Get metadata if requested
                metadata = None
                if metadata_indexes:
                    metadata = {
                        metadata_fields[j]: str(batch.column(idx)[i].as_py())
                        for j, idx in enumerate(metadata_indexes)
                    }
                
                # Add the document
                if metadata:
                    self.index.add_document_with_metadata(doc_id, content, metadata)
                else:
                    self.index.add_document(doc_id, content)
                
                docs_indexed += 1
                # Approximate token count (simple space-based split)
                tokens_indexed += len(content.split())
                
            except Exception as e:
                errors += 1
                print(f"Error indexing document {i}: {e}")
        
        # Return stats
        elapsed_ms = int((time.time() - start_time) * 1000)
        return {
            "documents_indexed": docs_indexed,
            "tokens_indexed": tokens_indexed,
            "elapsed_ms": elapsed_ms,
            "errors": errors
        }

def main():
    """Run a simple Arrow integration test."""
    # Create sample data
    data = [
        {"id": 1, "title": "Arrow Integration", "content": "Fast zero-copy data transfer", "author": "Dev"},
        {"id": 2, "title": "PyO3 Bindings", "content": "Rust and Python interoperability", "author": "Dev"},
        {"id": 3, "title": "Performance Boost", "content": "Bulk document loading optimizations", "author": "Dev"},
    ]
    
    # Create Arrow RecordBatch
    batch = pa.RecordBatch.from_pylist(data)
    print(f"Created Arrow batch with {batch.num_rows} rows and schema:")
    print(batch.schema)
    
    # Create index and wrapper
    index = fii.Index.builder().build()
    arrow_index = ArrowIndex(index)
    
    # Add documents
    stats = arrow_index.add_documents_from_arrow_batch(
        batch,
        id_field="id",
        content_fields=["title", "content"],
        metadata_fields=["author"]
    )
    
    print(f"Indexing stats: {json.dumps(stats, indent=2)}")
    
    # Perform a search
    results = index.search("arrow integration")
    print(f"\nSearch results for 'arrow integration':")
    for hit in results:
        print(f"  Document ID: {hit['document_id']}, Score: {hit['score']}")
        metadata = index.get_document(hit['document_id'])
        print(f"  Metadata: {metadata}")
    
    print("\nTest completed successfully!")

if __name__ == "__main__":
    main()