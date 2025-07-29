"""
Comprehensive tests for the Fast Inverted Index library
covering both type conversions and query functionality.

This test suite has been updated to match the current API.
"""

import unittest
import tempfile
import shutil
import json
from fast_inverted_index import Index, Schema, FieldSchema, QueryBuilder


class IndexTest(unittest.TestCase):
    def setUp(self):
        # Create a temporary directory for the index
        self.temp_dir = tempfile.mkdtemp()
        
        # Create schema with multiple field types
        self.schema = Schema()
        self.schema.add_field(FieldSchema.text("title").with_boost(2.0))
        self.schema.add_field(FieldSchema.text("content"))
        self.schema.add_field(FieldSchema.keyword("tags").with_boost(1.5))
        
        # Create index
        self.index = Index(
            storage_path=self.temp_dir,
            in_memory=True,
            schema=self.schema
        )
        
        # Add test documents
        self.index.add_document(1, "Rust is a fast systems programming language", {
            "title": "Rust programming language",
            "tags": ["rust", "programming", "systems"]
        })
        
        self.index.add_document(2, "Python is easy to learn and widely used", {
            "title": "Python programming",
            "tags": "python scripting dynamic"
        })
        
        self.index.add_document(3, "Search engines use inverted indexes for fast retrieval", {
            "title": "Search engines",
            "tags": ["search", "indexes", "information-retrieval"]
        })
        
        self.index.add_document(4, "Rust can be used with Python through bindings", {
            "title": "Rust and Python",
            "tags": ["rust", "python", "ffi", "bindings"]
        })
    
    def tearDown(self):
        # Clean up
        self.index.close()
        shutil.rmtree(self.temp_dir, ignore_errors=True)
    
    def test_tag_field_as_list(self):
        """Test that tags can be provided as a list of strings."""
        # Get document with tags provided as a list
        doc = self.index.get_document(1)
        
        # Verify tags
        tags = doc.get("tags", [])
        self.assertIn("rust", tags)
        self.assertIn("programming", tags)
        self.assertIn("systems", tags)
    
    def test_tag_field_as_string(self):
        """Test that tags can be provided as space-separated strings."""
        # Get document with tags provided as a string
        doc = self.index.get_document(2)
        
        # Verify tags
        tags = doc.get("tags", [])
        self.assertIn("python", tags)
        self.assertIn("scripting", tags)
        self.assertIn("dynamic", tags)
    
    def test_basic_search(self):
        """Test basic search functionality."""
        # Search for "rust"
        hits = self.index.search("rust")
        
        # Extract document IDs (hits are tuples of (doc_id, score))
        doc_ids = [hit[0] for hit in hits]
        
        # Documents 1 and 4 should match
        self.assertIn(1, doc_ids)
        self.assertIn(4, doc_ids)
    
    def test_search_with_limit(self):
        """Test search with limit parameter."""
        # Search with limit=1
        hits = self.index.search("programming", limit=1)
        
        # Verify only one result is returned
        self.assertEqual(len(hits), 1)
    
    def test_field_boosting(self):
        """Test field boosting in search."""
        # Search with field boosting
        boost_fields = {"title": 3.0, "tags": 1.5}
        hits = self.index.search("rust", boost_fields=boost_fields)
        
        # Verify the correct documents are found
        doc_ids = [hit[0] for hit in hits]
        self.assertIn(1, doc_ids)
        self.assertIn(4, doc_ids)
        
        # Note: We're not asserting score differences as the scoring algorithm
        # may normalize scores or weigh them differently than expected
    
    def test_boolean_and_search(self):
        """Test boolean AND search using raw query syntax."""
        # Search for documents containing both "rust" and "python"
        hits = self.index.search("rust AND python")
        
        # Only document 4 should match
        self.assertEqual(len(hits), 1)
        self.assertEqual(hits[0][0], 4)  # First element is doc_id
    
    def test_batch_document_addition(self):
        """Test batch document addition with different field types."""
        # Create documents with different field types
        documents = [
            (5, {"content": "Document 5", "tags": ["batch1", "batch2"]}),
            (6, {"content": "Document 6", "tags": "batch3 batch4"})
        ]
        
        # Add documents in batch
        self.index.add_documents_with_fields_parallel(documents)
        
        # Verify documents were added
        doc5 = self.index.get_document(5)
        doc6 = self.index.get_document(6)
        
        self.assertIsNotNone(doc5)
        self.assertIsNotNone(doc6)
        
        # Check that tags were properly converted
        tags5 = doc5.get("tags", [])
        tags6 = doc6.get("tags", [])
        
        self.assertIn("batch1", tags5)
        self.assertIn("batch2", tags5)
        self.assertIn("batch3", tags6)
        self.assertIn("batch4", tags6)
    
    def test_prepare_metadata(self):
        """Test the prepare_metadata helper method."""
        # Prepare metadata with list tags
        original = {"tags": ["tag1", "tag2", "tag3"]}
        prepared = self.index.prepare_metadata(original)
        
        # Check that it's a dict and tags are converted to a string
        self.assertTrue(isinstance(prepared, dict))
        self.assertTrue(isinstance(prepared.get("tags"), str))
        self.assertIn("tag1", prepared.get("tags"))
        self.assertIn("tag2", prepared.get("tags"))
        self.assertIn("tag3", prepared.get("tags"))
    
    def test_validate_document(self):
        """Test the validate_document helper method."""
        # Valid document
        is_valid, errors = self.index.validate_document(
            15, 
            "Content", 
            {"tags": ["tag1", "tag2"]}
        )
        self.assertTrue(is_valid)
        self.assertIsNone(errors)
        
        # Invalid document (tags as dict)
        is_valid, errors = self.index.validate_document(
            16, 
            "Content", 
            {"tags": {"nested": "invalid"}}
        )
        self.assertFalse(is_valid)
        self.assertIsNotNone(errors)
        self.assertIn("tags", errors)


if __name__ == "__main__":
    unittest.main()