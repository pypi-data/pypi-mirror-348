#!/usr/bin/env python
"""
Performance profiling tool for Apache Arrow integration.

This script profiles the performance of Arrow integration under various conditions:
- With different document sizes
- With different batch sizes
- With different thread configurations
- With different content field configurations

It helps identify optimal configurations and bottlenecks in the integration.
"""

import argparse
import gc
import json
import os
import time
import random
import string
import numpy as np
import pyarrow as pa
import fast_inverted_index as fii

# Wrapper class for Arrow integration
class ArrowIndex:
    """Wrapper class that adds Arrow functionality to the Index class."""
    
    def __init__(self, index=None):
        """Initialize with an existing index or create a new one."""
        if index is None:
            self.index = fii.Index.builder().build()
        else:
            self.index = index
    
    def add_documents_from_arrow_batch(self, batch, id_field, content_fields, metadata_fields=None):
        """Add documents from an Arrow RecordBatch to the index."""
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


def generate_random_text(min_words=10, max_words=100, word_length=7):
    """Generate random text with a given word count range and word length."""
    word_count = random.randint(min_words, max_words)
    words = []
    for _ in range(word_count):
        word_len = random.randint(3, word_length)
        word = ''.join(random.choice(string.ascii_lowercase) for _ in range(word_len))
        words.append(word)
    return ' '.join(words)


def generate_test_data(num_docs, content_size_range, num_fields=5):
    """Generate test data with random documents."""
    data = []
    min_words, max_words = content_size_range
    
    for i in range(num_docs):
        doc = {
            "id": i,
            "title": f"Document {i}: {' '.join(random.choice(string.ascii_lowercase) for _ in range(5))}"
        }
        
        # Add content fields
        for j in range(num_fields):
            doc[f"content_{j}"] = generate_random_text(min_words, max_words)
        
        # Add metadata
        doc["author"] = random.choice(["Alice", "Bob", "Charlie", "Dave", "Eve"])
        doc["tags"] = json.dumps([random.choice(["tech", "news", "science", "art", "politics"]) 
                          for _ in range(random.randint(1, 3))])
        doc["timestamp"] = str(int(time.time() - random.randint(0, 3600 * 24 * 30)))
        
        data.append(doc)
    
    return data


def standard_indexing(index, data, content_fields, metadata_fields=None):
    """Index documents using standard method."""
    start_time = time.time()
    
    docs_indexed = 0
    errors = 0
    tokens_indexed = 0
    
    for doc in data:
        try:
            # Get document ID
            doc_id = doc["id"]
            
            # Combine content fields
            content = " ".join(str(doc[field]) for field in content_fields if field in doc)
            
            # Get metadata
            metadata = None
            if metadata_fields:
                metadata = {
                    field: str(doc[field]) 
                    for field in metadata_fields 
                    if field in doc
                }
            
            # Add document
            if metadata:
                index.add_document_with_metadata(doc_id, content, metadata)
            else:
                index.add_document(doc_id, content)
            
            docs_indexed += 1
            tokens_indexed += len(content.split())
            
        except Exception as e:
            errors += 1
            print(f"Error indexing document {doc['id']}: {e}")
    
    elapsed_ms = int((time.time() - start_time) * 1000)
    return {
        "documents_indexed": docs_indexed,
        "tokens_indexed": tokens_indexed,
        "elapsed_ms": elapsed_ms,
        "errors": errors
    }


def arrow_indexing(index, data, content_fields, metadata_fields=None):
    """Index documents using Arrow integration."""
    # Create Arrow RecordBatch
    batch = pa.RecordBatch.from_pylist(data)
    
    # Create wrapper
    arrow_index = ArrowIndex(index)
    
    # Add documents
    return arrow_index.add_documents_from_arrow_batch(
        batch,
        id_field="id",
        content_fields=content_fields,
        metadata_fields=metadata_fields
    )


def profile_document_size():
    """Profile performance with different document sizes."""
    print("\n=== Profiling Document Size Impact ===")
    
    # Fixed document count
    doc_count = 1000
    
    # Test with different document sizes
    sizes = [
        (10, 20),    # Small
        (50, 100),   # Medium
        (500, 1000), # Large
    ]
    
    results = []
    
    for size_range in sizes:
        print(f"\nDocument size: {size_range[0]}-{size_range[1]} words")
        
        # Generate data
        data = generate_test_data(doc_count, size_range)
        
        # Content and metadata fields
        content_fields = ["title", "content_0", "content_1"]
        metadata_fields = ["author", "tags", "timestamp"]
        
        # Standard indexing
        index_std = fii.Index.builder().build()
        std_stats = standard_indexing(index_std, data, content_fields, metadata_fields)
        print(f"Standard: {std_stats['documents_indexed']} docs in {std_stats['elapsed_ms']}ms")
        
        # Force garbage collection
        index_std.close()
        gc.collect()
        
        # Arrow indexing
        index_arrow = fii.Index.builder().build()
        arrow_stats = arrow_indexing(index_arrow, data, content_fields, metadata_fields)
        print(f"Arrow: {arrow_stats['documents_indexed']} docs in {arrow_stats['elapsed_ms']}ms")
        
        # Calculate speedup
        speedup = std_stats['elapsed_ms'] / arrow_stats['elapsed_ms'] if arrow_stats['elapsed_ms'] > 0 else 0
        
        results.append({
            "size_range": f"{size_range[0]}-{size_range[1]}",
            "doc_count": doc_count,
            "std_time_ms": std_stats['elapsed_ms'],
            "arrow_time_ms": arrow_stats['elapsed_ms'],
            "speedup": speedup
        })
        
        # Force garbage collection
        index_arrow.close()
        gc.collect()
    
    return results


def profile_document_count():
    """Profile performance with different document counts."""
    print("\n=== Profiling Document Count Impact ===")
    
    # Fixed document size
    doc_size = (50, 100)
    
    # Test with different document counts
    counts = [100, 1000, 10000]
    
    results = []
    
    for count in counts:
        print(f"\nDocument count: {count}")
        
        # Generate data
        data = generate_test_data(count, doc_size)
        
        # Content and metadata fields
        content_fields = ["title", "content_0", "content_1"]
        metadata_fields = ["author", "tags", "timestamp"]
        
        # Standard indexing
        index_std = fii.Index.builder().build()
        std_stats = standard_indexing(index_std, data, content_fields, metadata_fields)
        print(f"Standard: {std_stats['documents_indexed']} docs in {std_stats['elapsed_ms']}ms")
        
        # Force garbage collection
        index_std.close()
        gc.collect()
        
        # Arrow indexing
        index_arrow = fii.Index.builder().build()
        arrow_stats = arrow_indexing(index_arrow, data, content_fields, metadata_fields)
        print(f"Arrow: {arrow_stats['documents_indexed']} docs in {arrow_stats['elapsed_ms']}ms")
        
        # Calculate speedup
        speedup = std_stats['elapsed_ms'] / arrow_stats['elapsed_ms'] if arrow_stats['elapsed_ms'] > 0 else 0
        
        results.append({
            "doc_count": count,
            "size_range": f"{doc_size[0]}-{doc_size[1]}",
            "std_time_ms": std_stats['elapsed_ms'],
            "arrow_time_ms": arrow_stats['elapsed_ms'],
            "speedup": speedup
        })
        
        # Force garbage collection
        index_arrow.close()
        gc.collect()
    
    return results


def profile_field_count():
    """Profile performance with different numbers of fields."""
    print("\n=== Profiling Field Count Impact ===")
    
    # Fixed document count and size
    doc_count = 1000
    doc_size = (50, 100)
    
    # Test with different numbers of content fields
    field_counts = [1, 3, 5, 10]
    
    results = []
    
    for field_count in field_counts:
        print(f"\nContent fields: {field_count}")
        
        # Generate data with appropriate number of fields
        data = generate_test_data(doc_count, doc_size, num_fields=max(field_counts))
        
        # Content fields
        content_fields = ["title"] + [f"content_{i}" for i in range(field_count-1)]
        # Fixed metadata fields
        metadata_fields = ["author", "tags", "timestamp"]
        
        # Standard indexing
        index_std = fii.Index.builder().build()
        std_stats = standard_indexing(index_std, data, content_fields, metadata_fields)
        print(f"Standard: {std_stats['documents_indexed']} docs in {std_stats['elapsed_ms']}ms")
        
        # Force garbage collection
        index_std.close()
        gc.collect()
        
        # Arrow indexing
        index_arrow = fii.Index.builder().build()
        arrow_stats = arrow_indexing(index_arrow, data, content_fields, metadata_fields)
        print(f"Arrow: {arrow_stats['documents_indexed']} docs in {arrow_stats['elapsed_ms']}ms")
        
        # Calculate speedup
        speedup = std_stats['elapsed_ms'] / arrow_stats['elapsed_ms'] if arrow_stats['elapsed_ms'] > 0 else 0
        
        results.append({
            "field_count": field_count,
            "doc_count": doc_count,
            "size_range": f"{doc_size[0]}-{doc_size[1]}",
            "std_time_ms": std_stats['elapsed_ms'],
            "arrow_time_ms": arrow_stats['elapsed_ms'],
            "speedup": speedup
        })
        
        # Force garbage collection
        index_arrow.close()
        gc.collect()
    
    return results


def summarize_results(results):
    """Print a summary of the profiling results."""
    print("\n=== Results Summary ===")
    
    for result in results:
        for key, value in result.items():
            print(f"{key}: {value}")
        print()


def main():
    """Main function to run the profiling."""
    parser = argparse.ArgumentParser(description="Profile Arrow integration performance.")
    parser.add_argument("--mode", choices=["all", "size", "count", "fields"], default="all",
                        help="Which profiling mode to run")
    parser.add_argument("--output", type=str, help="Output file for results (JSON)")
    args = parser.parse_args()
    
    all_results = {}
    
    if args.mode in ["all", "size"]:
        all_results["document_size"] = profile_document_size()
    
    if args.mode in ["all", "count"]:
        all_results["document_count"] = profile_document_count()
    
    if args.mode in ["all", "fields"]:
        all_results["field_count"] = profile_field_count()
    
    # Summarize results
    summarize_results(all_results.values())
    
    # Save results if output file is specified
    if args.output:
        with open(args.output, 'w') as f:
            json.dump(all_results, f, indent=2)
        print(f"Results saved to {args.output}")


if __name__ == "__main__":
    main()