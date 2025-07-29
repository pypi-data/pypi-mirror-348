"""
Comprehensive example demonstrating multi-field indexing and searching.

This example shows how to:
1. Define a schema with different field types
2. Create an index with the schema
3. Add documents with field values
4. Search within specific fields
5. Control relevance with field boosting
6. Use QueryNode API for complex field-specific queries
7. Save and load schemas
8. Verify document metadata storage and retrieval
"""

import os
import sys
import shutil
import tempfile

# Import the library - no path manipulation needed
# The library should be properly installed in the Python environment

from fast_inverted_index import (
    Index, Schema, FieldSchema, FieldType, AnalyzerType,
    QueryNode, QueryExecutionParams
)


def main():
    """Run the multi-field indexing example."""
    print("Multi-Field Indexing Example")
    print("===========================\n")

    # Create a temporary directory for the index
    temp_dir = tempfile.mkdtemp()
    index_path = os.path.join(temp_dir, "multi_field_index")
    schema_path = os.path.join(temp_dir, "schema.json")
    
    try:
        # Step 1: Define a schema with different field types
        print("Creating schema with different field types...")
        schema = Schema()
        
        # Add fields with different types and properties
        # For text fields, a standard analyzer is used (tokenization, lowercasing)
        # For keyword fields, a keyword analyzer is used (no tokenization)
        schema.add_field(FieldSchema.text("title").with_boost(5.0))
        schema.add_field(FieldSchema.text("content").with_boost(1.0))
        schema.add_field(FieldSchema.keyword("tags").with_boost(3.0))
        schema.add_field(FieldSchema.text("author").with_boost(2.0))
        schema.add_field(FieldSchema.keyword("category").with_boost(1.5))
        
        # Set default field for queries that don't specify a field
        schema.set_default_field("content")
        
        # Display schema information
        print(f"  Schema has {schema.len()} fields")
        print(f"  Field names: {schema.field_names()}")
        
        # Save schema to file
        schema.save_to_file(schema_path)
        print(f"  Schema saved to {schema_path}")
        
        # Step 2: Create an index with the schema
        print("\nCreating index with schema...")
        index = Index(storage_path=index_path, schema=schema)
        
        # Step 3: Add documents with fields
        print("\nAdding documents with fields...")
        
        # Method 1: Add a document using add_document_with_fields
        # The recommended approach for multi-field documents
        print("  Adding document 1 with add_document_with_fields...")
        doc1_fields = {
            "title": "Python Programming Guide",
            "content": "Python is a high-level programming language with simple, easy-to-learn syntax.",
            "tags": "programming python tutorial",  # For keyword fields, strings are treated as single terms
            "author": "Jane Smith",
            "category": "programming"
        }
        index.add_document_with_fields(1, doc1_fields)
        
        # Method 2: Using add_document_with_fields for the second document too
        # (Legacy add_document method is not recommended for multi-field use)
        print("  Adding document 2 with add_document_with_fields...")
        doc2_fields = {
            "title": "Rust Systems Programming",
            "content": "Rust provides memory safety without a garbage collector, making it ideal for systems programming.",
            "author": "John Doe",
            "tags": "rust systems programming",  # String format for consistency
            "category": "programming"
        }
        index.add_document_with_fields(2, doc2_fields)
        
        # Add more documents using the recommended add_document_with_fields method
        print("  Adding document 3 with fields...")
        doc3_fields = {
            "title": "Python Data Science",
            "content": "Python is widely used in data science and machine learning applications.",
            "tags": "python data-science machine-learning",
            "author": "Jane Smith",
            "category": "data-science"
        }
        index.add_document_with_fields(3, doc3_fields)
        
        print("  Adding document 4 with fields...")
        doc4_fields = {
            "title": "Web Development with JavaScript",
            "content": "JavaScript is the primary language for web development in browsers.",
            "tags": "javascript web development",
            "author": "Bob Johnson",
            "category": "web-development"
        }
        index.add_document_with_fields(4, doc4_fields)
        
        # Step 4: Verify document metadata storage
        print("\nVerifying document metadata storage...")
        for doc_id in range(1, 5):
            doc = index.get_document(doc_id)
            print(f"  Document {doc_id} metadata:")
            for field in schema.field_names():
                if field in doc:
                    print(f"    {field}: {doc[field]}")
            print()
        
        # Step 5: Search within specific fields
        print("\nSearching within specific fields...")
        
        # Search in the title field
        print("\n  Searching for 'Python' in the title field:")
        # Create field-specific search using QueryNode API
        title_query = QueryNode.term("title", "Python")
        title_results = index.execute_query(title_query, QueryExecutionParams(limit=10)).scored_docs
        print_results(index, title_results)
        
        # Search in the content field
        print("\n  Searching for 'programming' in the content field:")
        content_query = QueryNode.term("content", "programming")
        content_results = index.execute_query(content_query, QueryExecutionParams(limit=10)).scored_docs
        print_results(index, content_results)
        
        # Search in the author field
        print("\n  Searching for 'Jane' in the author field:")
        author_query = QueryNode.term("author", "Jane")
        author_results = index.execute_query(author_query, QueryExecutionParams(limit=10)).scored_docs
        print_results(index, author_results)
        
        # Search in the tags field (keyword field)
        print("\n  Searching for 'python' in the tags field:")
        tags_query = QueryNode.term("tags", "python")
        tags_results = index.execute_query(tags_query, QueryExecutionParams(limit=10)).scored_docs
        print_results(index, tags_results)
        
        # Step 6: Control relevance with field boosting
        print("\nSearching across all fields with boosting...")
        
        # Define field boosts
        boost_fields = {
            "title": 5.0,    # Title matches are 5x more important
            "content": 1.0,  # Content matches have normal importance
            "tags": 3.0,     # Tag matches are 3x more important
            "author": 2.0,   # Author matches are 2x more important
            "category": 1.5  # Category matches are 1.5x more important
        }
        
        # Search for "python" with field boosts
        print("\n  Searching for 'python' with field boosts:")
        boost_results = index.search("python", boost_fields=boost_fields, limit=10)
        print_results(index, boost_results)
        
        # Step 7: Use QueryNode API for more complex field queries
        print("\nUsing QueryNode API for field-specific searches...")
        
        # Create a multi-field query with different boosts
        query = QueryNode.OR([
            QueryNode.term("title", "python", boost=5.0),
            QueryNode.term("content", "python", boost=1.0),
            QueryNode.term("tags", "python", boost=3.0)
        ])
        
        # Execute the query
        params = QueryExecutionParams(
            scoring_algorithm="bm25",
            limit=10
        )
        query_results = index.execute_query(query, params)
        
        print("\n  Results from multi-field query:")
        for doc_id, score in query_results.scored_docs:
            doc = index.get_document(doc_id)
            print(f"    Document ID: {doc_id}, Score: {score:.4f}, Title: {doc['title']}")
        
        # Create a more complex combined query
        print("\n  Creating a complex combined query...")
        complex_query = QueryNode.AND([
            # Must contain 'python' in any of these fields
            QueryNode.OR([
                QueryNode.term("title", "python", boost=5.0),
                QueryNode.term("content", "python", boost=1.0),
                QueryNode.term("tags", "python", boost=3.0)
            ]),
            # Must be authored by 'Jane Smith'
            QueryNode.term("author", "jane smith")
        ])
        
        # Execute the complex query
        complex_results = index.execute_query(complex_query, params)
        
        print("\n  Results from complex combined query:")
        print_results(index, complex_results.scored_docs)
        
        # Step 8: Load a schema from file and create a new index
        print("\nLoading schema from file and creating a new index...")
        loaded_schema = Schema.load_from_file(schema_path)
        print(f"  Loaded schema has {loaded_schema.len()} fields")
        print(f"  Field names: {loaded_schema.field_names()}")
        
        # Create a new index with the loaded schema
        new_index_path = os.path.join(temp_dir, "new_multi_field_index")
        new_index = Index(storage_path=new_index_path, schema=loaded_schema)
        
        # Add a document to the new index
        print("\n  Adding a document to the new index...")
        new_doc_fields = {
            "title": "Machine Learning with Python",
            "content": "Using Python for machine learning and AI applications.",
            "tags": "python machine-learning AI",
            "author": "Alice Brown",
            "category": "machine-learning"
        }
        new_index.add_document_with_fields(1, new_doc_fields)
        
        # Verify the document was added correctly
        print("\n  Verifying document in new index:")
        new_doc = new_index.get_document(1)
        for field in loaded_schema.field_names():
            if field in new_doc:
                print(f"    {field}: {new_doc[field]}")
        
        print("\nExample completed successfully!")
        
    finally:
        # Clean up temporary directory
        shutil.rmtree(temp_dir)


def print_results(index, results):
    """Print search results with document details."""
    if not results:
        print("    No results found")
        return
    
    for doc_id, score in results:
        doc = index.get_document(doc_id)
        print(f"    Document ID: {doc_id}, Score: {score:.4f}, Title: {doc['title'] if 'title' in doc else 'N/A'}")
        # Also display the matched field values when available
        if 'content' in doc:
            content = doc['content']
            if len(content) > 60:
                content = content[:57] + "..."
            print(f"      Content: {content}")


if __name__ == "__main__":
    main()