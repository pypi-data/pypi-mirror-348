#!/usr/bin/env python3
"""
Example demonstrating parallel Arrow integration with fast-inverted-index.

This example shows how to:
1. Create PyArrow RecordBatches containing large document collections
2. Use parallel processing to efficiently index documents
3. Compare performance between parallel and non-parallel methods
"""

import time
import os
import shutil
import numpy as np
import pyarrow as pa
from fast_inverted_index import Index, Schema, FieldSchema, ParallelIndexingConfig

def create_large_test_batch(num_docs=10000):
    """Create a large test record batch with document data."""
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
    
    # Generate larger content for better benchmarking
    for i in range(num_docs):
        titles.append(f"Document {i} - Comprehensive Title for Testing")
        
        # Generate content with more tokens for realistic benchmarking
        content_parts = [
            f"This is document {i} with extended content for parallel processing benchmarks.",
            "It contains multiple sentences and paragraphs to better simulate real-world data.",
            "The content includes various words and phrases that will be tokenized and indexed.",
            f"Some specific terms like parallel processing, benchmarking, and document {i}",
            "are included to enable specific search tests after indexing is complete.",
            f"Author {i % 10} has written this document with ID {i} for testing purposes.",
            "The indexing system should efficiently process this content in parallel."
        ]
        contents.append(" ".join(content_parts))
        
        authors.append(f"Author {i % 10}")
        created_ats.append(int(time.time() - (i * 3600)))
        tags.append(f"tag{i % 5},parallel,benchmark")
    
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

def benchmark_parallel_vs_sequential(num_docs=10000):
    """Benchmark parallel Arrow indexing against sequential indexing."""
    # Clean up any existing indices
    parallel_index_path = "/tmp/parallel_arrow_benchmark"
    sequential_index_path = "/tmp/sequential_arrow_benchmark"
    
    for path in [parallel_index_path, sequential_index_path]:
        if os.path.exists(path):
            shutil.rmtree(path)
    
    # Create a large test batch
    print(f"Creating test batch with {num_docs} documents...")
    batch = create_large_test_batch(num_docs=num_docs)
    print(f"Created batch with {batch.num_rows} rows")
    
    # Sequential indexing
    print("\nBenchmarking sequential Arrow indexing...")
    sequential_index = Index(storage_path=sequential_index_path)
    
    sequential_start = time.time()
    sequential_stats = sequential_index.add_documents_from_pyarrow(
        batch,
        "id",
        ["title", "content"],
        ["author", "created_at", "tags"]
    )
    sequential_time = time.time() - sequential_start
    
    print(f"Sequential indexing completed in {sequential_time:.2f} seconds")
    print(f"Documents indexed: {sequential_stats['documents_indexed']}")
    print(f"Rate: {sequential_stats['documents_indexed'] / sequential_time:.2f} docs/sec")
    
    sequential_index.close()
    
    # Parallel indexing
    print("\nBenchmarking parallel Arrow indexing...")
    parallel_index = Index(storage_path=parallel_index_path)
    
    # Create parallel config
    parallel_config = ParallelIndexingConfig(
        num_threads=0,  # Auto-detect CPU cores
        batch_size=100, 
        channel_capacity=16
    )
    
    parallel_start = time.time()
    parallel_stats = parallel_index.add_documents_from_pyarrow_parallel(
        batch,
        "id",
        ["title", "content"],
        ["author", "created_at", "tags"],
        parallel_config
    )
    parallel_time = time.time() - parallel_start
    
    print(f"Parallel indexing completed in {parallel_time:.2f} seconds")
    print(f"Documents indexed: {parallel_stats['documents_indexed']}")
    print(f"Rate: {parallel_stats['documents_indexed'] / parallel_time:.2f} docs/sec")
    
    parallel_index.close()
    
    # Compare results
    print("\n=== Performance Comparison ===")
    speedup = sequential_time / parallel_time
    print(f"Sequential: {sequential_time:.2f} seconds ({sequential_stats['documents_indexed'] / sequential_time:.2f} docs/sec)")
    print(f"Parallel:   {parallel_time:.2f} seconds ({parallel_stats['documents_indexed'] / parallel_time:.2f} docs/sec)")
    print(f"Speedup:    {speedup:.2f}x")

def test_multi_batch_parallel():
    """Test parallel indexing with multiple batches."""
    # Clean up existing index
    index_path = "/tmp/multi_batch_parallel"
    if os.path.exists(index_path):
        shutil.rmtree(index_path)
    
    # Create multiple batches
    print("Creating test batches...")
    batch1 = create_large_test_batch(num_docs=5000)
    batch2 = create_large_test_batch(num_docs=5000)
    batch3 = create_large_test_batch(num_docs=5000)
    batch4 = create_large_test_batch(num_docs=5000)
    
    batches = [batch1, batch2, batch3, batch4]
    print(f"Created {len(batches)} batches with {sum(b.num_rows for b in batches)} total documents")
    
    # Create index
    index = Index(storage_path=index_path)
    
    # Create parallel config
    parallel_config = ParallelIndexingConfig(
        num_threads=0,  # Auto-detect CPU cores
        batch_size=100, 
        channel_capacity=8
    )
    
    # Index using parallel multi-batch
    print("\nIndexing multiple batches in parallel...")
    start_time = time.time()
    stats = index.add_documents_from_pyarrow_batches_parallel(
        batches,
        "id",
        ["title", "content"],
        ["author", "created_at", "tags"],
        parallel_config
    )
    elapsed = time.time() - start_time
    
    print(f"Multi-batch parallel indexing completed in {elapsed:.2f} seconds")
    print(f"Documents indexed: {stats['documents_indexed']}")
    print(f"Rate: {stats['documents_indexed'] / elapsed:.2f} docs/sec")
    
    # Test search
    print("\nTesting search...")
    results = index.search("parallel processing")
    print(f"Found {len(results)} results")
    
    # Close the index
    index.close()

def cpu_scaling_test(num_docs=20000):
    """Test scaling with different numbers of CPU cores."""
    # Clean up existing index
    index_path = "/tmp/cpu_scaling_test"
    if os.path.exists(index_path):
        shutil.rmtree(index_path)
    
    # Create a large test batch
    print(f"Creating test batch with {num_docs} documents...")
    batch = create_large_test_batch(num_docs=num_docs)
    
    # Test with different numbers of threads
    thread_counts = [1, 2, 4, 8, 16, 0]  # 0 means auto-detect
    results = {}
    
    for threads in thread_counts:
        # Clean the index directory
        if os.path.exists(index_path):
            shutil.rmtree(index_path)
        
        # Create a fresh index
        index = Index(storage_path=index_path)
        
        # Create parallel config
        parallel_config = ParallelIndexingConfig(
            num_threads=threads,
            batch_size=100, 
            channel_capacity=8
        )
        
        # Run the test
        print(f"\nTesting with {threads} threads {'(auto)' if threads == 0 else ''}...")
        start_time = time.time()
        stats = index.add_documents_from_pyarrow_parallel(
            batch,
            "id",
            ["title", "content"],
            None,
            parallel_config
        )
        elapsed = time.time() - start_time
        
        # Record results
        thread_desc = "auto" if threads == 0 else str(threads)
        results[thread_desc] = {
            "time": elapsed,
            "docs": stats["documents_indexed"],
            "rate": stats["documents_indexed"] / elapsed
        }
        
        print(f"Completed in {elapsed:.2f} seconds")
        print(f"Rate: {stats['documents_indexed'] / elapsed:.2f} docs/sec")
        
        # Close the index
        index.close()
    
    # Print comparison
    print("\n=== CPU Scaling Results ===")
    print(f"{'Threads':<10} {'Time (s)':<10} {'Rate (docs/s)':<15}")
    print("-" * 35)
    
    baseline = results["1"]["time"]
    for threads, data in results.items():
        speedup = baseline / data["time"]
        print(f"{threads:<10} {data['time']:.2f}s      {data['rate']:.2f} ({speedup:.2f}x)")

if __name__ == "__main__":
    print("=== Testing Parallel Arrow Indexing ===")
    
    print("\n=== Benchmarking Parallel vs Sequential Arrow Indexing ===")
    benchmark_parallel_vs_sequential(num_docs=20000)
    
    print("\n=== Testing Multi-Batch Parallel Indexing ===")
    test_multi_batch_parallel()
    
    print("\n=== CPU Scaling Test ===")
    cpu_scaling_test(num_docs=20000)