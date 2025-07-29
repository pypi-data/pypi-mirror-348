"""
Simple test for Arrow indexing with persistence.
"""

import tempfile
import os
import shutil
import random
import string
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
        return {
            "documents_indexed": docs_indexed,
            "tokens_indexed": tokens_indexed,
            "errors": errors
        }


def test_persistence_with_memory_index():
    """Test persistence of Arrow-indexed data using memory index."""
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
    
    # Create fresh in-memory index
    builder = fii.IndexBuilder()
    builder.with_in_memory(True)
    index = builder.build()
    arrow_index = ArrowIndex(index)
    
    # Add documents
    stats = arrow_index.add_documents_from_arrow_batch(
        batch,
        id_field="id",
        content_fields=["title", "content"],
        metadata_fields=["author"]
    )
    
    # Verify document was indexed correctly
    assert stats["documents_indexed"] == 1, "Document should be indexed"
    
    # Verify document can be retrieved with correct content and metadata
    doc = index.get_document(1)
    print(f"Persisted document: {doc}")
    # Document is searchable by the content
    results = index.search("document")
    assert len(results) == 1, "Document should be searchable"
    # Check metadata
    assert doc["author"] == "Alice", "Document should contain author metadata"
    
    print("Memory index test passed!")


def test_persistence_with_file_index():
    """Test persistence of Arrow-indexed data with file storage."""
    # Create a temporary directory for the index
    temp_dir = tempfile.mkdtemp()
    index_path = os.path.join(temp_dir, "arrow_test")
    
    try:
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
        
        # Create a persistent index
        print(f"Creating index at: {index_path}")
        builder = fii.IndexBuilder()
        builder.with_storage_path(index_path)
        index = builder.build()
        arrow_index = ArrowIndex(index)
        
        # Add documents
        stats = arrow_index.add_documents_from_arrow_batch(
            batch,
            id_field="id",
            content_fields=["title", "content"],
            metadata_fields=["author"]
        )
        
        # Verify document was indexed correctly
        assert stats["documents_indexed"] == 1, "Document should be indexed"
        
        # Close the index to ensure data is flushed to disk
        index.close()
        
        # Try to reopen the index
        print("Reopening index...")
        builder = fii.IndexBuilder()
        builder.with_storage_path(index_path)
        reopened = builder.build()
        
        # Verify document can be retrieved
        doc = reopened.get_document(1)
        print(f"Retrieved document: {doc}")
        assert "Persistent Document" in doc["_content"], "Document should contain title"
        assert "This document should persist" in doc["_content"], "Document should contain content"
        assert doc["author"] == "Alice", "Document should contain metadata"
        
        # Close the reopened index
        reopened.close()
        
        print("Persistence test passed!")
        
    finally:
        # Clean up
        try:
            shutil.rmtree(temp_dir)
        except Exception as e:
            print(f"Error cleaning up: {e}")


if __name__ == "__main__":
    print("Testing Arrow indexing with memory index...")
    test_persistence_with_memory_index()
    
    print("\nTesting Arrow indexing with file persistence...")
    test_persistence_with_file_index()