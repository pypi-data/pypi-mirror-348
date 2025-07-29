#!/usr/bin/env python
"""
Benchmark comparing standard indexing vs. Arrow-based indexing in fast-inverted-index.

This script focuses on comparing:
1. Standard document-by-document indexing
2. Arrow batch-based indexing
"""

import fast_inverted_index as fii
import pyarrow as pa
import time
import random
import string
import json
import argparse
import gc

# ============ Wrapper for Arrow indexing ============

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
                # Get document ID and ensure it's an integer
                doc_id = id_values[i]
                if isinstance(doc_id, str):
                    try:
                        doc_id = int(doc_id)
                    except ValueError:
                        raise ValueError(f"Document ID must be convertible to integer: {doc_id}")
                
                # Get content fields, handling nulls
                content_parts = []
                for idx in content_indexes:
                    try:
                        value = batch.column(idx)[i].as_py()
                        if value is not None:  # Skip null values
                            content_parts.append(str(value))
                    except Exception as e:
                        # Skip this field if there's an error
                        print(f"Warning: Error accessing field at index {idx}: {e}")

                content = " ".join(content_parts)
                
                # Get metadata if requested
                metadata = None
                if metadata_indexes:
                    metadata = {}
                    for j, idx in enumerate(metadata_indexes):
                        try:
                            value = batch.column(idx)[i].as_py()
                            if value is not None:  # Skip null values
                                metadata[metadata_fields[j]] = str(value)
                        except Exception as e:
                            # Skip this field if there's an error
                            print(f"Warning: Error accessing metadata field {metadata_fields[j]}: {e}")
                
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

# =============== Data Generation ================

def generate_random_text(min_words=20, max_words=50, word_length=7):
    """Generate random text with a given word count range and word length."""
    word_count = random.randint(min_words, max_words)
    words = []
    for _ in range(word_count):
        word_len = random.randint(3, word_length)
        word = ''.join(random.choice(string.ascii_lowercase) for _ in range(word_len))
        words.append(word)
    return ' '.join(words)

def generate_test_documents(num_docs=1000):
    """Generate test documents for benchmarking."""
    documents = []
    for i in range(num_docs):
        # Create unique ID starting from a large number to avoid conflicts
        doc_id = 1000000 + i

        doc = {
            "id": doc_id,
            "title": f"Document {doc_id}",
            "content": generate_random_text(),
            "author": random.choice(["Alice", "Bob", "Charlie", "David", "Eve"]),
            "tags": f"tag{i%5},test,document"
        }
        documents.append(doc)
    return documents

# =============== Benchmarks ================

def benchmark_standard_indexing(documents):
    """Benchmark standard document-by-document indexing."""
    print(f"Standard indexing: {len(documents)} documents")

    # Create fresh index with in-memory storage explicitly
    builder = fii.IndexBuilder()
    builder.with_in_memory(True)
    index = builder.build()

    # Force garbage collection to start with a clean slate
    gc.collect()

    # Start timing
    start_time = time.time()

    # Add documents one by one
    docs_indexed = 0
    for doc in documents:
        try:
            doc_id = doc["id"]
            content = f"{doc['title']} {doc['content']}"
            metadata = {
                "author": doc["author"],
                "tags": doc["tags"]
            }
            index.add_document_with_metadata(doc_id, content, metadata)
            docs_indexed += 1
        except Exception as e:
            print(f"Error indexing document {doc['id']}: {e}")

    # End timing
    elapsed = time.time() - start_time

    print(f"Indexed {docs_indexed} documents in {elapsed:.4f} seconds")
    print(f"Rate: {docs_indexed / elapsed:.2f} documents per second")

    return {
        "method": "Standard",
        "elapsed_seconds": elapsed,
        "documents_indexed": docs_indexed,
        "documents_per_second": docs_indexed / elapsed if docs_indexed > 0 else 0
    }

def benchmark_arrow_indexing(documents):
    """Benchmark Arrow batch-based indexing."""
    print(f"Arrow batch indexing: {len(documents)} documents")

    # Create Arrow RecordBatch
    batch = pa.RecordBatch.from_pylist(documents)

    # Create fresh index with in-memory storage explicitly
    builder = fii.IndexBuilder()
    builder.with_in_memory(True)
    index = builder.build()
    arrow_index = ArrowIndex(index)

    # Force garbage collection to start with a clean slate
    gc.collect()

    # Start timing
    start_time = time.time()

    # Add documents from Arrow batch
    stats = arrow_index.add_documents_from_arrow_batch(
        batch,
        id_field="id",
        content_fields=["title", "content"],
        metadata_fields=["author", "tags"]
    )

    # End timing
    elapsed = time.time() - start_time

    print(f"Indexed {stats['documents_indexed']} documents in {elapsed:.4f} seconds")
    print(f"Rate: {stats['documents_indexed'] / elapsed:.2f} documents per second")

    return {
        "method": "Arrow",
        "elapsed_seconds": elapsed,
        "documents_indexed": stats["documents_indexed"],
        "documents_per_second": stats["documents_indexed"] / elapsed if stats["documents_indexed"] > 0 else 0,
        "tokens_indexed": stats["tokens_indexed"]
    }

def run_comparison(num_docs=10000, num_runs=3):
    """Run benchmarks comparing standard and Arrow indexing."""
    print(f"=== Running comparison with {num_docs} documents, {num_runs} runs each ===\n")

    standard_results = []
    arrow_results = []

    for i in range(num_runs):
        print(f"=== Run {i+1}/{num_runs} ===")

        # Generate fresh documents for standard indexing
        print(f"Generating {num_docs} test documents for standard indexing...")
        standard_documents = generate_test_documents(num_docs)

        # Generate fresh documents for Arrow indexing with different IDs
        print(f"Generating {num_docs} test documents for Arrow indexing...")
        arrow_documents = []
        for i, doc in enumerate(generate_test_documents(num_docs)):
            # Use a different ID range for Arrow documents
            doc["id"] += 2000000  # Start from 3,000,000
            arrow_documents.append(doc)

        # Run standard indexing benchmark
        print("\nTesting standard indexing...")
        standard_result = benchmark_standard_indexing(standard_documents)
        standard_results.append(standard_result)

        # Run Arrow indexing benchmark
        print("\nTesting Arrow indexing...")
        arrow_result = benchmark_arrow_indexing(arrow_documents)
        arrow_results.append(arrow_result)
        
        print()  # Add spacing between runs
    
    # Calculate averages
    avg_standard_time = sum(r["elapsed_seconds"] for r in standard_results) / num_runs
    avg_standard_rate = sum(r["documents_per_second"] for r in standard_results) / num_runs
    
    avg_arrow_time = sum(r["elapsed_seconds"] for r in arrow_results) / num_runs
    avg_arrow_rate = sum(r["documents_per_second"] for r in arrow_results) / num_runs
    
    # Calculate speedup
    speedup = avg_standard_time / avg_arrow_time if avg_arrow_time > 0 else 0
    
    # Print summary
    print("=" * 60)
    print(f"COMPARISON SUMMARY ({num_docs} documents, {num_runs} runs)")
    print("=" * 60)
    print(f"Average standard indexing time: {avg_standard_time:.4f} seconds")
    print(f"Average standard indexing rate: {avg_standard_rate:.2f} documents/second")
    print()
    print(f"Average Arrow indexing time: {avg_arrow_time:.4f} seconds")
    print(f"Average Arrow indexing rate: {avg_arrow_rate:.2f} documents/second")
    print()
    print(f"Arrow vs Standard speedup: {speedup:.2f}x")
    print("=" * 60)
    
    return {
        "standard": {
            "avg_time": avg_standard_time,
            "avg_rate": avg_standard_rate
        },
        "arrow": {
            "avg_time": avg_arrow_time,
            "avg_rate": avg_arrow_rate
        },
        "speedup": speedup
    }

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Benchmark Arrow indexing vs. standard indexing")
    parser.add_argument("--docs", type=int, default=10000, help="Number of documents to index")
    parser.add_argument("--runs", type=int, default=3, help="Number of benchmark runs")
    args = parser.parse_args()
    
    run_comparison(num_docs=args.docs, num_runs=args.runs)