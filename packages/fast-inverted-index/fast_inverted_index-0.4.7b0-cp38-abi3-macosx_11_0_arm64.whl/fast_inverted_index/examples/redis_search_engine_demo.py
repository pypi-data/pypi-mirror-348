#!/usr/bin/env python
"""
Redis-Backed Search Engine Demo

This script demonstrates how to build a complete search engine using:
- Fast Inverted Index for indexing and searching
- Redis for storing and retrieving the full document content

Usage:
  python redis_search_engine_demo.py

Requirements:
  pip install redis fast-inverted-index
"""

import json
import time
import redis
from fast_inverted_index import Index, Schema, FieldSchema, QueryBuilder

class RedisSearchEngine:
    """
    Search engine that combines Fast Inverted Index with Redis for content storage.
    """
    def __init__(self, redis_host='localhost', redis_port=6379, redis_db=0, 
                 prefix='search:', in_memory=True, storage_path=None):
        """Initialize the search engine."""
        # Connect to Redis
        self.redis = redis.Redis(host=redis_host, port=redis_port, db=redis_db)
        self.prefix = prefix
        
        # Create schema for the index
        self.schema = Schema()
        self.schema.add_field(FieldSchema.text("title").with_boost(3.0))
        self.schema.add_field(FieldSchema.text("content"))
        self.schema.add_field(FieldSchema.keyword("tags"))
        self.schema.add_field(FieldSchema.keyword("category"))
        self.schema.add_field(FieldSchema.keyword("author"))
        
        # Create the index
        self.index = Index(
            storage_path=storage_path,
            in_memory=in_memory,
            schema=self.schema
        )
        
        print(f"Connected to Redis at {redis_host}:{redis_port}")
        print("Search engine initialized!")
    
    def _get_redis_key(self, doc_id):
        """Get the Redis key for a document."""
        return f"{self.prefix}doc:{doc_id}"
    
    def add_document(self, doc_id, content, metadata):
        """
        Add a document to both the index and Redis.
        
        Args:
            doc_id: Unique document identifier
            content: Document content text
            metadata: Dictionary of metadata fields
        """
        # Add to index
        self.index.add_document(doc_id, content, metadata)
        
        # Store in Redis
        doc_data = {
            "id": doc_id,
            "content": content,
            "metadata": metadata,
            "indexed_at": time.time()
        }
        
        self.redis.set(
            self._get_redis_key(doc_id),
            json.dumps(doc_data)
        )
        
        return doc_id
    
    def get_document(self, doc_id):
        """
        Get a document by ID, combining index metadata and content from Redis.
        
        Args:
            doc_id: The document ID to retrieve
            
        Returns:
            Dictionary with document metadata and content
        """
        # Get metadata from index
        index_data = self.index.get_document(doc_id)
        
        # Get content from Redis
        redis_data = self.redis.get(self._get_redis_key(doc_id))
        if redis_data:
            redis_data = json.loads(redis_data)
            # Combine data
            result = {
                "id": doc_id,
                "content": redis_data.get("content", ""),
                **index_data
            }
            return result
        else:
            # Just return index data if Redis data not found
            return index_data
    
    def search(self, query, limit=10):
        """
        Search for documents and enrich results with content.
        
        Args:
            query: Search query string
            limit: Maximum number of results to return
            
        Returns:
            List of dictionaries containing document data
        """
        # Search the index
        results = self.index.search(query, limit=limit)
        
        # Enrich results with content
        enriched_results = []
        for doc_id, score in results:
            doc = self.get_document(doc_id)
            doc["score"] = score
            enriched_results.append(doc)
            
        return enriched_results
    
    def build_and_query(self, terms):
        """Execute an AND query using the QueryBuilder."""
        builder = QueryBuilder(self.index)
        for term in terms:
            builder.add_term(term)
        
        doc_ids = builder.build_and_query()
        
        # Enrich with content
        enriched_results = []
        for doc_id in doc_ids:
            doc = self.get_document(doc_id)
            enriched_results.append(doc)
            
        return enriched_results
    
    def build_or_query(self, terms):
        """Execute an OR query using the QueryBuilder."""
        builder = QueryBuilder(self.index)
        for term in terms:
            builder.add_term(term)
        
        doc_ids = builder.build_or_query()
        
        # Enrich with content
        enriched_results = []
        for doc_id in doc_ids:
            doc = self.get_document(doc_id)
            enriched_results.append(doc)
            
        return enriched_results
    
    def get_stats(self):
        """Get statistics about the search engine."""
        # Get number of documents in Redis
        keys = self.redis.keys(f"{self.prefix}doc:*")
        num_docs_redis = len(keys)
        
        return {
            "num_docs_redis": num_docs_redis,
        }
    
    def close(self):
        """Close connections."""
        self.index.close()
        self.redis.close()
        print("Search engine connections closed.")


def print_result(doc, snippet_length=100):
    """Print a search result in a formatted way."""
    # Format title
    title = doc.get("title", "Untitled")
    print(f"\033[1m{title}\033[0m (Score: {doc.get('score', 'N/A')})")
    
    # Format metadata
    if "author" in doc:
        print(f"Author: {doc['author']}")
    
    if "tags" in doc:
        tags = doc["tags"]
        if isinstance(tags, list):
            tags_str = ", ".join(tags)
        else:
            tags_str = tags
        print(f"Tags: {tags_str}")
    
    # Format content snippet
    content = doc.get("content", "")
    if content:
        if len(content) > snippet_length:
            content = content[:snippet_length] + "..."
        print(f"\n{content}\n")
    
    print("-" * 50)


def load_sample_documents():
    """Create sample documents for the search engine."""
    return [
        {
            "id": 1,
            "title": "Introduction to Python Programming",
            "content": "Python is a high-level, interpreted programming language known for its readability and versatility. "
                      "Created by Guido van Rossum and first released in 1991, Python features a dynamic type system and "
                      "automatic memory management. Its simple, easy-to-learn syntax emphasizes readability, which reduces "
                      "the cost of program maintenance. Python supports modules and packages, encouraging program modularity "
                      "and code reuse. It's widely used in web development, data analysis, artificial intelligence, scientific "
                      "computing, and more.",
            "tags": ["python", "programming", "tutorial"],
            "category": "Technology",
            "author": "Guido Mentor"
        },
        {
            "id": 2,
            "title": "Machine Learning Fundamentals",
            "content": "Machine learning is a subset of artificial intelligence that provides systems the ability to "
                      "automatically learn and improve from experience without being explicitly programmed. Machine learning "
                      "focuses on developing computer programs that can access data and use it to learn for themselves. "
                      "The process of learning begins with observations or data, such as examples, direct experience, or "
                      "instruction, in order to look for patterns in data and make better decisions in the future based on "
                      "the examples provided. The primary aim is to allow computers to learn automatically without human "
                      "intervention and adjust actions accordingly.",
            "tags": ["machine learning", "AI", "data science"],
            "category": "Technology",
            "author": "Ada Lovelace"
        },
        {
            "id": 3,
            "title": "The History of Jazz Music",
            "content": "Jazz is a music genre that originated in the African-American communities of New Orleans, Louisiana, "
                      "in the late 19th and early 20th centuries, with its roots in blues and ragtime. Since the 1920s "
                      "Jazz Age, it has been recognized as a major form of musical expression in traditional and popular "
                      "music. Jazz is characterized by swing and blue notes, complex chords, call and response vocals, "
                      "polyrhythms, and improvisation. Jazz has roots in European harmony and African rhythmic rituals.",
            "tags": ["jazz", "music", "history"],
            "category": "Arts",
            "author": "Louis Armstrong"
        },
        {
            "id": 4,
            "title": "Introduction to Quantum Computing",
            "content": "Quantum computing is an area of computing focused on developing computer technology based on the "
                      "principles of quantum theory, which explains the behavior of energy and material on the atomic and "
                      "subatomic levels. Unlike classical computers that use bits (0s and 1s), quantum computers use quantum "
                      "bits or qubits, which can exist in multiple states simultaneously thanks to a property called "
                      "superposition. This allows quantum computers to handle operations at speeds exponentially higher "
                      "than conventional computers and to address problems that are too complex for classical systems.",
            "tags": ["quantum", "computing", "physics"],
            "category": "Science",
            "author": "Richard Feynman"
        },
        {
            "id": 5,
            "title": "Sustainable Agriculture Practices",
            "content": "Sustainable agriculture is farming in sustainable ways meeting society's present food and textile needs, "
                      "without compromising the ability for current or future generations to meet their needs. It can be based "
                      "on an understanding of ecosystem services. Sustainable agriculture is farming in sustainable ways based "
                      "on an understanding of ecosystem services, the study of relationships between organisms and their "
                      "environment. It integrates three main goals: environmental health, economic profitability, and social "
                      "equity. These goals have been defined by various disciplines and may be looked at from the vantage "
                      "point of the farmer or the consumer.",
            "tags": ["agriculture", "sustainability", "environment"],
            "category": "Environment",
            "author": "Wendell Berry"
        },
        {
            "id": 6,
            "title": "Modern Web Development Techniques",
            "content": "Modern web development encompasses a variety of technologies and methodologies aimed at building "
                      "robust, scalable, and user-friendly web applications. Today's web development often involves JavaScript "
                      "frameworks like React, Angular, or Vue.js for frontend development, with Node.js, Django, or Ruby on Rails "
                      "for backend services. Modern web applications often employ RESTful or GraphQL APIs to communicate between "
                      "client and server. Responsive design ensures applications work across all device sizes, while progressive "
                      "enhancement and accessibility considerations make apps usable for everyone.",
            "tags": ["web development", "javascript", "programming"],
            "category": "Technology",
            "author": "Tim Berners-Lee"
        },
        {
            "id": 7,
            "title": "The Basics of Astronomy",
            "content": "Astronomy is the scientific study of celestial objects such as stars, planets, comets, and galaxies, "
                      "as well as phenomena that originate outside the Earth's atmosphere like cosmic background radiation. "
                      "It is concerned with the evolution, physics, chemistry, meteorology, and motion of celestial objects, "
                      "as well as the formation and development of the universe. Astronomy is one of the oldest sciences, "
                      "with astronomical artifacts dating back to the early civilizations of Mesopotamia, Egypt, China, "
                      "Greece, India, and Central America.",
            "tags": ["astronomy", "space", "science"],
            "category": "Science",
            "author": "Carl Sagan"
        },
        {
            "id": 8,
            "title": "Artificial Intelligence in Healthcare",
            "content": "Artificial intelligence is revolutionizing healthcare through improved diagnosis, treatment, and "
                      "patient care. Machine learning algorithms can analyze complex medical data to identify patterns "
                      "and predict outcomes with remarkable accuracy. AI applications in healthcare include disease "
                      "detection from medical images, personalized treatment recommendations, drug discovery, and "
                      "predictive analytics for patient monitoring. While these technologies offer tremendous potential "
                      "to enhance healthcare delivery and outcomes, they also raise important questions about data privacy, "
                      "algorithmic bias, and the changing role of healthcare professionals.",
            "tags": ["AI", "healthcare", "medicine"],
            "category": "Technology",
            "author": "Ada Lovelace"
        },
        {
            "id": 9,
            "title": "Climate Change and Global Impacts",
            "content": "Climate change refers to long-term shifts in temperatures and weather patterns, mainly caused by "
                      "human activities, particularly the burning of fossil fuels. These activities increase heat-trapping "
                      "greenhouse gas levels in Earth's atmosphere, raising temperatures. The impacts of climate change "
                      "include intense droughts, water scarcity, severe fires, rising sea levels, flooding, melting polar ice, "
                      "catastrophic storms, and declining biodiversity. The Paris Agreement of 2015 aims to limit global "
                      "warming to well below 2 degrees Celsius compared to pre-industrial levels by reducing greenhouse "
                      "gas emissions.",
            "tags": ["climate change", "environment", "global warming"],
            "category": "Environment",
            "author": "Greta Thunberg"
        },
        {
            "id": 10,
            "title": "The Philosophy of Mind",
            "content": "Philosophy of mind is a branch of philosophy that studies the nature of the mind, mental events, "
                      "mental functions, mental properties, consciousness, and their relationship to the physical body. "
                      "The mind-body problem is a central issue, addressing the relationship between thought and consciousness "
                      "in the human mind, and the brain as part of the physical body. Approaches to this problem include "
                      "dualism, monism, and functionalism. Contemporary debates include the nature of consciousness, the "
                      "mind-computer analogy, artificial intelligence, and the possibility of uploading minds to computers.",
            "tags": ["philosophy", "mind", "consciousness"],
            "category": "Philosophy",
            "author": "René Descartes"
        }
    ]


def run_example_searches(search_engine):
    """Run several example searches to demonstrate functionality."""
    # Example 1: Search for "python programming"
    print("\n\n===== EXAMPLE 1: Search for 'python programming' =====")
    results = search_engine.search("python programming")
    print(f"Found {len(results)} results:\n")
    for doc in results:
        print_result(doc)
    
    # Example 2: AND search for "artificial intelligence"
    print("\n\n===== EXAMPLE 2: AND search for 'artificial intelligence' =====")
    results = search_engine.build_and_query(["artificial", "intelligence"])
    print(f"Found {len(results)} results:\n")
    for doc in results:
        print_result(doc)
    
    # Example 3: OR search for "science" or "philosophy"
    print("\n\n===== EXAMPLE 3: OR search for 'science' OR 'philosophy' =====")
    results = search_engine.build_or_query(["science", "philosophy"])
    print(f"Found {len(results)} results:\n")
    for doc in results:
        print_result(doc)
    
    # Example 4: Get document by ID
    print("\n\n===== EXAMPLE 4: Get document by ID (5) =====")
    doc = search_engine.get_document(5)
    print_result(doc, snippet_length=200)
    
    # Example 5: Search for "climate change"
    print("\n\n===== EXAMPLE 5: Search for 'climate change' =====")
    results = search_engine.search("climate change")
    print(f"Found {len(results)} results:\n")
    for doc in results:
        print_result(doc)


def main():
    """Run the search engine example."""
    try:
        # Initialize search engine
        search_engine = RedisSearchEngine()
        
        # Load sample documents
        documents = load_sample_documents()
        
        # Add documents to the search engine
        print(f"Adding {len(documents)} documents to the search engine...")
        for doc in documents:
            search_engine.add_document(
                doc["id"],
                doc["content"],
                {k: v for k, v in doc.items() if k != "content" and k != "id"}
            )
        
        # Run examples
        run_example_searches(search_engine)
        
        # Show stats
        stats = search_engine.get_stats()
        print("\nSearch Engine Statistics:")
        for key, value in stats.items():
            print(f"  {key}: {value}")
        
        # Clean up
        search_engine.close()
        
    except redis.ConnectionError:
        print("\nERROR: Could not connect to Redis. Make sure Redis is running at localhost:6379.")
        print("You can start Redis with 'redis-server' or use Docker: 'docker run -p 6379:6379 redis'")
    
    except Exception as e:
        print(f"\nERROR: {str(e)}")
        raise


if __name__ == "__main__":
    main()