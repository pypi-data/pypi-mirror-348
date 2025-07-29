#!/usr/bin/env python3
"""
Simplified Memory Management Test for Fast Inverted Index
"""

import gc
import time
import random
import string

import fast_inverted_index as fii
from fast_inverted_index import Index, Schema, FieldSchema, QueryNode, QueryExecutionParams

def generate_random_text(word_count: int) -> str:
    """Generate random text with the given number of words."""
    words = []
    for _ in range(word_count):
        word_len = random.randint(3, 8)  # Shorter for speed
        word = ''.join(random.choice(string.ascii_lowercase) for _ in range(word_len))
        words.append(word)
    return ' '.join(words)

def main():
    print("=== Fast Inverted Index Memory Management Test ===")
    
    # Create schema
    print("Creating schema...")
    schema = Schema()
    schema.add_field(FieldSchema.text("title").with_boost(2.0))
    schema.add_field(FieldSchema.text("content"))
    schema.add_field(FieldSchema.keyword("tags").with_boost(1.5))
    schema.set_default_field("content")
    
    # Create index with short TTL for cache
    print("Creating index...")
    index = Index(
        in_memory=True,
        schema=schema,
        cache_size=5000,
        cache_ttl_secs=10  # Very short TTL for testing
    )
    
    # Add some documents
    print("Adding documents...")
    doc_id = 1
    for batch in range(2):
        print(f"Adding batch {batch+1} of documents...")
        for i in range(50):  # Smaller batches
            title = generate_random_text(3)
            content = generate_random_text(30)
            tags = generate_random_text(2)
            
            # Add document
            index.add_document_with_metadata(
                doc_id,
                content,
                {
                    "title": title,
                    "tags": [tag for tag in tags.split()],
                    "category": "test"
                }
            )
            doc_id += 1
    
    # Get and print memory usage
    print("\nMemory usage before cleanup:")
    memory_usage = index.memory_usage()
    for component, size in memory_usage.items():
        print(f"  {component}: {size/1024/1024:.2f} MB")
    
    # Run a simple search query to populate cache
    print("\nRunning a simple search query...")
    results = index.search("the")
    print(f"Search returned {len(results)} results")
    
    # Force garbage collection
    gc.collect()
    
    # Wait for TTL expiration
    print("\nWaiting for cache TTL expiration...")
    time.sleep(15)  # Wait longer than the TTL
    
    # Call memory management function
    print("\nCalling manage_memory()...")
    index.manage_memory()
    
    # Get and print memory usage after cleanup
    print("\nMemory usage after cleanup:")
    memory_usage = index.memory_usage()
    for component, size in memory_usage.items():
        print(f"  {component}: {size/1024/1024:.2f} MB")
    
    # Try to close the index
    print("\nAttempting to close index...")
    try:
        index.close()
        print("Index successfully closed")
    except ValueError as e:
        print(f"Could not close index: {e}")
    
    # Force another garbage collection
    del index
    gc.collect()
    
    print("\nTest completed")

if __name__ == "__main__":
    main()