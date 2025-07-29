"""
Example demonstrating schema serialization and persistence.

This example shows how to:
1. Create a schema with different field types
2. Save the schema to a file
3. Load the schema from a file
4. Create an index with the loaded schema
5. Verify the schema was preserved correctly
"""

import os
import sys
import shutil
import tempfile
import json

# Import the library - no path manipulation needed
# The library should be properly installed in the Python environment

from fast_inverted_index import (
    Index, Schema, FieldSchema, FieldType, AnalyzerType,
    QueryNode, QueryExecutionParams
)


def main():
    """Run the schema serialization example."""
    print("Schema Serialization Example")
    print("===========================\n")

    # Create a temporary directory for files
    temp_dir = tempfile.mkdtemp()
    schema_path = os.path.join(temp_dir, "blog_schema.json")
    index_path = os.path.join(temp_dir, "blog_index")
    
    try:
        # Step 1: Create a schema with different field types
        print("Creating a comprehensive blog post schema...")
        schema = Schema()
        
        # Add fields with different types and analyzers
        schema.add_field(FieldSchema.text("title").with_boost(5.0))
        schema.add_field(FieldSchema.text("content").with_boost(1.0))
        schema.add_field(FieldSchema.keyword("tags").with_boost(3.0))
        schema.add_field(FieldSchema.text("author").with_boost(2.0))
        schema.add_field(FieldSchema.keyword("category").with_boost(1.5))
        schema.add_field(FieldSchema.numeric("word_count"))
        schema.add_field(FieldSchema.date("published_at"))
        schema.add_field(FieldSchema.boolean("is_published"))
        
        # Set default field for queries that don't specify a field
        schema.set_default_field("content")
        
        # Step 2: Save the schema to a file
        print(f"Saving schema with {schema.len()} fields to {schema_path}...")
        schema.save_to_file(schema_path)
        
        # Print the content of the schema file
        print("\nSchema file content:")
        with open(schema_path, 'r') as f:
            schema_json = json.load(f)
            print(json.dumps(schema_json, indent=2))
        
        # Step 3: Load the schema from the file
        print("\nLoading schema from file...")
        loaded_schema = Schema.load_from_file(schema_path)
        print(f"Successfully loaded schema with {loaded_schema.len()} fields")
        print(f"Field names: {loaded_schema.field_names()}")
        
        # Step 4: Create an index with the loaded schema
        print("\nCreating index with loaded schema...")
        index = Index(storage_path=index_path, schema=loaded_schema)
        
        # Add a test document to the index
        print("Adding a document with fields...")
        doc_fields = {
            "title": "Schema Serialization in Fast Inverted Index",
            "content": "This article explains how to serialize and deserialize schemas for persistence.",
            "tags": "schema serialization persistence",
            "author": "Jane Smith",
            "category": "documentation",
            "word_count": "150",
            "published_at": "2025-05-01T10:00:00Z",
            "is_published": "true"
        }
        index.add_document_with_fields(1, doc_fields)
        
        # Verify document was added correctly with all fields
        print("\nVerifying document fields...")
        doc = index.get_document(1)
        for field in loaded_schema.field_names():
            if field in doc:
                print(f"  {field}: {doc[field]}")
            else:
                print(f"  {field}: Not found (Missing)")
        
        # Step 5: Search for document to verify schema is working correctly
        print("\nSearching document with field-specific queries...")
        
        # Search in title field using QueryNode API
        title_query = QueryNode.term("title", "schema")
        title_results = index.execute_query(title_query, QueryExecutionParams(limit=10)).scored_docs
        print(f"  Title search results: {len(title_results)} documents")
        
        # Search in tags field using QueryNode API
        tags_query = QueryNode.term("tags", "serialization")
        tags_results = index.execute_query(tags_query, QueryExecutionParams(limit=10)).scored_docs
        print(f"  Tags search results: {len(tags_results)} documents")
        
        # Create a complex query
        print("\nExecuting a complex field-aware query...")
        query = QueryNode.AND([
            QueryNode.OR([
                QueryNode.term("title", "schema", boost=5.0),
                QueryNode.term("tags", "serialization", boost=3.0)
            ]),
            QueryNode.term("is_published", "true")
        ])
        
        params = QueryExecutionParams(
            scoring_algorithm="bm25",
            limit=10
        )
        
        results = index.execute_query(query, params)
        print(f"  Complex query results: {len(results.scored_docs)} documents")
        
        print("\nSchema serialization example completed successfully!")
        
    finally:
        # Clean up temporary directory
        shutil.rmtree(temp_dir)
        print("\nTemporary directory removed.")


if __name__ == "__main__":
    main()