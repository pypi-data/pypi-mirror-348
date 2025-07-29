#!/usr/bin/env python3
"""
Comprehensive benchmark for Arrow integration in fast-inverted-index.

This script tests and compares the performance of different indexing methods:
1. Standard indexing (one document at a time)
2. Basic Arrow integration (single-threaded)
3. Parallel Arrow indexing (multi-threaded)
4. Multi-batch Parallel Arrow indexing (multi-threaded with multiple batches)

The script also measures memory usage and generates performance reports.
"""

import time
import os
import shutil
import argparse
import resource
import random
import string
import pandas as pd
import pyarrow as pa
import matplotlib.pyplot as plt
from fast_inverted_index import Index, ParallelIndexingConfig

def get_memory_usage():
    """Get current memory usage in MB."""
    return resource.getrusage(resource.RUSAGE_SELF).ru_maxrss / 1024.0

def generate_test_document(word_count=100, avg_word_length=7):
    """Generate a random document with the specified parameters."""
    words = []
    for _ in range(word_count):
        word_len = max(1, int(random.gauss(avg_word_length, 2)))
        word = ''.join(random.choice(string.ascii_lowercase) for _ in range(word_len))
        words.append(word)
    return ' '.join(words)

def create_test_dataframe(num_docs=10000, words_per_doc=100):
    """Create a test DataFrame with document data."""
    data = {
        'id': list(range(num_docs)),
        'title': [f"Document {i} Title" for i in range(num_docs)],
        'content': [generate_test_document(words_per_doc) for _ in range(num_docs)],
        'author': [f"Author {i % 10}" for i in range(num_docs)],
        'created_at': [int(time.time() - (i * 3600)) for i in range(num_docs)],
        'tags': [f"tag{i % 5},test,document" for i in range(num_docs)],
    }
    return pd.DataFrame(data)

def dataframe_to_batches(df, batch_size=5000):
    """Convert a DataFrame to a list of PyArrow RecordBatches."""
    # Convert DataFrame to PyArrow Table
    table = pa.Table.from_pandas(df)
    
    # Split into batches
    return [batch for batch in table.to_batches(max_chunksize=batch_size)]

def benchmark_standard_indexing(docs_df, index_path):
    """Benchmark standard document-by-document indexing."""
    if os.path.exists(index_path):
        shutil.rmtree(index_path)
    
    index = Index(storage_path=index_path)
    
    # Extract data from DataFrame
    docs = []
    for _, row in docs_df.iterrows():
        docs.append((
            row['id'],
            row['content'],
            {
                'title': row['title'],
                'author': row['author'],
                'created_at': row['created_at'],
                'tags': row['tags']
            }
        ))
    
    # Measure memory before
    mem_before = get_memory_usage()
    
    # Run benchmark
    start_time = time.time()
    
    for doc_id, content, metadata in docs:
        index.add_document(doc_id, content, metadata)
    
    elapsed = time.time() - start_time
    
    # Measure memory after
    mem_after = get_memory_usage()
    mem_used = mem_after - mem_before
    
    # Get stats
    stats = index.stats()
    
    index.close()
    
    return {
        'method': 'Standard',
        'docs_indexed': len(docs),
        'time_seconds': elapsed,
        'docs_per_second': len(docs) / elapsed,
        'memory_mb': mem_used,
    }

def benchmark_arrow_indexing(docs_df, index_path):
    """Benchmark basic Arrow indexing."""
    if os.path.exists(index_path):
        shutil.rmtree(index_path)
    
    index = Index(storage_path=index_path)
    
    # Convert DataFrame to PyArrow batch
    table = pa.Table.from_pandas(docs_df)
    batch = table.to_batches()[0]
    
    # Measure memory before
    mem_before = get_memory_usage()
    
    # Run benchmark
    start_time = time.time()
    
    stats = index.add_documents_from_pyarrow(
        batch,
        "id",
        ["title", "content"],
        ["author", "created_at", "tags"]
    )
    
    elapsed = time.time() - start_time
    
    # Measure memory after
    mem_after = get_memory_usage()
    mem_used = mem_after - mem_before
    
    index.close()
    
    return {
        'method': 'Arrow',
        'docs_indexed': stats['documents_indexed'],
        'time_seconds': elapsed,
        'docs_per_second': stats['documents_indexed'] / elapsed,
        'memory_mb': mem_used,
    }

def benchmark_parallel_arrow(docs_df, index_path, num_threads=0):
    """Benchmark parallel Arrow indexing."""
    if os.path.exists(index_path):
        shutil.rmtree(index_path)
    
    index = Index(storage_path=index_path)
    
    # Convert DataFrame to PyArrow batch
    table = pa.Table.from_pandas(docs_df)
    batch = table.to_batches()[0]
    
    # Create parallel config
    config = ParallelIndexingConfig(
        num_threads=num_threads,  # Auto-detect if 0
        batch_size=100,
        channel_capacity=16
    )
    
    # Measure memory before
    mem_before = get_memory_usage()
    
    # Run benchmark
    start_time = time.time()
    
    stats = index.add_documents_from_pyarrow_parallel(
        batch,
        "id",
        ["title", "content"],
        ["author", "created_at", "tags"],
        config
    )
    
    elapsed = time.time() - start_time
    
    # Measure memory after
    mem_after = get_memory_usage()
    mem_used = mem_after - mem_before
    
    index.close()
    
    return {
        'method': f'Parallel Arrow ({num_threads if num_threads > 0 else "auto"} threads)',
        'docs_indexed': stats['documents_indexed'],
        'time_seconds': elapsed,
        'docs_per_second': stats['documents_indexed'] / elapsed,
        'memory_mb': mem_used,
    }

def benchmark_multi_batch_parallel(docs_df, index_path, batch_size=5000, num_threads=0):
    """Benchmark multi-batch parallel Arrow indexing."""
    if os.path.exists(index_path):
        shutil.rmtree(index_path)
    
    index = Index(storage_path=index_path)
    
    # Convert DataFrame to multiple PyArrow batches
    batches = dataframe_to_batches(docs_df, batch_size)
    
    # Create parallel config
    config = ParallelIndexingConfig(
        num_threads=num_threads,  # Auto-detect if 0
        batch_size=100,
        channel_capacity=16
    )
    
    # Measure memory before
    mem_before = get_memory_usage()
    
    # Run benchmark
    start_time = time.time()
    
    stats = index.add_documents_from_pyarrow_batches_parallel(
        batches,
        "id",
        ["title", "content"],
        ["author", "created_at", "tags"],
        config
    )
    
    elapsed = time.time() - start_time
    
    # Measure memory after
    mem_after = get_memory_usage()
    mem_used = mem_after - mem_before
    
    index.close()
    
    batch_count = len(batches)
    
    return {
        'method': f'Multi-Batch Parallel ({batch_count} batches, {num_threads if num_threads > 0 else "auto"} threads)',
        'docs_indexed': stats['documents_indexed'],
        'time_seconds': elapsed,
        'docs_per_second': stats['documents_indexed'] / elapsed,
        'memory_mb': mem_used,
    }

def run_all_benchmarks(num_docs=50000, words_per_doc=100):
    """Run all benchmarks and compare results."""
    print(f"Generating test data with {num_docs} documents ({words_per_doc} words each)...")
    docs_df = create_test_dataframe(num_docs, words_per_doc)
    
    results = []
    
    # Standard indexing
    print("\nRunning standard indexing benchmark...")
    standard_result = benchmark_standard_indexing(docs_df, "/tmp/standard_index")
    results.append(standard_result)
    print(f"  Completed in {standard_result['time_seconds']:.2f}s ({standard_result['docs_per_second']:.2f} docs/sec)")
    
    # Basic Arrow indexing
    print("\nRunning basic Arrow indexing benchmark...")
    arrow_result = benchmark_arrow_indexing(docs_df, "/tmp/arrow_index")
    results.append(arrow_result)
    print(f"  Completed in {arrow_result['time_seconds']:.2f}s ({arrow_result['docs_per_second']:.2f} docs/sec)")
    
    # Parallel Arrow indexing with auto-detected threads
    print("\nRunning parallel Arrow indexing benchmark (auto-detect threads)...")
    parallel_auto_result = benchmark_parallel_arrow(docs_df, "/tmp/parallel_auto_index")
    results.append(parallel_auto_result)
    print(f"  Completed in {parallel_auto_result['time_seconds']:.2f}s ({parallel_auto_result['docs_per_second']:.2f} docs/sec)")
    
    # Parallel Arrow indexing with fixed threads
    thread_counts = [2, 4, 8]
    for threads in thread_counts:
        print(f"\nRunning parallel Arrow indexing benchmark ({threads} threads)...")
        parallel_result = benchmark_parallel_arrow(docs_df, f"/tmp/parallel_{threads}_index", threads)
        results.append(parallel_result)
        print(f"  Completed in {parallel_result['time_seconds']:.2f}s ({parallel_result['docs_per_second']:.2f} docs/sec)")
    
    # Multi-batch parallel Arrow indexing
    print("\nRunning multi-batch parallel Arrow indexing benchmark...")
    multi_batch_result = benchmark_multi_batch_parallel(docs_df, "/tmp/multi_batch_index")
    results.append(multi_batch_result)
    print(f"  Completed in {multi_batch_result['time_seconds']:.2f}s ({multi_batch_result['docs_per_second']:.2f} docs/sec)")
    
    # Show comparison
    print("\n=== Performance Comparison ===")
    print(f"{'Method':<50} {'Time (s)':<10} {'Rate (docs/s)':<15} {'Memory (MB)':<15}")
    print("-" * 90)
    
    # Sort by performance (docs per second)
    results.sort(key=lambda x: x['docs_per_second'], reverse=True)
    
    baseline = next(r for r in results if r['method'] == 'Standard')['time_seconds']
    baseline_memory = next(r for r in results if r['method'] == 'Standard')['memory_mb']
    
    for result in results:
        speedup = baseline / result['time_seconds']
        memory_ratio = result['memory_mb'] / baseline_memory
        print(f"{result['method']:<50} {result['time_seconds']:.2f}s      {result['docs_per_second']:.2f} ({speedup:.2f}x)    {result['memory_mb']:.2f} ({memory_ratio:.2f}x)")
    
    # Create visualization
    create_performance_chart(results, "performance_comparison.png")
    
    return results

def create_performance_chart(results, output_file):
    """Create a performance comparison chart."""
    plt.figure(figsize=(12, 8))
    
    # Sort by performance
    results = sorted(results, key=lambda x: x['docs_per_second'])
    
    methods = [r['method'] for r in results]
    speeds = [r['docs_per_second'] for r in results]
    
    # Create bar chart
    bars = plt.barh(methods, speeds, color='skyblue')
    
    # Add values to bars
    for bar in bars:
        width = bar.get_width()
        plt.text(width + 0.5, bar.get_y() + bar.get_height()/2, f"{width:.2f} docs/sec", 
                 ha='left', va='center')
    
    plt.xlabel('Documents per Second')
    plt.title('Indexing Performance Comparison')
    plt.tight_layout()
    
    plt.savefig(output_file)
    print(f"\nPerformance chart saved to {output_file}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Benchmark Arrow integration in fast-inverted-index")
    parser.add_argument("--docs", type=int, default=50000, help="Number of documents to index")
    parser.add_argument("--words", type=int, default=100, help="Words per document")
    args = parser.parse_args()
    
    run_all_benchmarks(args.docs, args.words)