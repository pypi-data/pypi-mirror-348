"""
Content Retrieval Example

This script demonstrates how to add documents to the index and retrieve their content.
"""

from fast_inverted_index import Index
import json
import tempfile
import shutil

def main():
    """Run the content retrieval example."""
    # Create a temporary directory for the index
    temp_dir = tempfile.mkdtemp()
    
    try:
        # Create index
        index = Index(storage_path=temp_dir, in_memory=True)
        
        # Add a document with content
        doc_content = "This is the main content of my document. It includes important information."
        doc_fields = {
            "title": "Important Document",
            "tags": ["example", "test", "content"],
            "author": "Test User",
            "priority": "high"
        }
        
        # Add to index - note content is passed as the 2nd parameter
        index.add_document(1, doc_content, doc_fields)
        
        print("Document added to index.\n")
        
        # Retrieve the document
        doc = index.get_document(1)
        print(f"Document structure: {json.dumps(doc, indent=2)}")
        
        # Search for the document
        results = index.search("important information")
        print(f"\nSearch results for 'important information': {results}")
        
        # Add a document with content in the fields
        doc_fields2 = {
            "title": "Second Document",
            "content": "This is the content of my second document. It has the content inside the fields.",
            "tags": ["example", "content"],
            "author": "Another User"
        }
        
        index.add_document(2, doc_fields2["content"], doc_fields2)
        
        # Retrieve the second document
        doc2 = index.get_document(2)
        print(f"\nSecond document structure: {json.dumps(doc2, indent=2)}")
        
        # Demonstrate ways to get content
        print("\nDifferent ways to access document content:")
        print("1. Search and get content from original document:")
        results = index.search("second document")
        if results:
            doc_id = results[0][0]
            # Get document by ID
            doc = index.get_document(doc_id)
            print(f"   - Document title: {doc.get('title')}")
            print(f"   - Document has content field: {'content' in doc}")
            print(f"   - All available fields: {list(doc.keys())}")
        
        print("\n2. Original document content must be stored separately:")
        doc_store = {
            1: doc_content,
            2: doc_fields2["content"]
        }
        print(f"   - Original content for doc 1: {doc_store[1]}")
        print(f"   - Original content for doc 2: {doc_store[2]}")
    
    finally:
        # Clean up
        shutil.rmtree(temp_dir)

if __name__ == "__main__":
    main()