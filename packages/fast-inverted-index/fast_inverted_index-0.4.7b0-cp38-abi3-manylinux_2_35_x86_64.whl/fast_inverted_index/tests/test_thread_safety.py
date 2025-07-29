"""
Tests for thread safety in the Fast Inverted Index
"""

import unittest
import concurrent.futures
import random
import string
import threading
import time

from fast_inverted_index import Index, Schema, FieldSchema

def generate_random_text(word_count: int) -> str:
    """Generate random text with the given number of words."""
    words = []
    for _ in range(word_count):
        word_len = random.randint(3, 8)
        word = ''.join(random.choice(string.ascii_lowercase) for _ in range(word_len))
        words.append(word)
    return ' '.join(words)

class ThreadSafetyTest(unittest.TestCase):
    def setUp(self):
        # Create schema
        self.schema = Schema()
        self.schema.add_field(FieldSchema.text("title").with_boost(2.0))
        self.schema.add_field(FieldSchema.text("content"))
        self.schema.add_field(FieldSchema.keyword("tags").with_boost(1.5))
        self.schema.set_default_field("content")
        
        # Create index
        self.index = Index(
            in_memory=True,
            schema=self.schema,
            cache_size=5000,
            cache_ttl_secs=60
        )
        
        # Add some initial documents
        for doc_id in range(1, 21):
            title = generate_random_text(3)
            content = generate_random_text(20)
            tags = generate_random_text(2)
            
            self.index.add_document_with_metadata(
                doc_id,
                content,
                {
                    "title": title,
                    "tags": [tag for tag in tags.split()],
                    "category": "test"
                }
            )
    
    def tearDown(self):
        # Ensure the index is closed
        try:
            self.index.close()
        except:
            pass
    
    def test_concurrent_add_and_search(self):
        """Test adding and searching documents concurrently from multiple threads."""
        
        def add_document(doc_id):
            content = generate_random_text(30)
            metadata = {
                "title": generate_random_text(3),
                "tags": [generate_random_text(1) for _ in range(3)],
                "category": "test"
            }
            self.index.add_document_with_metadata(doc_id, content, metadata)
            return doc_id
        
        def search_index(term):
            results = self.index.search(term)
            return results
        
        def remove_document(doc_id):
            self.index.remove_document(doc_id)
            return doc_id
        
        # Track exceptions that occur in threads
        exceptions = []
        
        # Create a list of futures for tracking operations
        with concurrent.futures.ThreadPoolExecutor(max_workers=8) as executor:
            futures = []
            
            # Add documents (21-40)
            for doc_id in range(21, 41):
                futures.append(executor.submit(add_document, doc_id))
            
            # Remove some documents (1-5)
            for doc_id in range(1, 6):
                futures.append(executor.submit(remove_document, doc_id))
            
            # Search operations with random terms
            search_terms = [generate_random_text(1) for _ in range(10)]
            for term in search_terms:
                futures.append(executor.submit(search_index, term))
            
            # Wait for all operations to complete
            for future in concurrent.futures.as_completed(futures):
                try:
                    future.result()
                except Exception as e:
                    exceptions.append(e)
        
        # Assert no exceptions occurred during concurrent operations
        self.assertEqual(len(exceptions), 0, f"Exceptions occurred: {exceptions}")
        
        # Verify expected state after operations
        # Documents 6-40 should exist, 1-5 should be removed
        for doc_id in range(1, 6):
            with self.assertRaises(Exception):
                self.index.get_document(doc_id)
                
        for doc_id in range(6, 41):
            doc = self.index.get_document(doc_id)
            self.assertIsNotNone(doc)
    
    def test_stress_concurrent_operations(self):
        """Stress test with many concurrent operations."""
        operation_count = 200
        num_threads = 10
        
        def random_operation():
            operation = random.choice(["add", "search", "remove", "get"])
            
            if operation == "add":
                doc_id = random.randint(100, 1000)
                content = generate_random_text(10)
                try:
                    self.index.add_document(doc_id, content)
                except Exception as e:
                    # Document might already exist, which is okay
                    pass
                
            elif operation == "search":
                term = generate_random_text(1)
                try:
                    self.index.search(term)
                except Exception as e:
                    return e
                    
            elif operation == "remove":
                doc_id = random.randint(1, 50)  # Remove only from a limited set
                try:
                    self.index.remove_document(doc_id)
                except Exception as e:
                    # Document might not exist, which is okay
                    pass
                
            elif operation == "get":
                doc_id = random.randint(1, 50)
                try:
                    self.index.get_document(doc_id)
                except Exception as e:
                    # Document might not exist, which is okay
                    pass
            
            return None
        
        # Run operations concurrently
        exceptions = []
        with concurrent.futures.ThreadPoolExecutor(max_workers=num_threads) as executor:
            futures = []
            
            for _ in range(operation_count):
                futures.append(executor.submit(random_operation))
            
            for future in concurrent.futures.as_completed(futures):
                result = future.result()
                if result is not None:
                    exceptions.append(result)
        
        # There might be expected exceptions from trying to get/remove
        # documents that don't exist. We're mostly checking that the
        # library doesn't crash or corrupt data.
        
        # Verify the index is still functioning
        try:
            # Add a final document
            final_doc_id = 9999
            self.index.add_document(final_doc_id, "final test document")
            
            # Verify we can retrieve it
            doc = self.index.get_document(final_doc_id)
            self.assertIsNotNone(doc)
            
            # Verify search works
            results = self.index.search("final")
            self.assertTrue(len(results) > 0)
            
        except Exception as e:
            self.fail(f"Index is not functioning after stress test: {e}")

if __name__ == "__main__":
    unittest.main()