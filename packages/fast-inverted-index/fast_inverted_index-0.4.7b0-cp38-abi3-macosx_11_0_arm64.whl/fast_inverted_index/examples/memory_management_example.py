#!/usr/bin/env python3
"""
Memory Management Example for Fast Inverted Index

This example demonstrates how to use the memory management features
to keep memory usage under control in long-running applications.
"""

import gc
import time
import random
import string
import tracemalloc
from typing import List, Dict, Tuple

import fast_inverted_index as fii
from fast_inverted_index import Index, Schema, FieldSchema, QueryNode, QueryExecutionParams

def generate_random_text(word_count: int) -> str:
    """Generate random text with the specified number of words."""
    words = []
    for _ in range(word_count):
        word_len = random.randint(3, 12)
        word = ''.join(random.choice(string.ascii_lowercase) for _ in range(word_len))
        words.append(word)
    return ' '.join(words)

def print_memory_stats(index: Index) -> None:
    """Print memory usage statistics for an index."""
    memory_usage = index.memory_usage()
    
    print("Memory Usage:")
    for component, size in memory_usage.items():
        print(f"  {component}: {size/1024/1024:.2f} MB")

def test_memory_management() -> None:
    """Demonstrate memory management features by adding documents and running queries."""
    
    # Start memory tracking
    tracemalloc.start()
    
    # Create a schema with multiple fields
    schema = fii.Schema()
    schema.add_field(fii.FieldSchema.text("title").with_boost(2.0))
    schema.add_field(fii.FieldSchema.text("content"))
    schema.add_field(fii.FieldSchema.keyword("tags").with_boost(1.5))
    schema.set_default_field("content")
    
    # Create an in-memory index with a specific cache TTL
    index = Index(
        in_memory=True,
        schema=schema,
        cache_size=10000,
        cache_ttl_secs=30  # Short TTL for demonstration
    )
    
    print("Created index")
    
    # Add documents in batches
    doc_id = 1
    for batch in range(5):
        print(f"\nAdding batch {batch+1} of documents...")
        
        for i in range(100):
            title = generate_random_text(5)
            content = generate_random_text(100)
            tags = generate_random_text(3)
            
            # Add document with all fields
            index.add_document_with_metadata(
                doc_id,
                content,
                {
                    "title": title,
                    "tags": [t for t in tags.split()],
                    "category": "test"
                }
            )
            doc_id += 1
        
        # Print memory usage after each batch
        print_memory_stats(index)
        
        # Run some queries
        content = generate_random_text(500)
        terms = content.split()
        
        print("\nRunning queries...")
        for i in range(20):
            # Create queries of varying complexity
            if i % 4 == 0:
                term = random.choice(terms)
                query = QueryNode.term("content", term)
            elif i % 4 == 1:
                term1, term2 = random.sample(terms, 2)
                query = QueryNode.AND([
                    QueryNode.term("content", term1),
                    QueryNode.term("content", term2)
                ])
            else:
                term1, term2, term3 = random.sample(terms, 3)
                query = QueryNode.OR([
                    QueryNode.term("content", term1),
                    QueryNode.term("content", term2),
                    QueryNode.term("content", term3)
                ])
            
            # Execute the query
            params = QueryExecutionParams(
                scoring_algorithm="bm25",
                limit=50,
                explain=True  # Enable explanations to test memory usage
            )
            result = index.execute_query(query, params)
        
        # Print memory usage after queries
        print("\nMemory usage after queries:")
        print_memory_stats(index)
        
        # Clean up memory
        print("\nCleaning up memory...")
        index.manage_memory()
        gc.collect()
        
        # Print memory usage after cleanup
        print("\nMemory usage after cleanup:")
        print_memory_stats(index)
        
        # Short delay to allow TTL expirations
        print("\nWaiting for cache TTL expiration...")
        time.sleep(35)  # > cache_ttl_secs
        
        # Manage memory again
        index.manage_memory()
        
        # Print memory usage after TTL expiration
        print("\nMemory usage after TTL expiration and memory management:")
        print_memory_stats(index)
    
    # Get current memory snapshot
    snapshot = tracemalloc.take_snapshot()
    top_stats = snapshot.statistics('lineno')
    
    print("\nTop 10 memory consumers before cleanup:")
    for stat in top_stats[:10]:
        print(f"{stat.count} objects: {stat.size / 1024:.1f} KB")
        print(f"  {stat.traceback[0].filename}:{stat.traceback[0].lineno}")
    
    # Final explicit cleanup
    print("\nPerforming final cleanup...")
    index.manage_memory()
    
    try:
        index.close()
        print("Index successfully closed")
    except ValueError as e:
        print(f"Could not close index: {e}")
        print("This often happens if there are still references to query results or other index objects")
        
    # Force a full garbage collection
    del index
    gc.collect()
    
    # Stop tracking
    tracemalloc.stop()
    print("\nMemory tracking stopped")

if __name__ == "__main__":
    test_memory_management()