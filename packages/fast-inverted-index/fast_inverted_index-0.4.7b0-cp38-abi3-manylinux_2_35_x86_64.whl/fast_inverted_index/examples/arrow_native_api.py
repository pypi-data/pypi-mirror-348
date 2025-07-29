"""
Example of how the native Arrow integration API should work.

This file shows the desired API for the native Arrow integration.
Implementation of these methods needs to be added to the PyIndex class.
"""

import fast_inverted_index as fii
import pyarrow as pa
import json
import time

class PyIndexArrowExtension:
    """Extension to be added to PyIndex class."""
    
    def add_documents_from_arrow_batch(self, batch_bytes, id_field, content_fields, metadata_fields=None):
        """Process an Arrow RecordBatch for indexing.
        
        Args:
            batch_bytes: Serialized Arrow RecordBatch bytes
            id_field: Name of ID field
            content_fields: List of field names to index
            metadata_fields: Optional list of metadata field names
            
        Returns:
            Dict with indexing statistics
        """
        print(f"Native: add_documents_from_arrow_batch called")
        print(f"  - id_field: {id_field}")
        print(f"  - content_fields: {content_fields}")
        print(f"  - metadata_fields: {metadata_fields}")
        print(f"  - batch_bytes length: {len(batch_bytes)}")
        
        # This would be implemented in native code
        return {
            "documents_indexed": 3,  # Example values
            "tokens_indexed": 18,
            "elapsed_ms": 5,
            "errors": 0
        }
    
    def add_documents_from_arrow_batches(self, batches_bytes, id_field, content_fields, metadata_fields=None):
        """Process multiple Arrow RecordBatches for indexing.
        
        Args:
            batches_bytes: List of serialized Arrow RecordBatch bytes
            id_field: Name of ID field  
            content_fields: List of field names to index
            metadata_fields: Optional list of metadata field names
            
        Returns:
            Dict with indexing statistics
        """
        print(f"Native: add_documents_from_arrow_batches called")
        print(f"  - id_field: {id_field}")
        print(f"  - content_fields: {content_fields}")
        print(f"  - metadata_fields: {metadata_fields}")
        print(f"  - batches count: {len(batches_bytes)}")
        
        # This would be implemented in native code
        return {
            "documents_indexed": 6,  # Example values
            "tokens_indexed": 36,
            "elapsed_ms": 10,
            "errors": 0
        }
    
    def add_documents_from_arrow_parallel(self, batch_bytes, id_field, content_fields, metadata_fields=None, parallel_config=None):
        """Process an Arrow RecordBatch for indexing using parallel processing.
        
        Args:
            batch_bytes: Serialized Arrow RecordBatch bytes
            id_field: Name of ID field
            content_fields: List of field names to index
            metadata_fields: Optional list of metadata field names
            parallel_config: Optional parallel processing config
            
        Returns:
            Dict with indexing statistics
        """
        print(f"Native: add_documents_from_arrow_parallel called")
        print(f"  - id_field: {id_field}")
        print(f"  - content_fields: {content_fields}")
        print(f"  - metadata_fields: {metadata_fields}")
        print(f"  - parallel_config: {parallel_config}")
        print(f"  - batch_bytes length: {len(batch_bytes)}")
        
        # This would be implemented in native code
        return {
            "documents_indexed": 3,  # Example values
            "tokens_indexed": 18,
            "elapsed_ms": 3,
            "errors": 0
        }
    
    def add_documents_from_arrow_batches_parallel(self, batches_bytes, id_field, content_fields, metadata_fields=None, parallel_config=None):
        """Process multiple Arrow RecordBatches for indexing using parallel processing.
        
        Args:
            batches_bytes: List of serialized Arrow RecordBatch bytes
            id_field: Name of ID field
            content_fields: List of field names to index
            metadata_fields: Optional list of metadata field names
            parallel_config: Optional parallel processing config
            
        Returns:
            Dict with indexing statistics
        """
        print(f"Native: add_documents_from_arrow_batches_parallel called")
        print(f"  - id_field: {id_field}")
        print(f"  - content_fields: {content_fields}")
        print(f"  - metadata_fields: {metadata_fields}")
        print(f"  - parallel_config: {parallel_config}")
        print(f"  - batches count: {len(batches_bytes)}")
        
        # This would be implemented in native code  
        return {
            "documents_indexed": 6,  # Example values
            "tokens_indexed": 36,
            "elapsed_ms": 5,
            "errors": 0
        }

# Monkey-patch the methods onto PyIndex for demonstration
for name, method in PyIndexArrowExtension.__dict__.items():
    if callable(method) and not name.startswith('__'):
        setattr(fii.Index, name, method.__get__(None, fii.Index))

def main():
    """Demonstrate the desired API for Arrow integration."""
    # Create sample data
    data = [
        {"id": 1, "title": "Arrow Integration", "content": "Fast zero-copy data transfer", "author": "Dev"},
        {"id": 2, "title": "PyO3 Bindings", "content": "Rust and Python interoperability", "author": "Dev"},
        {"id": 3, "title": "Performance Boost", "content": "Bulk document loading optimizations", "author": "Dev"},
    ]
    
    # Create Arrow RecordBatch
    batch = pa.RecordBatch.from_pylist(data)
    print(f"Created Arrow batch with {batch.num_rows} rows and schema:")
    print(batch.schema)
    
    # Serialize batch to IPC format
    sink = pa.BufferOutputStream()
    writer = pa.ipc.new_file(sink, batch.schema)
    writer.write_batch(batch)
    writer.close()
    buffer = sink.getvalue()
    batch_bytes = buffer.to_pybytes()
    
    # Create another batch
    data2 = [
        {"id": 4, "title": "Second Batch", "content": "Testing multiple batches", "author": "Dev"},
        {"id": 5, "title": "Batch Processing", "content": "Handling multiple data chunks", "author": "Dev"},
        {"id": 6, "title": "Arrow Records", "content": "Columnar data format benefits", "author": "Dev"},
    ]
    batch2 = pa.RecordBatch.from_pylist(data2)
    
    # Serialize second batch
    sink2 = pa.BufferOutputStream()
    writer2 = pa.ipc.new_file(sink2, batch2.schema)
    writer2.write_batch(batch2)
    writer2.close()
    buffer2 = sink2.getvalue()
    batch_bytes2 = buffer2.to_pybytes()
    
    # Create index
    index = fii.Index.builder().build()
    
    print("\n=== Testing add_documents_from_arrow_batch ===")
    stats = index.add_documents_from_arrow_batch(
        batch_bytes,
        id_field="id",
        content_fields=["title", "content"],
        metadata_fields=["author"]
    )
    print(f"Stats: {json.dumps(stats, indent=2)}")
    
    print("\n=== Testing add_documents_from_arrow_batches ===")
    stats = index.add_documents_from_arrow_batches(
        [batch_bytes, batch_bytes2],
        id_field="id",
        content_fields=["title", "content"],
        metadata_fields=["author"]
    )
    print(f"Stats: {json.dumps(stats, indent=2)}")
    
    print("\n=== Testing add_documents_from_arrow_parallel ===")
    config = {"num_threads": 4, "batch_size": 100, "channel_capacity": 10}
    stats = index.add_documents_from_arrow_parallel(
        batch_bytes,
        id_field="id",
        content_fields=["title", "content"],
        metadata_fields=["author"],
        parallel_config=config
    )
    print(f"Stats: {json.dumps(stats, indent=2)}")
    
    print("\n=== Testing add_documents_from_arrow_batches_parallel ===")
    stats = index.add_documents_from_arrow_batches_parallel(
        [batch_bytes, batch_bytes2],
        id_field="id",
        content_fields=["title", "content"],
        metadata_fields=["author"],
        parallel_config=config
    )
    print(f"Stats: {json.dumps(stats, indent=2)}")
    
if __name__ == "__main__":
    main()