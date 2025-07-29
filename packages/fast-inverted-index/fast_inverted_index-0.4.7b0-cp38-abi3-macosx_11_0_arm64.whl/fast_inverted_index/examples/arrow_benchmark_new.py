"""
Benchmark for Arrow integration with fast-inverted-index.

This script benchmarks the performance of using Arrow for document loading
compared to standard document loading.
"""

import fast_inverted_index as fii
import pyarrow as pa
import time
import random
import string
import json
import argparse

# Implementation of our temporary ArrowIndex wrapper
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


def benchmark_standard_loading(index, data):
    """Benchmark standard document loading."""
    start_time = time.time()

    for doc in data:
        try:
            metadata = {
                "author": doc["author"],
                "tags": doc["tags"]
            }
            content = f"{doc['title']} {doc['content']}"
            index.add_document_with_metadata(doc["id"], content, metadata)
        except Exception as e:
            print(f"Error indexing document {doc['id']}: {e}")

    elapsed_ms = int((time.time() - start_time) * 1000)
    return {
        "documents_indexed": len(data),
        "elapsed_ms": elapsed_ms
    }


def benchmark_arrow_loading(data):
    """Benchmark Arrow document loading."""
    # Create Arrow RecordBatch
    batch = pa.RecordBatch.from_pylist(data)

    # Create in-memory index and wrapper
    index_config = fii.IndexConfig()
    index_config.storage_type = "memory"
    index = fii.Index.builder().with_config(index_config).build()
    arrow_index = ArrowIndex(index)

    # Add documents via Arrow
    stats = arrow_index.add_documents_from_arrow_batch(
        batch,
        id_field="id",
        content_fields=["title", "content"],
        metadata_fields=["author", "tags"]
    )

    return stats, index


def run_benchmark(num_docs=1000, num_runs=3):
    """Run benchmark comparing standard and Arrow loading."""
    print(f"Generating {num_docs} test documents...")
    data = generate_test_data(num_docs)

    std_times = []
    arrow_times = []

    print(f"Running {num_runs} benchmarks with {num_docs} documents each...")

    for i in range(num_runs):
        print(f"\nRun {i+1}/{num_runs}:")

        try:
            # Create separate data for each run to avoid document ID conflicts
            run_data = generate_test_data(num_docs)

            # Benchmark standard loading with in-memory index
            index_config = fii.IndexConfig()
            index_config.storage_type = "memory"
            index_std = fii.Index.builder().with_config(index_config).build()

            std_stats = benchmark_standard_loading(index_std, run_data)
            std_times.append(std_stats["elapsed_ms"])
            print(f"Standard loading: {std_stats['elapsed_ms']}ms")

            # Create separate data for Arrow to avoid conflicts
            arrow_data = generate_test_data(num_docs)

            # Benchmark Arrow loading with in-memory index
            arrow_stats, index_arrow = benchmark_arrow_loading(arrow_data)
            arrow_times.append(arrow_stats["elapsed_ms"])
            print(f"Arrow loading: {arrow_stats['elapsed_ms']}ms")

            # Validate results (might not have same counts due to random data)
            test_query = "document"
            std_results = index_std.search(test_query)
            arrow_results = index_arrow.search(test_query)
            print(f"Result counts - Standard: {len(std_results)}, Arrow: {len(arrow_results)}")

            # Explicitly close indexes
            index_std.close()
            index_arrow.close()

        except Exception as e:
            print(f"Error in benchmark run {i+1}: {e}")

    if not std_times or not arrow_times:
        print("No benchmark data collected. All runs failed.")
        return

    # Calculate averages
    avg_std = sum(std_times) / len(std_times)
    avg_arrow = sum(arrow_times) / len(arrow_times)

    # Print summary
    print("\n===== BENCHMARK SUMMARY =====")
    print(f"Document count: {num_docs}")
    print(f"Average standard loading time: {avg_std:.2f}ms")
    print(f"Average Arrow loading time: {avg_arrow:.2f}ms")
    print(f"Speedup: {avg_std/avg_arrow:.2f}x")
    print("=============================")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Benchmark Arrow integration")
    parser.add_argument("--docs", type=int, default=1000, help="Number of documents")
    parser.add_argument("--runs", type=int, default=3, help="Number of benchmark runs")
    args = parser.parse_args()
    
    run_benchmark(num_docs=args.docs, num_runs=args.runs)