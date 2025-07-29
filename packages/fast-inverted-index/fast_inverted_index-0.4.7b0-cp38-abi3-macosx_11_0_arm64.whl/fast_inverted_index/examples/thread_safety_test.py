#!/usr/bin/env python3
"""
Thread Safety Test for Fast Inverted Index
This tests the thread safety of our index implementation by concurrently performing
operations from multiple threads.
"""

import concurrent.futures
import random
import string
import time
from typing import Dict, List, Tuple

import fast_inverted_index as fii
from fast_inverted_index import Index, Schema, FieldSchema, QueryNode, QueryExecutionParams

def generate_random_text(word_count: int) -> str:
    """Generate random text with the given number of words."""
    words = []
    for _ in range(word_count):
        word_len = random.randint(3, 8)
        word = ''.join(random.choice(string.ascii_lowercase) for _ in range(word_len))
        words.append(word)
    return ' '.join(words)

def add_document(index: Index, doc_id: int) -> None:
    """Add a document to the index."""
    title = generate_random_text(3)
    content = generate_random_text(30)
    tags = generate_random_text(2)
    
    try:
        index.add_document_with_metadata(
            doc_id,
            content,
            {
                "title": title,
                "tags": [tag for tag in tags.split()],
                "category": "test"
            }
        )
        print(f"Added document {doc_id}")
    except Exception as e:
        print(f"Error adding document {doc_id}: {e}")

def search_index(index: Index, term: str) -> List[Tuple[int, float]]:
    """Search the index for the given term."""
    try:
        results = index.search(term)
        print(f"Search for '{term}' returned {len(results)} results")
        return results
    except Exception as e:
        print(f"Error searching for '{term}': {e}")
        return []

def update_document(index: Index, doc_id: int) -> None:
    """Update a document in the index."""
    try:
        new_content = generate_random_text(40)
        index.update_document(doc_id, new_content)
        print(f"Updated document {doc_id}")
    except Exception as e:
        print(f"Error updating document {doc_id}: {e}")

def remove_document(index: Index, doc_id: int) -> None:
    """Remove a document from the index."""
    try:
        index.remove_document(doc_id)
        print(f"Removed document {doc_id}")
    except Exception as e:
        print(f"Error removing document {doc_id}: {e}")

def main():
    print("=== Fast Inverted Index Thread Safety Test ===")
    
    # Create schema
    print("Creating schema...")
    schema = Schema()
    schema.add_field(FieldSchema.text("title").with_boost(2.0))
    schema.add_field(FieldSchema.text("content"))
    schema.add_field(FieldSchema.keyword("tags").with_boost(1.5))
    schema.set_default_field("content")
    
    # Create index
    print("Creating index...")
    index = Index(
        in_memory=True,
        schema=schema,
        cache_size=5000,
        cache_ttl_secs=60
    )
    
    # Add initial documents
    print("Adding initial documents...")
    doc_ids = list(range(1, 51))
    for doc_id in doc_ids:
        add_document(index, doc_id)
    
    # Test concurrent operations
    print("\nTesting concurrent operations...")
    with concurrent.futures.ThreadPoolExecutor(max_workers=8) as executor:
        # Mix of document additions, updates, removals, and searches
        futures = []
        
        # Add new documents
        for doc_id in range(51, 101):
            futures.append(executor.submit(add_document, index, doc_id))
        
        # Update existing documents
        for doc_id in random.sample(doc_ids, 10):
            futures.append(executor.submit(update_document, index, doc_id))
        
        # Remove some documents
        for doc_id in random.sample(doc_ids, 5):
            futures.append(executor.submit(remove_document, index, doc_id))
        
        # Perform searches
        search_terms = [generate_random_text(1) for _ in range(20)]
        for term in search_terms:
            futures.append(executor.submit(search_index, index, term))
        
        # Wait for all operations to complete
        concurrent.futures.wait(futures)
    
    # Verify final state
    print("\nVerifying final state...")
    memory_usage = index.memory_usage()
    for component, size in memory_usage.items():
        print(f"  {component}: {size/1024/1024:.2f} MB")
    
    # Optimize index
    print("\nOptimizing index...")
    index.optimize()
    
    # Close index
    print("\nClosing index...")
    index.close()
    
    print("\nThread safety test completed successfully!")

if __name__ == "__main__":
    main()