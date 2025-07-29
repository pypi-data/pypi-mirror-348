"""
Fast Inverted Index - A high-performance search engine.

This module provides Python bindings for the Rust implementation of an
inverted index with a modular query engine.

The index provides the following features:
- Efficient term dictionary using a Radix Trie
- Fast posting list traversal with skip pointers
- Variable-length integer compression
- Thread-safe LRU caching
- Persistent storage with RocksDB
- Modular query engine with a rich Domain Specific Language (DSL)
- Field boosting and multiple ranking algorithms (TF-IDF, BM25, BM25L, Learning to Rank)
- Faceted search and filtering
- Score explanations for debugging
- Term suggestion and autocomplete

Query Engine Usage:
    # Import required classes
    from fast_inverted_index import Index, QueryNode, QueryExecutionParams
    
    # Create an index and add documents
    index = Index()
    index.add_document(1, "Python is a high-level programming language...")
    
    # Create a simple term query
    term_query = QueryNode.term("content", "python")
    
    # Create a boolean query (note: AND, OR, and NOT have uppercase alternatives to avoid Python keyword conflicts)
    bool_query = QueryNode.AND([
        QueryNode.term("content", "python"),
        QueryNode.NOT(QueryNode.term("content", "javascript"))
    ])
    
    # Create a boosted field query
    boosted_query = QueryNode.OR([
        QueryNode.term("title", "python", boost=2.0),
        QueryNode.term("content", "python", boost=1.0)
    ])
    
    # Execute a query with explanations
    params = QueryExecutionParams(
        scoring_algorithm="bm25l",
        explain=True,
        limit=10
    )
    result = index.execute_query(bool_query, params)
    
    # Access results
    for doc_id, score in result.scored_docs:
        print(f"Document {doc_id}: {score}")
        if result.explanations and doc_id in result.explanations:
            print(f"  Explanation: {result.explanations[doc_id].description}")
"""

try:
    from ._fast_inverted_index import (
        PyIndex, 
        PyIndexBuilder,
        PyIndexConfig,
        PyDictionaryConfig,
        PyValue,
        PyQueryBound,
        PyQueryNode,
        PyQueryExecutionParams,
        PyQueryResult,
        PyScoreExplanation,
        ScoringAlgorithms,
        __version__,
        BooleanOperators,
        RankingMethods,
        # Schema types
        PyFieldType,
        PyAnalyzerType,
        PyFieldSchema,
        PySchema,
        PySchemaBuilder,
        FieldTypes,
        AnalyzerTypes,
    )
except ImportError:
    # For mock implementation in case the module can't be loaded
    class PyIndex:
        pass
    class PyIndexBuilder:
        pass
    class PyIndexConfig:
        pass
    class PyDictionaryConfig:
        pass
    class PyValue:
        pass
    class PyQueryBound:
        pass
    class PyQueryNode:
        pass
    class PyQueryExecutionParams:
        pass
    class PyQueryResult:
        pass
    class PyScoreExplanation:
        pass
    class PyFieldType:
        pass
    class PyAnalyzerType:
        pass
    class PyFieldSchema:
        pass
    class PySchema:
        pass
    class PySchemaBuilder:
        pass
    __version__ = "0.4.7-beta"
    BooleanOperators = {"AND": "AND", "OR": "OR", "NOT": "NOT"}
    RankingMethods = {"TFIDF": "tfidf", "BM25": "bm25"}
    ScoringAlgorithms = {"TFIDF": "tfidf", "BM25": "bm25", "BM25L": "bm25l", "LTR": "ltr"}
    FieldTypes = {"TEXT": "text", "KEYWORD": "keyword", "NUMERIC": "numeric", "DATE": "date", "BOOLEAN": "boolean"}
    AnalyzerTypes = {"STANDARD": "standard", "KEYWORD": "keyword", "SIMPLE": "simple"}
    
# Export PyIndex as Index for backward compatibility
Index = PyIndex
IndexBuilder = PyIndexBuilder
IndexConfig = PyIndexConfig
DictionaryConfig = PyDictionaryConfig

# Export query engine classes with more user-friendly names
Value = PyValue
QueryBound = PyQueryBound
QueryNode = PyQueryNode
QueryExecutionParams = PyQueryExecutionParams
QueryResult = PyQueryResult
ScoreExplanation = PyScoreExplanation

# Export schema classes with more user-friendly names
FieldType = PyFieldType
AnalyzerType = PyAnalyzerType
FieldSchema = PyFieldSchema
Schema = PySchema
SchemaBuilder = PySchemaBuilder

class QueryBuilder:
    """Class to help build complex queries."""
    
    def __init__(self, index):
        self.index = index
        self.terms = []
        
    def add_term(self, term):
        """Add a single term to the query."""
        self.terms.append(term)
        return self
        
    def build_and_query(self):
        """Build and execute an AND query."""
        return self.index.and_query(self.terms)
        
    def build_or_query(self):
        """Build and execute an OR query."""
        return self.index.or_query(self.terms)
        
    def clear(self):
        """Clear all terms from the builder."""
        self.terms = []
        return self

# Make user-friendly exceptions available
class IndexError(Exception):
    """Base class for index errors."""
    pass
    
class DocumentNotFoundError(IndexError):
    """Raised when a document is not found."""
    pass
    
class TermNotFoundError(IndexError):
    """Raised when a term is not found."""
    pass

__all__ = [
    # Index classes
    "PyIndex", 
    "Index", 
    "PyIndexBuilder",
    "IndexBuilder",
    "PyIndexConfig",
    "IndexConfig",
    "PyDictionaryConfig",
    "DictionaryConfig",
    "__version__",
    "QueryBuilder",
    "BooleanOperators",
    "RankingMethods",
    "ScoringAlgorithms",
    
    # Query engine classes
    "PyValue",
    "Value",
    "PyQueryBound",
    "QueryBound",
    "PyQueryNode",
    "QueryNode",
    "PyQueryExecutionParams",
    "QueryExecutionParams",
    "PyQueryResult",
    "QueryResult",
    "PyScoreExplanation",
    "ScoreExplanation",
    
    # Exceptions
    "IndexError",
    "DocumentNotFoundError",
    "TermNotFoundError",
    
    # Schema types
    "PyFieldType",
    "FieldType",
    "PyAnalyzerType",
    "AnalyzerType",
    "PyFieldSchema",
    "FieldSchema",
    "PySchema",
    "Schema",
    "PySchemaBuilder",
    "SchemaBuilder",
    "FieldTypes",
    "AnalyzerTypes",
]