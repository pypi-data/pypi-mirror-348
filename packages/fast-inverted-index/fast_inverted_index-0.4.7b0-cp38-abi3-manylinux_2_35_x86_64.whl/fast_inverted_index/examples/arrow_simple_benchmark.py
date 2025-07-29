"""
Simple benchmark for Arrow data processing vs standard Python processing.

This script compares the overhead of processing documents via Arrow vs standard Python.
"""

import pyarrow as pa
import time
import random
import string
import json
import argparse

def generate_random_text(min_words=20, max_words=200):
    """Generate random text with given word count range."""
    word_count = random.randint(min_words, max_words)
    words = []
    for _ in range(word_count):
        word_len = random.randint(2, 12)
        word = ''.join(random.choice(string.ascii_lowercase) for _ in range(word_len))
        words.append(word)
    return ' '.join(words)

def generate_test_data(num_docs):
    """Generate test data with random documents."""
    data = []
    for i in range(num_docs):
        doc = {
            "id": i,
            "title": f"Document {i}: {' '.join(random.choice(string.ascii_lowercase) for _ in range(5))}",
            "content": generate_random_text(),
            "author": random.choice(["Alice", "Bob", "Charlie", "Dave", "Eve"]),
            "tags": json.dumps([random.choice(["tech", "news", "science", "art", "politics"]) 
                              for _ in range(random.randint(1, 3))])
        }
        data.append(doc)
    return data

def benchmark_standard_processing(data):
    """Benchmark standard Python document processing."""
    start_time = time.time()
    
    processed_docs = []
    for doc in data:
        # Extract fields (simulating document processing)
        doc_id = doc["id"]
        title = doc["title"]
        content = doc["content"]
        metadata = {
            "author": doc["author"],
            "tags": doc["tags"]
        }
        
        # Combine content fields (simulating document preparation)
        full_content = f"{title} {content}"
        
        # Count tokens (simulating indexing)
        token_count = len(full_content.split())
        
        processed_docs.append({
            "id": doc_id,
            "content": full_content,
            "metadata": metadata,
            "token_count": token_count
        })
    
    elapsed_ms = int((time.time() - start_time) * 1000)
    return {
        "documents_processed": len(processed_docs),
        "elapsed_ms": elapsed_ms
    }

def benchmark_arrow_processing(data):
    """Benchmark Arrow document processing."""
    start_time = time.time()
    
    # Create Arrow RecordBatch
    batch = pa.RecordBatch.from_pylist(data)
    
    # Extract fields from batch
    id_values = batch.column(batch.schema.get_field_index("id")).to_pylist()
    title_values = batch.column(batch.schema.get_field_index("title")).to_pylist()
    content_values = batch.column(batch.schema.get_field_index("content")).to_pylist()
    author_values = batch.column(batch.schema.get_field_index("author")).to_pylist()
    tags_values = batch.column(batch.schema.get_field_index("tags")).to_pylist()
    
    # Process documents
    processed_docs = []
    for i in range(batch.num_rows):
        # Extract data for this row
        doc_id = id_values[i]
        title = title_values[i]
        content = content_values[i]
        
        # Combine content fields
        full_content = f"{title} {content}"
        
        # Create metadata
        metadata = {
            "author": author_values[i],
            "tags": tags_values[i]
        }
        
        # Count tokens
        token_count = len(full_content.split())
        
        processed_docs.append({
            "id": doc_id,
            "content": full_content,
            "metadata": metadata,
            "token_count": token_count
        })
    
    elapsed_ms = int((time.time() - start_time) * 1000)
    return {
        "documents_processed": len(processed_docs),
        "elapsed_ms": elapsed_ms
    }

def benchmark_arrow_batch_processing(data):
    """Benchmark Arrow document processing with batch operations."""
    start_time = time.time()
    
    # Create Arrow RecordBatch
    batch = pa.RecordBatch.from_pylist(data)
    
    # Extract all fields at once
    id_values = batch.column(batch.schema.get_field_index("id")).to_pylist()
    title_values = batch.column(batch.schema.get_field_index("title")).to_pylist()
    content_values = batch.column(batch.schema.get_field_index("content")).to_pylist()
    author_values = batch.column(batch.schema.get_field_index("author")).to_pylist()
    tags_values = batch.column(batch.schema.get_field_index("tags")).to_pylist()
    
    # Combine content fields in bulk
    full_contents = [f"{title} {content}" for title, content in zip(title_values, content_values)]
    
    # Create metadata in bulk
    metadata_list = [{"author": author, "tags": tags} for author, tags in zip(author_values, tags_values)]
    
    # Count tokens in bulk
    token_counts = [len(content.split()) for content in full_contents]
    
    # Create result objects in bulk
    processed_docs = [
        {"id": doc_id, "content": content, "metadata": metadata, "token_count": token_count}
        for doc_id, content, metadata, token_count in zip(
            id_values, full_contents, metadata_list, token_counts
        )
    ]
    
    elapsed_ms = int((time.time() - start_time) * 1000)
    return {
        "documents_processed": len(processed_docs),
        "elapsed_ms": elapsed_ms
    }

def run_benchmark(num_docs=1000, num_runs=3):
    """Run benchmark comparing standard and Arrow processing."""
    print(f"Generating {num_docs} test documents...")
    
    std_times = []
    arrow_times = []
    arrow_batch_times = []
    
    print(f"Running {num_runs} benchmarks with {num_docs} documents each...")
    
    for i in range(num_runs):
        print(f"\nRun {i+1}/{num_runs}:")
        
        # Generate fresh data for each run
        run_data = generate_test_data(num_docs)
        
        # Standard processing approach
        std_stats = benchmark_standard_processing(run_data)
        std_times.append(std_stats["elapsed_ms"])
        print(f"Standard processing: {std_stats['elapsed_ms']}ms")
        
        # Arrow row-by-row processing approach
        arrow_stats = benchmark_arrow_processing(run_data)
        arrow_times.append(arrow_stats["elapsed_ms"])
        print(f"Arrow row-by-row processing: {arrow_stats['elapsed_ms']}ms")
        
        # Arrow batch processing approach
        arrow_batch_stats = benchmark_arrow_batch_processing(run_data)
        arrow_batch_times.append(arrow_batch_stats["elapsed_ms"])
        print(f"Arrow batch processing: {arrow_batch_stats['elapsed_ms']}ms")
    
    # Calculate averages
    avg_std = sum(std_times) / len(std_times)
    avg_arrow = sum(arrow_times) / len(arrow_times)
    avg_arrow_batch = sum(arrow_batch_times) / len(arrow_batch_times)
    
    # Print summary
    print("\n===== BENCHMARK SUMMARY =====")
    print(f"Document count: {num_docs}")
    print(f"Average standard processing time: {avg_std:.2f}ms")
    print(f"Average Arrow row-by-row processing time: {avg_arrow:.2f}ms")
    print(f"Average Arrow batch processing time: {avg_arrow_batch:.2f}ms")
    
    if avg_std > 0:
        print(f"Speedup (Arrow row-by-row vs standard): {avg_std/avg_arrow:.2f}x")
        print(f"Speedup (Arrow batch vs standard): {avg_std/avg_arrow_batch:.2f}x")
    
    print("=============================")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Benchmark Arrow processing")
    parser.add_argument("--docs", type=int, default=1000, help="Number of documents")
    parser.add_argument("--runs", type=int, default=3, help="Number of benchmark runs")
    args = parser.parse_args()
    
    run_benchmark(num_docs=args.docs, num_runs=args.runs)