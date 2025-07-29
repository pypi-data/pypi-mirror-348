"""
Tests for type conversion in the Fast Inverted Index
"""

import unittest
import tempfile
import shutil
import time
from fast_inverted_index import Index, Schema, FieldSchema

class TypeConversionTest(unittest.TestCase):
    def setUp(self):
        # Create a temporary directory for the index
        self.temp_dir = tempfile.mkdtemp()
        
        # Create schema
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
    
    def tearDown(self):
        # Clean up
        self.index.close()
        shutil.rmtree(self.temp_dir, ignore_errors=True)
    
    def test_tags_as_list(self):
        """Test that tags can be provided as a list of strings."""
        try:
            # Add document with tags as a list
            self.index.add_document(
                1, 
                "Sample content", 
                {
                    "title": "Document with list tags",
                    "tags": ["tag1", "tag2", "tag3"]
                }
            )
            
            # If we get here, no exception was raised
            doc = self.index.get_document(1)
            self.assertIsNotNone(doc)
            self.assertIn("tag1", doc.get("tags", ""))
            self.assertIn("tag2", doc.get("tags", ""))
            self.assertIn("tag3", doc.get("tags", ""))
        except Exception as e:
            self.fail(f"add_document with list tags raised exception: {e}")
    
    def test_tags_as_string(self):
        """Test that tags can be provided as a space-separated string."""
        try:
            # Add document with tags as a string
            self.index.add_document(
                2, 
                "Sample content", 
                {
                    "title": "Document with string tags",
                    "tags": "tag1 tag2 tag3"
                }
            )
            
            # If we get here, no exception was raised
            doc = self.index.get_document(2)
            self.assertIsNotNone(doc)
            self.assertIn("tag1", doc.get("tags", ""))
            self.assertIn("tag2", doc.get("tags", ""))
            self.assertIn("tag3", doc.get("tags", ""))
        except Exception as e:
            self.fail(f"add_document with string tags raised exception: {e}")
    
    def test_batch_field_types(self):
        """Test that batch document addition handles various field types."""
        try:
            # Create documents with different field types
            documents = [
                (3, {"content": "Document 3", "tags": ["batch1", "batch2"]}),
                (4, {"content": "Document 4", "tags": "batch3 batch4"})
            ]
            
            # Add documents in batch
            self.index.add_documents_with_fields_parallel(documents)
            
            # Verify documents were added
            doc3 = self.index.get_document(3)
            doc4 = self.index.get_document(4)
            
            self.assertIsNotNone(doc3)
            self.assertIsNotNone(doc4)
            
            # Tests passing - no need for debug prints
            # Check that tags were properly converted
            self.assertIn("batch1", doc3.get("tags", ""))
            self.assertIn("batch2", doc3.get("tags", ""))
            self.assertIn("batch3", doc4.get("tags", ""))
            self.assertIn("batch4", doc4.get("tags", ""))
        except Exception as e:
            self.fail(f"add_documents_with_fields_parallel raised exception: {e}")
    
    def test_search_with_limit(self):
        """Test that search accepts and respects the limit parameter."""
        # Add 10 documents
        for i in range(5, 15):
            self.index.add_document(i, f"Document {i} content")
        
        # Search with limit
        results = self.index.search("document", limit=3)
        
        # Verify limit was respected
        self.assertLessEqual(len(results), 3)
    
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

if __name__ == "__main__":
    unittest.main()