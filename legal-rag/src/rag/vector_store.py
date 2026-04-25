#!/usr/bin/env python3
"""
ChromaDB Vector Store for Legal RAG System

Manages vector database for semantic search over legal documents.
"""

import json
from pathlib import Path
from typing import Dict, List, Any, Optional, Tuple
from datetime import datetime
import chromadb
from chromadb.config import Settings
from chromadb.utils import embedding_functions


class LegalVectorStore:
    """ChromaDB vector store for legal document retrieval."""
    
    def __init__(self, persist_directory: str = "data/chroma_db"):
        """
        Initialize ChromaDB vector store.
        
        Args:
            persist_directory: Directory to persist the database
        """
        self.persist_dir = Path(persist_directory)
        self.persist_dir.mkdir(parents=True, exist_ok=True)
        
        print(f"Initializing ChromaDB at: {self.persist_dir}")
        
        # Initialize ChromaDB client with persistence
        self.client = chromadb.PersistentClient(
            path=str(self.persist_dir),
            settings=Settings(
                anonymized_telemetry=False,
                allow_reset=True
            )
        )
        
        self.collection = None
        self.embeddings_dir = Path("data/embeddings")
        
        print("ChromaDB initialized")
    
    def create_collection(self, collection_name: str = "indian_laws", reset: bool = False) -> None:
        """
        Create or get collection for legal documents.
        
        Args:
            collection_name: Name of the collection
            reset: If True, delete existing collection and create new
        """
        if reset:
            try:
                self.client.delete_collection(collection_name)
                print(f"Deleted existing collection: {collection_name}")
            except:
                pass
        
        # Create collection with cosine similarity
        self.collection = self.client.get_or_create_collection(
            name=collection_name,
            metadata={"hnsw:space": "cosine"}  # Use cosine similarity
        )
        
        print(f"Collection ready: {collection_name}")
        print(f"Current document count: {self.collection.count()}")
    
    def load_embedded_chunks(self) -> List[Dict[str, Any]]:
        """
        Load embedded chunks from JSON file.
        
        Returns:
            List of chunk dictionaries with embeddings
        """
        master_file = self.embeddings_dir / "all_legal_embedded.json"
        
        if not master_file.exists():
            raise FileNotFoundError(
                f"Embedded chunks not found at {master_file}. "
                "Run embedder.py first to generate embeddings."
            )
        
        print(f"Loading embedded chunks from: {master_file.name}")
        
        with open(master_file, 'r', encoding='utf-8') as f:
            chunks = json.load(f)
        
        print(f"Loaded {len(chunks)} embedded chunks")
        return chunks
    
    def prepare_chunk_for_storage(self, chunk: Dict[str, Any]) -> Tuple[str, List[float], str, Dict[str, Any]]:
        """
        Prepare a chunk for ChromaDB storage.
        
        Args:
            chunk: Chunk dictionary with embedding
            
        Returns:
            Tuple of (id, embedding, document_text, metadata)
        """
        # Extract embedding
        embedding = chunk.get('embedding')
        if not embedding:
            raise ValueError(f"Chunk {chunk.get('chunk_id')} missing embedding")
        
        # Prepare metadata (ChromaDB doesn't support nested dicts or lists in metadata)
        metadata = {
            "chunk_id": chunk['chunk_id'],
            "document_type": chunk['document_type'],
            "section_number": chunk['section_number'],
            "section_title": chunk['section_title'],
            "chunk_index": chunk['chunk_index'],
            "token_count": chunk['token_count'],
            "word_count": chunk['word_count'],
            
            # Legal metadata
            "offense_type": chunk.get('offense_type', 'unknown'),
            "punishment_severity": chunk.get('punishment_severity', 'unknown'),
            "involves_imprisonment": str(chunk.get('involves_imprisonment', False)),
            "involves_fine": str(chunk.get('involves_fine', False)),
            "keywords": ','.join(chunk.get('keywords', [])),  # Convert list to comma-separated string
            
            # Embedding metadata
            "embedding_model": chunk.get('embedding_model', 'unknown'),
            "embedded_at": chunk.get('embedded_at', '')
        }
        
        # Document text
        document_text = chunk['text']
        
        # ID
        chunk_id = chunk['chunk_id']
        
        return chunk_id, embedding, document_text, metadata
    
    def ingest_chunks(self, batch_size: int = 100) -> Dict[str, Any]:
        """
        Ingest all embedded chunks into ChromaDB.
        
        Args:
            batch_size: Number of chunks to insert per batch
            
        Returns:
            Ingestion statistics
        """
        if not self.collection:
            raise ValueError("Collection not initialized. Call create_collection() first.")
        
        print("\n" + "="*60)
        print("INGESTING CHUNKS INTO CHROMADB")
        print("="*60)
        
        # Load chunks
        chunks = self.load_embedded_chunks()
        total_chunks = len(chunks)
        
        print(f"Preparing to ingest {total_chunks} chunks...")
        
        # Prepare data in batches
        ingested_count = 0
        failed_count = 0
        
        for i in range(0, total_chunks, batch_size):
            batch = chunks[i:i + batch_size]
            batch_num = (i // batch_size) + 1
            total_batches = (total_chunks + batch_size - 1) // batch_size
            
            print(f"Processing batch {batch_num}/{total_batches} ({len(batch)} chunks)...")
            
            try:
                # Prepare batch data
                ids = []
                embeddings = []
                documents = []
                metadatas = []
                
                for chunk in batch:
                    chunk_id, embedding, document, metadata = self.prepare_chunk_for_storage(chunk)
                    ids.append(chunk_id)
                    embeddings.append(embedding)
                    documents.append(document)
                    metadatas.append(metadata)
                
                # Add to collection
                self.collection.add(
                    ids=ids,
                    embeddings=embeddings,
                    documents=documents,
                    metadatas=metadatas
                )
                
                ingested_count += len(batch)
                print(f"  ✓ Batch {batch_num} ingested successfully")
                
            except Exception as e:
                print(f"  ✗ Error in batch {batch_num}: {e}")
                failed_count += len(batch)
        
        # Get final count
        final_count = self.collection.count()
        
        stats = {
            "total_chunks": total_chunks,
            "ingested_count": ingested_count,
            "failed_count": failed_count,
            "final_db_count": final_count,
            "ingested_at": datetime.now().isoformat()
        }
        
        print("\n" + "="*60)
        print("INGESTION SUMMARY")
        print("="*60)
        print(f"Total chunks: {stats['total_chunks']:,}")
        print(f"Successfully ingested: {stats['ingested_count']:,}")
        print(f"Failed: {stats['failed_count']}")
        print(f"Final database count: {stats['final_db_count']:,}")
        
        # Save stats
        stats_file = self.persist_dir / "ingestion_stats.json"
        with open(stats_file, 'w', encoding='utf-8') as f:
            json.dump(stats, f, indent=2)
        
        return stats
    
    def query(
        self,
        query_text: str,
        n_results: int = 5,
        filter_metadata: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        """
        Query the vector store for similar documents.
        
        Args:
            query_text: Query string
            n_results: Number of results to return
            filter_metadata: Optional metadata filters
            
        Returns:
            Query results with documents, distances, and metadata
        """
        if not self.collection:
            raise ValueError("Collection not initialized")
        
        results = self.collection.query(
            query_texts=[query_text],
            n_results=n_results,
            where=filter_metadata
        )
        
        return results
    
    def get_collection_stats(self) -> Dict[str, Any]:
        """
        Get statistics about the collection.
        
        Returns:
            Collection statistics
        """
        if not self.collection:
            return {"error": "Collection not initialized"}
        
        count = self.collection.count()
        
        # Get sample to analyze
        sample = self.collection.peek(limit=10)
        
        # Extract document types
        doc_types = {}
        if sample and 'metadatas' in sample:
            for metadata in sample['metadatas']:
                doc_type = metadata.get('document_type', 'unknown')
                doc_types[doc_type] = doc_types.get(doc_type, 0) + 1
        
        stats = {
            "total_documents": count,
            "collection_name": self.collection.name,
            "sample_document_types": doc_types,
            "persist_directory": str(self.persist_dir)
        }
        
        return stats
    
    def test_retrieval(self, test_queries: List[str] = None) -> None:
        """
        Test retrieval with sample queries.
        
        Args:
            test_queries: List of test query strings
        """
        if not test_queries:
            test_queries = [
                "What is the punishment for murder?",
                "Is theft a bailable offense?",
                "What are the penalties for drunk driving?",
                "Punishment for dowry harassment"
            ]
        
        print("\n" + "="*60)
        print("TESTING RETRIEVAL")
        print("="*60)
        
        for i, query in enumerate(test_queries, 1):
            print(f"\n{i}. Query: '{query}'")
            print("-" * 60)
            
            try:
                results = self.query(query, n_results=3)
                
                if results and 'documents' in results and results['documents']:
                    for j, (doc, metadata, distance) in enumerate(zip(
                        results['documents'][0],
                        results['metadatas'][0],
                        results['distances'][0]
                    ), 1):
                        print(f"\n   Result {j} (similarity: {1 - distance:.3f}):")
                        print(f"   Section: {metadata['section_number']} - {metadata['section_title']}")
                        print(f"   Type: {metadata['document_type']} | Severity: {metadata['punishment_severity']}")
                        print(f"   Text: {doc[:150]}...")
                else:
                    print("   No results found")
                    
            except Exception as e:
                print(f"   Error: {e}")


def main():
    """Main execution function."""
    # Initialize vector store
    vector_store = LegalVectorStore()
    
    # Create collection (reset=True to start fresh)
    vector_store.create_collection(collection_name="indian_laws", reset=True)
    
    # Ingest chunks
    stats = vector_store.ingest_chunks(batch_size=100)
    
    # Get collection stats
    print("\n" + "="*60)
    print("COLLECTION STATISTICS")
    print("="*60)
    collection_stats = vector_store.get_collection_stats()
    for key, value in collection_stats.items():
        print(f"{key}: {value}")
    
    # Test retrieval
    vector_store.test_retrieval()
    
    print("\n" + "="*60)
    print("NEXT STEPS:")
    print("="*60)
    print("1. ✓ Embeddings generated")
    print("2. ✓ ChromaDB vector store created")
    print("3. → Build RAG retrieval pipeline with LangChain")
    print("4. → Implement severity classification")
    print("5. → Create FastAPI backend")


if __name__ == "__main__":
    main()
