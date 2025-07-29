#!/usr/bin/env python3
"""
Example demonstrating Apache Arrow integration with fast-inverted-index.

This example shows how to:
1. Create PyArrow RecordBatches containing documents
2. Use zero-copy transfer to index documents efficiently
3. Compare performance with standard indexing method
"""

import time
import os
import shutil
import numpy as np
import pyarrow as pa
from fast_inverted_index import Index, Schema, FieldSchema

def create_test_record_batch(num_docs=1000):
    """Create a test record batch with document data."""
    # Define the schema
    schema = pa.schema([
        pa.field('id', pa.int64()),
        pa.field('title', pa.string()),
        pa.field('content', pa.string()),
        pa.field('author', pa.string()),
        pa.field('created_at', pa.int64()),
        pa.field('tags', pa.string()),
    ])
    
    # Create arrays for each field
    ids = pa.array(range(num_docs), type=pa.int64())
    
    titles = []
    contents = []
    authors = []
    created_ats = []
    tags = []
    
    for i in range(num_docs):
        titles.append(f"Document {i} Title")
        contents.append(f"This is the content of document {i}. It contains various words for searching.")
        authors.append(f"Author {i % 10}")
        created_ats.append(int(time.time() - (i * 3600)))  # Different timestamps
        tags.append(f"tag{i % 5},test,document")
    
    # Convert to Arrow arrays
    titles = pa.array(titles, type=pa.string())
    contents = pa.array(contents, type=pa.string())
    authors = pa.array(authors, type=pa.string())
    created_ats = pa.array(created_ats, type=pa.int64())
    tags = pa.array(tags, type=pa.string())
    
    # Create record batch
    return pa.RecordBatch.from_arrays(
        [ids, titles, contents, authors, created_ats, tags],
        schema=schema
    )

def test_arrow_integration():
    """Test Arrow integration with the index."""
    # Clean up any existing index
    index_path = "/tmp/arrow_index"
    if os.path.exists(index_path):
        shutil.rmtree(index_path)
    
    # Create index
    index = Index(storage_path=index_path)
    
    # Create a test record batch
    print("Creating test record batch...")
    batch = create_test_record_batch(num_docs=10000)
    print(f"Created batch with {batch.num_rows} rows")
    
    # Index documents using Arrow
    print("\nIndexing documents using Arrow integration...")
    start_time = time.time()
    stats = index.add_documents_from_pyarrow(
        batch,
        "id",
        ["title", "content"],
        ["author", "created_at", "tags"]
    )
    arrow_time = time.time() - start_time
    
    print(f"Arrow indexing completed in {arrow_time:.2f} seconds")
    print(f"Documents indexed: {stats['documents_indexed']}")
    print(f"Tokens indexed: {stats['tokens_indexed']}")
    print(f"Errors: {stats['errors']}")
    print(f"Rate: {stats['documents_indexed'] / arrow_time:.2f} docs/sec")
    
    # Test search
    print("\nTesting search...")
    results = index.search("document 42")
    print(f"Found {len(results)} results")
    if results:
        print(f"Top result: Document {results[0][0]} with score {results[0][1]:.4f}")
    
    # Close index
    index.close()
    
    print("\nTest completed successfully!")

def benchmark_arrow_vs_standard(num_docs=10000):
    """Benchmark Arrow integration vs standard indexing."""
    # Clean up any existing indices
    arrow_index_path = "/tmp/arrow_benchmark"
    standard_index_path = "/tmp/standard_benchmark"
    
    for path in [arrow_index_path, standard_index_path]:
        if os.path.exists(path):
            shutil.rmtree(path)
    
    # Create record batch
    print(f"Creating test data with {num_docs} documents...")
    batch = create_test_record_batch(num_docs=num_docs)
    
    # Extract standard data for comparison
    ids = batch.column(0).to_pylist()
    titles = batch.column(1).to_pylist()
    contents = batch.column(2).to_pylist()
    authors = batch.column(3).to_pylist()
    created_ats = batch.column(4).to_pylist()
    tags = batch.column(5).to_pylist()
    
    # Benchmark Arrow indexing
    print("\nBenchmarking Arrow indexing...")
    arrow_index = Index(storage_path=arrow_index_path)
    start_time = time.time()
    stats = arrow_index.add_documents_from_pyarrow(
        batch,
        "id",
        ["title", "content"],
        ["author", "created_at", "tags"]
    )
    arrow_time = time.time() - start_time
    arrow_index.close()
    
    # Benchmark standard indexing
    print("\nBenchmarking standard indexing...")
    standard_index = Index(storage_path=standard_index_path)
    start_time = time.time()
    
    for i in range(num_docs):
        metadata = {
            "title": titles[i],
            "author": authors[i],
            "created_at": created_ats[i],
            "tags": tags[i]
        }
        standard_index.add_document(ids[i], contents[i], metadata)
        
        # Print progress every 1000 documents
        if (i + 1) % 1000 == 0:
            print(f"  Indexed {i + 1} documents...")
    
    standard_time = time.time() - start_time
    standard_index.close()
    
    # Report results
    print("\n=== Benchmark Results ===")
    print(f"Documents: {num_docs}")
    print(f"Arrow indexing time: {arrow_time:.2f} seconds ({num_docs / arrow_time:.2f} docs/sec)")
    print(f"Standard indexing time: {standard_time:.2f} seconds ({num_docs / standard_time:.2f} docs/sec)")
    print(f"Speedup: {standard_time / arrow_time:.2f}x")

def test_multiple_batches():
    """Test indexing multiple batches."""
    # Clean up any existing index
    index_path = "/tmp/multi_batch_index"
    if os.path.exists(index_path):
        shutil.rmtree(index_path)
    
    # Create index
    index = Index(storage_path=index_path)
    
    # Create multiple batches
    print("Creating test batches...")
    batch1 = create_test_record_batch(num_docs=5000)
    batch2 = create_test_record_batch(num_docs=5000)
    
    # Index documents using multiple batches
    print("\nIndexing multiple batches...")
    start_time = time.time()
    stats = index.add_documents_from_pyarrow_batches(
        [batch1, batch2],
        "id",
        ["title", "content"],
        ["author", "created_at", "tags"]
    )
    multi_batch_time = time.time() - start_time
    
    print(f"Multi-batch indexing completed in {multi_batch_time:.2f} seconds")
    print(f"Documents indexed: {stats['documents_indexed']}")
    print(f"Tokens indexed: {stats['tokens_indexed']}")
    print(f"Rate: {stats['documents_indexed'] / multi_batch_time:.2f} docs/sec")
    
    # Close index
    index.close()

if __name__ == "__main__":
    print("=== Testing Arrow Integration ===")
    test_arrow_integration()
    
    print("\n=== Benchmarking Arrow vs Standard Indexing ===")
    benchmark_arrow_vs_standard(num_docs=10000)
    
    print("\n=== Testing Multiple Batches ===")
    test_multiple_batches()