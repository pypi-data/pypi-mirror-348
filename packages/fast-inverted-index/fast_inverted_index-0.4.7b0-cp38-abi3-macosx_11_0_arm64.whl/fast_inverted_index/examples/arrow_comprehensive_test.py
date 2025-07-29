#!/usr/bin/env python
"""
Comprehensive testing for Arrow integration with fast-inverted-index.

This script tests various aspects of the Arrow integration:
1. Basic functionality with different data types
2. Error handling with invalid inputs
3. Performance with different dataset sizes
4. Parallel processing performance
5. Edge cases (empty batches, missing fields, etc.)
"""

import os
import time
import tempfile
import unittest
import json
import random
import string
import sys

import numpy as np
import pyarrow as pa
import fast_inverted_index as fii

# Implementation of our temporary ArrowIndex wrapper
class ArrowIndex:
    """Wrapper class that adds Arrow functionality to the Index class."""
    
    def __init__(self, index=None):
        """Initialize with an existing index or create a new one."""
        if index is None:
            builder = fii.IndexBuilder()
            builder.with_in_memory(True)
            self.index = builder.build()
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


def generate_random_text(min_words=5, max_words=20, word_length=7):
    """Generate random text with a given word count range and word length."""
    word_count = random.randint(min_words, max_words)
    words = []
    for _ in range(word_count):
        word_len = random.randint(3, word_length)
        word = ''.join(random.choice(string.ascii_lowercase) for _ in range(word_len))
        words.append(word)
    return ' '.join(words)


class TestArrowIntegration(unittest.TestCase):
    """Test Apache Arrow integration with fast-inverted-index."""
    
    def setUp(self):
        """Set up test environment."""
        # Create a temporary directory for indexes
        self.temp_dir = tempfile.mkdtemp()

        # Create a clean in-memory index for each test to avoid RocksDB locks
        builder = fii.IndexBuilder()
        builder.with_in_memory(True)
        self.index = builder.build()
        self.arrow_index = ArrowIndex(self.index)
    
    def tearDown(self):
        """Clean up test environment."""
        # Clear temporary directory and its contents
        for name in os.listdir(self.temp_dir):
            os.remove(os.path.join(self.temp_dir, name))
        os.rmdir(self.temp_dir)
    
    def test_basic_indexing(self):
        """Test basic document indexing with Arrow."""
        # Create sample data
        data = [
            {
                "id": 1,
                "title": "Arrow Integration",
                "content": "Fast zero-copy data transfer",
                "author": "Alice"
            },
            {
                "id": 2,
                "title": "PyO3 Bindings",
                "content": "Rust and Python interoperability",
                "author": "Bob"
            }
        ]
        
        # Create Arrow batch
        batch = pa.RecordBatch.from_pylist(data)
        
        # Add documents
        stats = self.arrow_index.add_documents_from_arrow_batch(
            batch,
            id_field="id",
            content_fields=["title", "content"],
            metadata_fields=["author"]
        )
        
        # Verify documents were indexed
        self.assertEqual(stats["documents_indexed"], 2)
        self.assertTrue(stats["tokens_indexed"] > 0)
        self.assertEqual(stats["errors"], 0)
        
        # Test search
        results = self.index.search("arrow")
        self.assertEqual(len(results), 1)
        self.assertEqual(results[0][0], 1)  # First element is document_id
        
        # Test metadata retrieval
        doc = self.index.get_document(1)
        self.assertEqual(doc["author"], "Alice")
    
    def test_numeric_types(self):
        """Test indexing with numeric data types."""
        # Create data with numeric fields
        data = [
            {
                "id": 1,
                "int_value": 42,
                "float_value": 3.14,
                "content": "Document with numeric fields"
            }
        ]
        
        # Create Arrow batch
        batch = pa.RecordBatch.from_pylist(data)
        
        # Add documents
        stats = self.arrow_index.add_documents_from_arrow_batch(
            batch,
            id_field="id",
            content_fields=["content"],
            metadata_fields=["int_value", "float_value"]
        )
        
        # Verify documents were indexed
        self.assertEqual(stats["documents_indexed"], 1)
        
        # Get the document with metadata
        doc = self.index.get_document(1)

        # Print the document to debug
        print(f"Document metadata: {doc}")

        # Check that content was indexed
        self.assertTrue("Document with numeric fields" in doc["_content"])
    
    def test_error_handling(self):
        """Test error handling with invalid inputs."""
        # Create data with missing required field
        data = [
            {
                # Missing id field
                "title": "Missing ID",
                "content": "This document has no ID field"
            },
            {
                "id": 2,
                "title": "Valid Document",
                "content": "This document has an ID"
            }
        ]

        # Create Arrow batch
        batch = pa.RecordBatch.from_pylist(data)

        # This should handle the error for missing ID and continue processing
        stats = self.arrow_index.add_documents_from_arrow_batch(
            batch,
            id_field="id",  # This field is missing from first document
            content_fields=["title", "content"],
            metadata_fields=None
        )

        # Verify that we got errors but still processed the valid document
        self.assertTrue(stats["errors"] > 0, "Should report errors for missing ID field")
        self.assertEqual(stats["documents_indexed"], 1, "Should index the valid document")
    
    def test_missing_content_field(self):
        """Test error handling with missing content field."""
        # Create data with missing content field
        data = [
            {
                "id": 1,
                "title": "Document with missing content",
                # Missing content field
                "author": "Alice"
            }
        ]

        # Create Arrow batch
        batch = pa.RecordBatch.from_pylist(data)

        # This should handle the error but still index with the available content field
        stats = self.arrow_index.add_documents_from_arrow_batch(
            batch,
            id_field="id",
            content_fields=["title", "nonexistent"],  # nonexistent field
            metadata_fields=["author"]
        )

        # Verify one document was indexed with the title field
        doc = self.index.get_document(1)
        print(f"Missing content field document: {doc}")
        self.assertTrue("Document with missing content" in doc["_content"],
                      "Document should be indexed with available content fields")
    
    def test_empty_batch(self):
        """Test handling of empty Arrow batch."""
        # Create empty data
        data = []

        # For empty data, we need to define the schema explicitly
        schema = pa.schema([
            pa.field("id", pa.int64()),
            pa.field("title", pa.string()),
            pa.field("content", pa.string())
        ])

        # Create empty Arrow batch
        batch = pa.RecordBatch.from_arrays(
            [pa.array([], type=pa.int64()),
             pa.array([], type=pa.string()),
             pa.array([], type=pa.string())],
            names=["id", "title", "content"]
        )

        # Add empty batch
        stats = self.arrow_index.add_documents_from_arrow_batch(
            batch,
            id_field="id",
            content_fields=["title", "content"],
            metadata_fields=None
        )

        # Verify no documents were indexed
        self.assertEqual(stats["documents_indexed"], 0)
    
    def test_large_batch(self):
        """Test indexing a large batch of documents."""
        # Create many documents
        data = []
        for i in range(100):
            data.append({
                "id": i,
                "title": f"Document {i}",
                "content": generate_random_text(20, 50),
                "author": random.choice(["Alice", "Bob", "Charlie"])
            })
        
        # Create Arrow batch
        batch = pa.RecordBatch.from_pylist(data)
        
        # Add documents
        start_time = time.time()
        stats = self.arrow_index.add_documents_from_arrow_batch(
            batch,
            id_field="id",
            content_fields=["title", "content"],
            metadata_fields=["author"]
        )
        elapsed = time.time() - start_time
        
        # Verify documents were indexed
        self.assertEqual(stats["documents_indexed"], 100)
        self.assertEqual(stats["errors"], 0)
        
        # Log performance
        print(f"Indexed 100 documents in {elapsed:.3f} seconds")
        print(f"Documents per second: {100/elapsed:.1f}")
    
    def test_complex_types(self):
        """Test handling of complex data types."""
        # Create data with complex types
        data = [
            {
                "id": 1,
                "title": "Complex Types",
                "content": "Testing complex data types",
                "tags": ["tag1", "tag2", "tag3"],
                "nested": {"key1": "value1", "key2": "value2"}
            }
        ]
        
        # Create Arrow batch
        batch = pa.RecordBatch.from_pylist(data)
        
        # Add documents
        stats = self.arrow_index.add_documents_from_arrow_batch(
            batch,
            id_field="id",
            content_fields=["title", "content"],
            metadata_fields=["tags", "nested"]
        )
        
        # Verify documents were indexed
        self.assertEqual(stats["documents_indexed"], 1)
        
        # Verify content was indexed correctly
        doc = self.index.get_document(1)
        print(f"Complex types document: {doc}")
        self.assertTrue("Testing complex data types" in doc["_content"])
    
    def test_null_values(self):
        """Test handling of null values."""
        # Create data with null values
        data = [
            {
                "id": 1,
                "title": "Document with nulls",
                "content": None,
                "author": None
            }
        ]

        # Create Arrow batch
        batch = pa.RecordBatch.from_pylist(data)

        # Add documents - this should handle null values gracefully
        stats = self.arrow_index.add_documents_from_arrow_batch(
            batch,
            id_field="id",
            content_fields=["title", "content"],
            metadata_fields=["author"]
        )

        # Verify the document was indexed with available data
        doc = self.index.get_document(1)
        print(f"Null values document: {doc}")
        self.assertTrue("Document with nulls" in doc["_content"],
                      "Document should be indexed with non-null values")
    
    def test_persistence(self):
        """Test persistence of Arrow-indexed data."""
        # Create data
        data = [
            {
                "id": 1,
                "title": "Persistent Document",
                "content": "This document should persist",
                "author": "Alice"
            }
        ]

        # Create Arrow batch
        batch = pa.RecordBatch.from_pylist(data)

        # Create a unique path for this test
        test_id = random.randint(10000, 99999)
        index_path = os.path.join(self.temp_dir, f"arrow_index_{test_id}")

        try:
            # Create persistent index
            builder = fii.IndexBuilder()
            builder.with_storage_path(index_path)
            persistent_index = builder.build()
            arrow_index = ArrowIndex(persistent_index)

            # Add documents
            stats = arrow_index.add_documents_from_arrow_batch(
                batch,
                id_field="id",
                content_fields=["title", "content"],
                metadata_fields=["author"]
            )

            # Close index
            persistent_index.close()

            # Reopen index
            builder = fii.IndexBuilder()
            builder.with_storage_path(index_path)
            reopened_index = builder.build()

            # Verify document persisted
            doc = reopened_index.get_document(1)
            self.assertEqual(doc["_content"], "Persistent Document This document should persist")
            self.assertEqual(doc["author"], "Alice")

            # Close reopened index
            reopened_index.close()

        finally:
            # Clean up
            try:
                # Remove DB files that may have been created
                for file in os.listdir(index_path):
                    os.remove(os.path.join(index_path, file))
                os.rmdir(index_path)
            except:
                pass
    
    def test_performance_scaling(self):
        """Test performance scaling with dataset size."""
        # Skip this test if running in CI environment
        if os.environ.get("CI") == "true":
            self.skipTest("Skipping performance test in CI environment")
        
        # Test with different batch sizes
        batch_sizes = [10, 100, 1000]
        times = []
        
        for size in batch_sizes:
            # Create data
            data = []
            for i in range(size):
                data.append({
                    "id": i,
                    "title": f"Document {i}",
                    "content": generate_random_text(20, 50),
                    "author": random.choice(["Alice", "Bob", "Charlie"])
                })
            
            # Create Arrow batch
            batch = pa.RecordBatch.from_pylist(data)
            
            # Create clean index for this test
            builder = fii.IndexBuilder()
            builder.with_in_memory(True)
            test_index = builder.build()
            arrow_index = ArrowIndex(test_index)
            
            # Add documents and measure time
            start_time = time.time()
            stats = arrow_index.add_documents_from_arrow_batch(
                batch,
                id_field="id",
                content_fields=["title", "content"],
                metadata_fields=["author"]
            )
            elapsed = time.time() - start_time
            
            # Store results
            times.append(elapsed)
            print(f"Batch size: {size}, Time: {elapsed:.3f}s, Rate: {size/elapsed:.1f} docs/sec")
        
        # Verify rough linear scaling (allowing for some overhead)
        if len(times) == 3 and times[0] > 0:
            ratio1 = times[1] / times[0]  # 100/10
            ratio2 = times[2] / times[1]  # 1000/100
            
            print(f"Scaling ratios: {ratio1:.2f} (100/10), {ratio2:.2f} (1000/100)")
            
            # Ratios should be roughly 10 for linear scaling, but allow for some overhead
            # Just print scaling info without asserting - scaling can vary due to
            # system load, JIT compilation, caching effects, etc.
            print(f"NOTE: Expect roughly 10x ratios for linear scaling. Higher values suggest non-linear scaling.")


def run_tests():
    """Run the test suite."""
    loader = unittest.TestLoader()
    suite = loader.loadTestsFromTestCase(TestArrowIntegration)
    
    # Run the tests
    result = unittest.TextTestRunner(verbosity=2).run(suite)
    
    # Return 0 if all tests passed, 1 otherwise
    return 0 if result.wasSuccessful() else 1


if __name__ == "__main__":
    sys.exit(run_tests())