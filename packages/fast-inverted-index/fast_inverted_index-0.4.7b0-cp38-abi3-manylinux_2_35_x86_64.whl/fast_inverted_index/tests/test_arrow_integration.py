"""
Test suite for Apache Arrow integration with fast-inverted-index.

This module tests all aspects of Arrow integration:
- Functionality: Basic operations work as expected
- Performance: Arrow provides expected performance benefits
- Error handling: Proper errors for invalid inputs
- Edge cases: Empty batches, schema mismatches, etc.
"""

import unittest
import tempfile
import os
import time
import pyarrow as pa
import json
import numpy as np
import fast_inverted_index as fii

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


class TestArrowDataTypes(unittest.TestCase):
    """Test Arrow data type compatibility."""
    
    def test_numeric_types(self):
        """Test handling of numeric data types."""
        # Create batch with various numeric types
        data = [
            {
                "id": 1,
                "int8_val": np.int8(-128),
                "uint8_val": np.uint8(255),
                "int16_val": np.int16(-32768),
                "uint16_val": np.uint16(65535),
                "int32_val": np.int32(-2147483648),
                "uint32_val": np.uint32(4294967295),
                "int64_val": np.int64(-9223372036854775808),
                "uint64_val": np.uint64(18446744073709551615),
                "float32_val": np.float32(1.234),
                "float64_val": np.float64(1.23456789),
                "content": "Numeric data types test"
            }
        ]
        batch = pa.RecordBatch.from_pylist(data)
        
        # Create index
        index = fii.Index.builder().build()
        arrow_index = ArrowIndex(index)
        
        # Add document from batch
        stats = arrow_index.add_documents_from_arrow_batch(
            batch,
            id_field="id",
            content_fields=["content"],
            metadata_fields=["int8_val", "float64_val"]
        )
        
        # Verify document was indexed
        self.assertEqual(stats["documents_indexed"], 1)
        
        # Verify document can be retrieved with metadata
        doc = index.get_document(1)
        self.assertIsNotNone(doc)
        self.assertIn("int8_val", doc)
        self.assertIn("float64_val", doc)
        
    def test_string_types(self):
        """Test handling of string data types."""
        # Create batch with various string types
        data = [
            {
                "id": 1,
                "ascii_string": "ASCII string",
                "unicode_string": "Unicode string with symbols: 😀 🌍 🚀",
                "empty_string": "",
                "null_string": None,
                "content": "String data types test"
            }
        ]
        batch = pa.RecordBatch.from_pylist(data)
        
        # Create index
        index = fii.Index.builder().build()
        arrow_index = ArrowIndex(index)
        
        # Add document from batch
        stats = arrow_index.add_documents_from_arrow_batch(
            batch,
            id_field="id",
            content_fields=["content"],
            metadata_fields=["ascii_string", "unicode_string", "empty_string", "null_string"]
        )
        
        # Verify document was indexed
        self.assertEqual(stats["documents_indexed"], 1)
        
        # Verify metadata was stored correctly
        doc = index.get_document(1)
        self.assertEqual(doc["ascii_string"], "ASCII string")
        self.assertEqual(doc["unicode_string"], "Unicode string with symbols: 😀 🌍 🚀")
        self.assertEqual(doc["empty_string"], "")
        self.assertEqual(doc["null_string"], "None")  # None becomes "None" string
        
    def test_binary_types(self):
        """Test handling of binary data types."""
        # Create batch with binary data
        binary_data = b"\x00\x01\x02\x03\x04"
        data = [
            {
                "id": 1,
                "binary_val": binary_data,
                "content": "Binary data types test"
            }
        ]
        batch = pa.RecordBatch.from_pylist(data)
        
        # Create index
        index = fii.Index.builder().build()
        arrow_index = ArrowIndex(index)
        
        # Add document from batch
        stats = arrow_index.add_documents_from_arrow_batch(
            batch,
            id_field="id",
            content_fields=["content"],
            metadata_fields=["binary_val"]
        )
        
        # Verify document was indexed
        self.assertEqual(stats["documents_indexed"], 1)
        
        # Verify metadata was stored correctly (as string representation)
        doc = index.get_document(1)
        self.assertIn("binary_val", doc)
    
    def test_complex_types(self):
        """Test handling of complex data types (lists, structs)."""
        # Create batch with complex types
        data = [
            {
                "id": 1,
                "list_val": [1, 2, 3, 4, 5],
                "nested_list": [[1, 2], [3, 4]],
                "dict_val": {"key1": "value1", "key2": "value2"},
                "content": "Complex data types test"
            }
        ]
        batch = pa.RecordBatch.from_pylist(data)
        
        # Create index
        index = fii.Index.builder().build()
        arrow_index = ArrowIndex(index)
        
        # Add document from batch
        stats = arrow_index.add_documents_from_arrow_batch(
            batch,
            id_field="id",
            content_fields=["content"],
            metadata_fields=["list_val", "nested_list", "dict_val"]
        )
        
        # Verify document was indexed
        self.assertEqual(stats["documents_indexed"], 1)
        
        # Verify metadata was stored correctly (as string representations)
        doc = index.get_document(1)
        self.assertIn("list_val", doc)
        self.assertIn("nested_list", doc)
        self.assertIn("dict_val", doc)


class TestFunctionalityTests(unittest.TestCase):
    """Test basic functionality of Arrow integration."""
    
    def setUp(self):
        """Set up test environment."""
        # Create a temporary directory for indexes
        self.temp_dir = tempfile.mkdtemp()
        
        # Sample data for testing
        self.data = [
            {
                "id": 1,
                "title": "Arrow Integration",
                "content": "Fast zero-copy data transfer",
                "author": "Alice",
                "tags": ["tech", "data"]
            },
            {
                "id": 2,
                "title": "PyO3 Bindings",
                "content": "Rust and Python interoperability",
                "author": "Bob",
                "tags": ["tech", "programming"]
            },
            {
                "id": 3,
                "title": "Performance Optimization",
                "content": "Bulk document loading for speed",
                "author": "Charlie",
                "tags": ["performance", "data"]
            }
        ]
        
        # Convert tags to strings (as they would be in real usage)
        for doc in self.data:
            doc["tags"] = json.dumps(doc["tags"])
        
        # Create Arrow batch
        self.batch = pa.RecordBatch.from_pylist(self.data)
    
    def tearDown(self):
        """Clean up test environment."""
        # Remove temporary directory and its contents
        for name in os.listdir(self.temp_dir):
            os.remove(os.path.join(self.temp_dir, name))
        os.rmdir(self.temp_dir)
    
    def test_basic_indexing(self):
        """Test basic document indexing via Arrow."""
        # Create index
        index = fii.Index.builder().build()
        arrow_index = ArrowIndex(index)
        
        # Add documents from Arrow batch
        stats = arrow_index.add_documents_from_arrow_batch(
            self.batch,
            id_field="id",
            content_fields=["title", "content"],
            metadata_fields=["author", "tags"]
        )
        
        # Verify all documents were indexed
        self.assertEqual(stats["documents_indexed"], 3)
        
        # Test search
        results = index.search("data")
        self.assertEqual(len(results), 2)  # Should match docs 1 and 3
        
        # Test document retrieval with metadata
        doc = index.get_document(1)
        self.assertEqual(doc["author"], "Alice")
        self.assertEqual(doc["tags"], '["tech", "data"]')
    
    def test_content_field_combinations(self):
        """Test various combinations of content fields."""
        # Create index
        index = fii.Index.builder().build()
        arrow_index = ArrowIndex(index)
        
        # Test with title only
        arrow_index.add_documents_from_arrow_batch(
            self.batch,
            id_field="id",
            content_fields=["title"],
            metadata_fields=None
        )
        
        # Should find documents with "Arrow" in title
        results = index.search("Arrow")
        self.assertEqual(len(results), 1)
        self.assertEqual(results[0]["document_id"], 1)
        
        # Should not find documents with "zero-copy" (only in content)
        results = index.search("zero-copy")
        self.assertEqual(len(results), 0)
        
        # Create new index with content only
        index = fii.Index.builder().build()
        arrow_index = ArrowIndex(index)
        
        arrow_index.add_documents_from_arrow_batch(
            self.batch,
            id_field="id",
            content_fields=["content"],
            metadata_fields=None
        )
        
        # Should find documents with "zero-copy" in content
        results = index.search("zero-copy")
        self.assertEqual(len(results), 1)
        
        # Create new index with both title and content
        index = fii.Index.builder().build()
        arrow_index = ArrowIndex(index)
        
        arrow_index.add_documents_from_arrow_batch(
            self.batch,
            id_field="id",
            content_fields=["title", "content"],
            metadata_fields=None
        )
        
        # Should find documents with either term
        results = index.search("Arrow OR zero-copy")
        self.assertEqual(len(results), 1)
    
    def test_metadata_options(self):
        """Test various metadata field configurations."""
        # Create index with no metadata
        index1 = fii.Index.builder().build()
        arrow_index1 = ArrowIndex(index1)
        
        arrow_index1.add_documents_from_arrow_batch(
            self.batch,
            id_field="id",
            content_fields=["title", "content"],
            metadata_fields=None
        )
        
        # Create index with author metadata only
        index2 = fii.Index.builder().build()
        arrow_index2 = ArrowIndex(index2)
        
        arrow_index2.add_documents_from_arrow_batch(
            self.batch,
            id_field="id",
            content_fields=["title", "content"],
            metadata_fields=["author"]
        )
        
        # Create index with all metadata
        index3 = fii.Index.builder().build()
        arrow_index3 = ArrowIndex(index3)
        
        arrow_index3.add_documents_from_arrow_batch(
            self.batch,
            id_field="id",
            content_fields=["title", "content"],
            metadata_fields=["author", "tags"]
        )
        
        # Verify metadata is stored correctly
        doc1 = index1.get_document(1)
        self.assertNotIn("author", doc1)
        self.assertNotIn("tags", doc1)
        
        doc2 = index2.get_document(1)
        self.assertEqual(doc2["author"], "Alice")
        self.assertNotIn("tags", doc2)
        
        doc3 = index3.get_document(1)
        self.assertEqual(doc3["author"], "Alice")
        self.assertEqual(doc3["tags"], '["tech", "data"]')
    
    def test_persistence(self):
        """Test persistence of indexed Arrow data."""
        index_path = os.path.join(self.temp_dir, "arrow_index")
        
        # Create index with persistence
        index = fii.Index.builder().path(index_path).build()
        arrow_index = ArrowIndex(index)
        
        # Add documents from Arrow batch
        arrow_index.add_documents_from_arrow_batch(
            self.batch,
            id_field="id",
            content_fields=["title", "content"],
            metadata_fields=["author", "tags"]
        )
        
        # Test search immediately
        results = index.search("data")
        self.assertEqual(len(results), 2)
        
        # Close the index
        index.close()
        
        # Reopen the index
        reopened_index = fii.Index.builder().path(index_path).build()
        
        # Test search after reopening
        results = reopened_index.search("data")
        self.assertEqual(len(results), 2)
        
        # Verify metadata is still available
        doc = reopened_index.get_document(1)
        self.assertEqual(doc["author"], "Alice")
        self.assertEqual(doc["tags"], '["tech", "data"]')
        
        # Close the reopened index
        reopened_index.close()


class TestErrorHandling(unittest.TestCase):
    """Test error handling in Arrow integration."""
    
    def test_missing_id_field(self):
        """Test error handling for missing ID field."""
        # Create Arrow batch
        data = [
            {
                "title": "Test Document",
                "content": "Test content"
            }
        ]
        batch = pa.RecordBatch.from_pylist(data)
        
        # Create index
        index = fii.Index.builder().build()
        arrow_index = ArrowIndex(index)
        
        # Attempt to add documents with non-existent ID field
        with self.assertRaises(Exception):
            arrow_index.add_documents_from_arrow_batch(
                batch,
                id_field="id",  # This field doesn't exist
                content_fields=["title", "content"],
                metadata_fields=None
            )
    
    def test_missing_content_fields(self):
        """Test error handling for missing content fields."""
        # Create Arrow batch
        data = [
            {
                "id": 1,
                "title": "Test Document"
            }
        ]
        batch = pa.RecordBatch.from_pylist(data)
        
        # Create index
        index = fii.Index.builder().build()
        arrow_index = ArrowIndex(index)
        
        # Attempt to add documents with non-existent content field
        with self.assertRaises(Exception):
            arrow_index.add_documents_from_arrow_batch(
                batch,
                id_field="id",
                content_fields=["content"],  # This field doesn't exist
                metadata_fields=None
            )
    
    def test_missing_metadata_fields(self):
        """Test error handling for missing metadata fields."""
        # Create Arrow batch
        data = [
            {
                "id": 1,
                "title": "Test Document",
                "content": "Test content"
            }
        ]
        batch = pa.RecordBatch.from_pylist(data)
        
        # Create index
        index = fii.Index.builder().build()
        arrow_index = ArrowIndex(index)
        
        # Add documents with non-existent metadata field
        # This should not fail, but just skip the missing metadata
        stats = arrow_index.add_documents_from_arrow_batch(
            batch,
            id_field="id",
            content_fields=["title", "content"],
            metadata_fields=["author"]  # This field doesn't exist
        )
        
        # Verify document was still indexed
        self.assertEqual(stats["documents_indexed"], 1)
        
        # Verify we can search the document
        results = index.search("test")
        self.assertEqual(len(results), 1)
    
    def test_empty_batch(self):
        """Test handling of empty Arrow batch."""
        # Create empty Arrow batch
        data = []
        batch = pa.RecordBatch.from_pylist(data)
        
        # Create index
        index = fii.Index.builder().build()
        arrow_index = ArrowIndex(index)
        
        # Add empty batch
        stats = arrow_index.add_documents_from_arrow_batch(
            batch,
            id_field="id",
            content_fields=["title", "content"],
            metadata_fields=None
        )
        
        # Verify no documents were indexed
        self.assertEqual(stats["documents_indexed"], 0)
    
    def test_duplicate_ids(self):
        """Test handling of duplicate document IDs."""
        # Create Arrow batch with duplicate IDs
        data = [
            {
                "id": 1,
                "title": "Document 1",
                "content": "First document"
            },
            {
                "id": 1,  # Duplicate ID
                "title": "Document 2",
                "content": "Second document"
            }
        ]
        batch = pa.RecordBatch.from_pylist(data)
        
        # Create index
        index = fii.Index.builder().build()
        arrow_index = ArrowIndex(index)
        
        # Add documents with duplicate IDs
        stats = arrow_index.add_documents_from_arrow_batch(
            batch,
            id_field="id",
            content_fields=["title", "content"],
            metadata_fields=None
        )
        
        # Verify one document was indexed and one failed
        self.assertEqual(stats["documents_indexed"], 1)
        self.assertEqual(stats["errors"], 1)
        
        # Verify the content of the indexed document
        doc = index.get_document(1)
        self.assertTrue("Document 1" in doc["_content"])
        self.assertTrue("First document" in doc["_content"])


class TestPerformanceScaling(unittest.TestCase):
    """Test performance scaling with dataset size."""
    
    def test_scaling_behavior(self):
        """Test how performance scales with dataset size."""
        # Test with different batch sizes
        batch_sizes = [10, 100, 1000]
        
        results = []
        for size in batch_sizes:
            # Generate test data
            data = []
            for i in range(size):
                doc = {
                    "id": i,
                    "title": f"Document {i}",
                    "content": f"This is test document {i} with some additional content to make it more realistic.",
                    "author": "Test Author",
                    "tags": json.dumps(["test", "performance"])
                }
                data.append(doc)
            
            # Create Arrow batch
            batch = pa.RecordBatch.from_pylist(data)
            
            # Create index
            index = fii.Index.builder().build()
            arrow_index = ArrowIndex(index)
            
            # Measure indexing time
            start_time = time.time()
            stats = arrow_index.add_documents_from_arrow_batch(
                batch,
                id_field="id",
                content_fields=["title", "content"],
                metadata_fields=["author", "tags"]
            )
            elapsed_ms = int((time.time() - start_time) * 1000)
            
            # Verify all documents were indexed
            self.assertEqual(stats["documents_indexed"], size)
            
            # Record results
            results.append({
                "batch_size": size,
                "elapsed_ms": elapsed_ms,
                "docs_per_second": size * 1000 / elapsed_ms if elapsed_ms > 0 else 0
            })
        
        # Verify performance scales reasonably
        # Just print results for manual verification - we don't want the test to fail
        # due to performance variations on different machines
        print("\nPerformance scaling results:")
        for result in results:
            print(f"Batch size: {result['batch_size']}, "
                  f"Elapsed: {result['elapsed_ms']}ms, "
                  f"Throughput: {result['docs_per_second']:.2f} docs/sec")


class TestEdgeCases(unittest.TestCase):
    """Test edge cases for Arrow integration."""
    
    def test_large_documents(self):
        """Test indexing of very large documents."""
        # Create a large document (100K words)
        large_content = " ".join(["word"] * 100000)
        
        data = [
            {
                "id": 1,
                "title": "Large Document",
                "content": large_content,
                "author": "Test"
            }
        ]
        batch = pa.RecordBatch.from_pylist(data)
        
        # Create index
        index = fii.Index.builder().build()
        arrow_index = ArrowIndex(index)
        
        # Add large document
        stats = arrow_index.add_documents_from_arrow_batch(
            batch,
            id_field="id",
            content_fields=["title", "content"],
            metadata_fields=["author"]
        )
        
        # Verify document was indexed
        self.assertEqual(stats["documents_indexed"], 1)
        
        # Test search
        results = index.search("word")
        self.assertEqual(len(results), 1)
    
    def test_many_fields(self):
        """Test batch with many fields."""
        # Create document with many fields
        doc = {"id": 1}
        for i in range(100):
            doc[f"field_{i}"] = f"value_{i}"
        
        data = [doc]
        batch = pa.RecordBatch.from_pylist(data)
        
        # Create index
        index = fii.Index.builder().build()
        arrow_index = ArrowIndex(index)
        
        # Select a subset of fields for content and metadata
        content_fields = ["field_0", "field_1", "field_2"]
        metadata_fields = [f"field_{i}" for i in range(3, 10)]
        
        # Add document
        stats = arrow_index.add_documents_from_arrow_batch(
            batch,
            id_field="id",
            content_fields=content_fields,
            metadata_fields=metadata_fields
        )
        
        # Verify document was indexed
        self.assertEqual(stats["documents_indexed"], 1)
        
        # Test search
        results = index.search("value_0")
        self.assertEqual(len(results), 1)
        
        # Check metadata
        doc = index.get_document(1)
        for i in range(3, 10):
            self.assertEqual(doc[f"field_{i}"], f"value_{i}")


if __name__ == "__main__":
    unittest.main()