"""
Tests for the QueryBuilder API in Fast Inverted Index
"""

import unittest
import tempfile
import shutil
from fast_inverted_index import Index, Schema, FieldSchema, QueryBuilder


class QueryBuilderTest(unittest.TestCase):
    def setUp(self):
        # Create a temporary directory for the index
        self.temp_dir = tempfile.mkdtemp()
        
        # Create schema
        self.schema = Schema()
        self.schema.add_field(FieldSchema.text("title").with_boost(2.0))
        self.schema.add_field(FieldSchema.text("content"))
        self.schema.add_field(FieldSchema.keyword("tags"))
        
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
            "tags": ["python", "programming", "scripting"]
        })
        
        self.index.add_document(3, "Search engines use inverted indexes", {
            "title": "Search engines",
            "tags": ["search", "indexes"]
        })
        
        self.index.add_document(4, "Rust can be used with Python through bindings", {
            "title": "Rust and Python",
            "tags": ["rust", "python", "bindings"]
        })
    
    def tearDown(self):
        # Clean up
        self.index.close()
        shutil.rmtree(self.temp_dir, ignore_errors=True)
    
    def test_create_builder(self):
        """Test creating a QueryBuilder."""
        builder = QueryBuilder(self.index)
        self.assertIsNotNone(builder)
        self.assertEqual(builder.terms, [])  # Should start with empty terms list
    
    def test_add_term(self):
        """Test adding a term to the builder."""
        builder = QueryBuilder(self.index)
        builder.add_term("rust")
        self.assertEqual(len(builder.terms), 1)
        
        # Add another term
        builder.add_term("programming")
        self.assertEqual(len(builder.terms), 2)
    
    def test_clear_terms(self):
        """Test clearing terms from the builder."""
        builder = QueryBuilder(self.index)
        builder.add_term("rust")
        builder.add_term("programming")
        self.assertEqual(len(builder.terms), 2)
        
        # Clear terms
        builder.clear()
        self.assertEqual(len(builder.terms), 0)
    
    def test_build_or_query(self):
        """Test building an OR query."""
        # First builder with 'rust' term
        builder1 = QueryBuilder(self.index)
        builder1.add_term("rust")
        
        # Second builder with 'python' term
        builder2 = QueryBuilder(self.index)
        builder2.add_term("python")
        
        # Create a new builder for OR query
        or_builder = QueryBuilder(self.index)
        
        # Add both term lists
        for term in builder1.terms:
            or_builder.add_term(term)
            
        for term in builder2.terms:
            or_builder.add_term(term)
        
        # Build OR query - returns list of doc_ids directly
        doc_ids = or_builder.build_or_query()
        
        # Should find documents 1, 2, and 4
        self.assertIn(1, doc_ids)  # Rust doc
        self.assertIn(2, doc_ids)  # Python doc
        self.assertIn(4, doc_ids)  # Rust and Python doc
    
    def test_build_and_query(self):
        """Test building an AND query."""
        # Create a builder with multiple terms
        builder = QueryBuilder(self.index)
        builder.add_term("rust")
        builder.add_term("python")
        
        # Build AND query - should return docs containing both terms
        doc_ids = builder.build_and_query()
        
        # Should only find document 4 (which has both rust AND python)
        self.assertEqual(len(doc_ids), 1)
        self.assertEqual(doc_ids[0], 4)
    
    def test_direct_search(self):
        """Test direct search with a term list."""
        builder = QueryBuilder(self.index)
        builder.add_term("rust")
        
        # Use the terms directly in search
        hits = self.index.search(" ".join(builder.terms))
        
        # Extract document IDs
        doc_ids = [hit[0] for hit in hits]
        
        # Should find documents 1 and 4
        self.assertIn(1, doc_ids)
        self.assertIn(4, doc_ids)
    
    def test_complex_query(self):
        """Test a more complex query scenario."""
        # Create a builder for a complex query
        builder = QueryBuilder(self.index)
        
        # Add multiple terms
        builder.add_term("rust")
        builder.add_term("python")
        
        # Build OR query (documents with either rust OR python)
        doc_ids = builder.build_or_query()
        
        # Should find documents 1, 2, and 4
        self.assertEqual(len(doc_ids), 3)
        self.assertIn(1, doc_ids)  # Rust doc
        self.assertIn(2, doc_ids)  # Python doc
        self.assertIn(4, doc_ids)  # Rust and Python doc
        
        # Clear builder
        builder.clear()
        
        # Add multiple terms
        builder.add_term("rust")
        builder.add_term("python")
        
        # Try using different syntax for direct search
        hits = self.index.search("rust AND python")
        
        # Should only find document 4 (which has both rust AND python)
        doc_ids = [hit[0] for hit in hits]
        self.assertEqual(len(doc_ids), 1)
        self.assertEqual(doc_ids[0], 4)


if __name__ == "__main__":
    unittest.main()