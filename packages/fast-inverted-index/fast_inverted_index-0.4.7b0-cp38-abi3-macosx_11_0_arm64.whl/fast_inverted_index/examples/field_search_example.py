#!/usr/bin/env python3
"""
Field Search Example - Demonstrates the use of field-specific search functionality.

This example shows how to use field-specific search with different field types
(text and keyword) and search behaviors, including:
- Single token searches in text fields
- Multi-token searches in text fields
- Exact matching in keyword fields 
- Field boosting
"""

import os
import tempfile
import shutil

# Import the library - no path manipulation needed
# The library should be properly installed in the Python environment
try:
    from fast_inverted_index import (
        Index, Schema, FieldSchema, QueryNode, 
        QueryExecutionParams, ScoringAlgorithms
    )
except ImportError:
    print("Error: Could not import fast_inverted_index. Please install the library:")
    print("  pip install fast-inverted-index")
    raise

def print_header(title):
    """Print a formatted section header."""
    print(f"\n{'-' * 80}")
    print(f"  {title}")
    print(f"{'-' * 80}")

def format_result(doc, score):
    """Format a search result for display."""
    title = doc.get('title', 'Unknown Title')
    author = doc.get('author', 'Unknown Author')
    category = doc.get('category', 'Uncategorized')
    return f"Score: {score:.4f} | {title} by {author} [{category}]"

def main():
    """Demonstrate field-specific search functionality."""
    print_header("Multi-Field Search Example")
    
    # Create a temporary directory for the index
    temp_dir = tempfile.mkdtemp()
    index_path = os.path.join(temp_dir, "field_search_example")
    
    try:
        # Create a schema with multiple field types
        print("\nCreating schema with text and keyword fields...")
        schema = Schema()
        
        # Add text fields with different analyzers
        schema.add_field(FieldSchema.text("title"))  # Title field with standard analyzer
        schema.add_field(FieldSchema.text("author"))  # Author field with standard analyzer
        schema.add_field(FieldSchema.text("content"))  # Content field with standard analyzer
        
        # Add keyword field (exact match)
        schema.add_field(FieldSchema.keyword("category"))
        
        # Set default field
        schema.set_default_field("content")
        
        # Create index with schema
        print("Creating index...")
        index = Index(storage_path=index_path, schema=schema)
        
        # Add sample documents
        print("Adding sample documents...")
        docs = [
            (1, {
                "title": "Python Programming Guide",
                "author": "Jane Smith",
                "category": "Programming",
                "content": "A comprehensive guide to Python programming language."
            }),
            (2, {
                "title": "Advanced Python Techniques", 
                "author": "John Doe",
                "category": "Programming",
                "content": "Learn advanced Python programming techniques for experts."
            }),
            (3, {
                "title": "Data Science with Python",
                "author": "Jane Smith",
                "category": "Data Science",
                "content": "Applying Python to solve data science problems."
            }),
            (4, {
                "title": "Machine Learning Fundamentals",
                "author": "Robert Johnson Smith",
                "category": "Data Science",
                "content": "Introduction to machine learning concepts."
            })
        ]
        
        # Add documents to index
        for doc_id, fields in docs:
            # Create content that combines all fields to ensure they're indexed
            content = f"{fields['title']} {fields['author']} {fields['content']} {fields['category']}"
            
            # Add document with fields and metadata
            index.add_document_with_metadata(doc_id, content, {
                "title": fields["title"],
                "author": fields["author"],
                "category": fields["category"]
            })
        
        # Demonstrate field-specific searches
        print_header("1. Single-Token Text Field Search (Author First Name)")
        results = index.search_field("author", "Jane", "bm25", 10)
        if results:
            print(f"Found {len(results)} documents with author name 'Jane':")
            for doc_id, score in results:
                doc = index.get_document(doc_id)
                print(f"  - {format_result(doc, score)}")
        else:
            print("No results found.")
        
        print_header("2. Multi-Token Text Field Search (Full Author Name)")
        results = index.search_field("author", "Jane Smith", "bm25", 10)
        if results:
            print(f"Found {len(results)} documents with full author name 'Jane Smith':")
            for doc_id, score in results:
                doc = index.get_document(doc_id)
                print(f"  - {format_result(doc, score)}")
        else:
            print("No results found.")
        
        print_header("3. Three-Token Author Name Search")
        results = index.search_field("author", "Robert Johnson Smith", "bm25", 10)
        if results:
            print(f"Found {len(results)} documents with author 'Robert Johnson Smith':")
            for doc_id, score in results:
                doc = index.get_document(doc_id)
                print(f"  - {format_result(doc, score)}")
        else:
            print("No results found.")
        
        print_header("4. Keyword Field Exact Match (Category)")
        results = index.search_field("category", "Data Science", "bm25", 10)
        if results:
            print(f"Found {len(results)} documents in 'Data Science' category:")
            for doc_id, score in results:
                doc = index.get_document(doc_id)
                print(f"  - {format_result(doc, score)}")
        else:
            print("No results found.")
        
        print_header("5. Multi-Field Search with Field Boosting")
        
        # Create field boosts dictionary
        field_boosts = {
            "title": 2.0,     # Highest boost
            "author": 1.5,    # Medium boost
            "content": 1.0,   # Normal boost
            "category": 1.0   # Normal boost
        }
        
        # Create query for multi-field search
        print("Running multi-field search for 'python' with field boosts...")
        # Use the v0.4.6 API for search with field boosting
        results = index.search("python", boost_fields=field_boosts, limit=10)
        
        if results:
            print(f"Found {len(results)} documents matching 'python' across all fields with boosting:")
            for doc_id, score in results:
                doc = index.get_document(doc_id)
                print(f"  - {format_result(doc, score)}")
        else:
            print("No results found.")
            
        # Alternative approach using the advanced Query DSL
        print("\nAlternative approach using the Query DSL:")
            
        # Create query nodes for each field (without boost since we'll specify it in parameters)
        title_query = QueryNode.term("title", "python")
        author_query = QueryNode.term("author", "jane")
        category_query = QueryNode.term("category", "programming")
        
        # Combine with OR to match any field
        combined_query = QueryNode.OR([title_query, author_query, category_query])
        
        # Set query parameters
        params = QueryExecutionParams(
            scoring_algorithm="bm25l",
            limit=10,
            explain=True  # Request explanations for debugging
        )
        
        # Execute the query
        result = index.execute_query(combined_query, params)
        
        if result and result.scored_docs:
            print(f"Found {len(result.scored_docs)} documents matching multi-field query:")
            for doc_id, score in result.scored_docs:
                doc = index.get_document(doc_id)
                print(f"  - {format_result(doc, score)}")
                
                # If explanations are available, show scoring details
                if result.explanations and doc_id in result.explanations:
                    print(f"    Explanation: {result.explanations[doc_id].description}")
        else:
            print("No results found.")
        
        print("\nSearch demonstration completed successfully!")
    
    finally:
        # Clean up temporary directory
        shutil.rmtree(temp_dir)
        print(f"\nCleaned up temporary index directory: {index_path}")

if __name__ == "__main__":
    main()