# Fast Inverted Index Examples

This directory contains example scripts demonstrating how to use the Fast Inverted Index library.

## Enterprise Search with Redis Content Storage

The `redis_search_engine.py` and `redis_search_engine_demo.py` examples demonstrate how to build a complete enterprise search solution using:

- Fast Inverted Index for indexing and searching
- Redis for document content storage
- Rich metadata handling and search result presentation

### Prerequisites

To run these examples, you need:

1. Redis server running on localhost:6379
2. Python Redis client installed: `pip install redis`

### Usage

Run the demo script to see a complete search engine in action:

```bash
python redis_search_engine_demo.py
```

### Key Concepts Demonstrated

1. **Separation of Concerns**:
   - Indexing: Fast Inverted Index creates efficient search structures
   - Storage: Redis stores the full document content
   - Combined: The application layer bridges these components

2. **Data Flow**:
   - Document Ingestion: Content is both indexed for search and stored in Redis
   - Searching: The index finds matching document IDs
   - Result Enrichment: The application fetches full content from Redis

3. **Enterprise Features**:
   - Rich document metadata
   - Tag fields supporting both list and string formats
   - Boolean queries (AND, OR)
   - Field-specific boosting
   - Formatted search results

## Memory Management Examples

The `memory_management_example.py` example shows how to:

- Monitor memory usage
- Implement proper cleanup
- Use memory management operations
- Handle large document collections efficiently

## Schema and Field Examples

The `field_search_example.py` and `schema_serialization_example.py` examples demonstrate:

- Creating schemas with different field types
- Field-specific searching
- Field boosting
- Schema serialization and loading

## Thread Safety

The `thread_safety_test.py` example shows how to:

- Use the index from multiple threads
- Perform concurrent reads and writes
- Test thread safety of various operations

## Additional Examples

- `multi_field_example.py`: Working with multiple fields in documents
- `memory_test_simple.py`: Simple memory usage testing

## Best Practices

These examples demonstrate several best practices:

1. Proper error handling
2. Clean resource management
3. Efficient batch operations
4. Type conversion handling
5. Content storage strategies
6. Documentation and commenting

## Support

If you encounter any issues with these examples, please check the main documentation or file an issue in the repository.