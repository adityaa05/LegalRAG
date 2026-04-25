#!/usr/bin/env python3
"""
Embedding Generator for Legal RAG System

Generates vector embeddings for legal text chunks using sentence-transformers.
"""

import json
from pathlib import Path
from typing import Dict, List, Any
from datetime import datetime
import numpy as np
from sentence_transformers import SentenceTransformer
from tqdm import tqdm


class LegalEmbedder:
    """Generate embeddings for legal text chunks."""
    
    def __init__(self, model_name: str = "sentence-transformers/all-MiniLM-L6-v2"):
        """
        Initialize embedder with specified model.
        
        Args:
            model_name: HuggingFace model identifier
        """
        print(f"Loading embedding model: {model_name}")
        self.model = SentenceTransformer(model_name)
        self.model_name = model_name
        self.embedding_dim = self.model.get_sentence_embedding_dimension()
        
        # Prefer improved pipeline directories when present
        improved_chunks = Path("data/chunks_v2")
        improved_embeddings = Path("data/embeddings_v2")

        if improved_chunks.exists():
            self.chunks_dir = improved_chunks
            print(f"Using improved chunks directory: {self.chunks_dir}")
        else:
            self.chunks_dir = Path("data/chunks")

        if improved_embeddings.exists() or improved_chunks.exists():
            self.embeddings_dir = improved_embeddings
        else:
            self.embeddings_dir = Path("data/embeddings")

        self.embeddings_dir.mkdir(parents=True, exist_ok=True)
        
        print(f"Model loaded. Embedding dimension: {self.embedding_dim}")
    
    def generate_embeddings_batch(self, texts: List[str], batch_size: int = 32) -> np.ndarray:
        """
        Generate embeddings for a batch of texts.
        
        Args:
            texts: List of text strings to embed
            batch_size: Batch size for encoding
            
        Returns:
            numpy array of embeddings
        """
        embeddings = self.model.encode(
            texts,
            batch_size=batch_size,
            show_progress_bar=True,
            convert_to_numpy=True,
            normalize_embeddings=True  # Normalize for cosine similarity
        )
        return embeddings
    
    def process_chunks_file(self, chunks_file: Path) -> Dict[str, Any]:
        """
        Process a chunks file and generate embeddings.
        
        Args:
            chunks_file: Path to chunks JSON file
            
        Returns:
            Statistics about the embedding generation
        """
        print(f"\nProcessing: {chunks_file.name}")
        
        # Load chunks
        with open(chunks_file, 'r', encoding='utf-8') as f:
            chunks = json.load(f)
        
        print(f"Loaded {len(chunks)} chunks")
        
        # Extract texts
        texts = [chunk['text'] for chunk in chunks]
        
        # Generate embeddings
        print("Generating embeddings...")
        embeddings = self.generate_embeddings_batch(texts)
        
        # Add embeddings to chunks
        for i, chunk in enumerate(chunks):
            chunk['embedding'] = embeddings[i].tolist()
            chunk['embedding_model'] = self.model_name
            chunk['embedding_dim'] = self.embedding_dim
            chunk['embedded_at'] = datetime.now().isoformat()
        
        # Save embedded chunks
        doc_type = chunks_file.stem.replace('_chunks', '')
        output_file = self.embeddings_dir / f"{doc_type}_embedded.json"
        
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(chunks, f, indent=2, ensure_ascii=False)
        
        print(f"Saved embeddings to: {output_file.name}")
        
        # Calculate statistics
        embedding_size_mb = embeddings.nbytes / (1024 * 1024)
        
        stats = {
            "document_type": doc_type,
            "total_chunks": len(chunks),
            "embedding_dimension": self.embedding_dim,
            "embedding_size_mb": round(embedding_size_mb, 2),
            "model_name": self.model_name,
            "output_file": str(output_file.name)
        }
        
        return stats
    
    def process_all_chunks(self) -> Dict[str, Any]:
        """
        Process all chunk files and generate embeddings.
        
        Returns:
            Summary statistics
        """
        print("="*60)
        print("LEGAL TEXT EMBEDDING GENERATOR")
        print("="*60)
        
        # Find all chunk files
        chunk_files = list(self.chunks_dir.glob("*_chunks.json"))
        
        if not chunk_files:
            print("No chunk files found!")
            return {"success": False, "error": "No chunk files found"}
        
        print(f"Found {len(chunk_files)} chunk files")
        
        results = []
        total_chunks = 0
        total_size_mb = 0
        
        for chunk_file in chunk_files:
            try:
                stats = self.process_chunks_file(chunk_file)
                results.append(stats)
                total_chunks += stats['total_chunks']
                total_size_mb += stats['embedding_size_mb']
            except Exception as e:
                print(f"Error processing {chunk_file.name}: {e}")
                results.append({
                    "document_type": chunk_file.stem,
                    "error": str(e)
                })
        
        # Create master embedded file
        print("\nCreating master embedded file...")
        all_embedded_chunks = []
        
        for embedded_file in self.embeddings_dir.glob("*_embedded.json"):
            with open(embedded_file, 'r', encoding='utf-8') as f:
                chunks = json.load(f)
                all_embedded_chunks.extend(chunks)
        
        master_file = self.embeddings_dir / "all_legal_embedded.json"
        with open(master_file, 'w', encoding='utf-8') as f:
            json.dump(all_embedded_chunks, f, indent=2, ensure_ascii=False)
        
        print(f"Master file created: {master_file.name}")
        
        # Generate summary
        summary = {
            "total_documents": len(chunk_files),
            "total_chunks_embedded": total_chunks,
            "embedding_dimension": self.embedding_dim,
            "total_embedding_size_mb": round(total_size_mb, 2),
            "model_name": self.model_name,
            "processed_at": datetime.now().isoformat(),
            "results": results
        }
        
        # Save summary
        summary_file = self.embeddings_dir / "embedding_summary.json"
        with open(summary_file, 'w', encoding='utf-8') as f:
            json.dump(summary, f, indent=2, ensure_ascii=False)
        
        # Print summary
        print("\n" + "="*60)
        print("EMBEDDING GENERATION SUMMARY")
        print("="*60)
        print(f"Documents processed: {summary['total_documents']}")
        print(f"Total chunks embedded: {summary['total_chunks_embedded']:,}")
        print(f"Embedding dimension: {summary['embedding_dimension']}")
        print(f"Total size: {summary['total_embedding_size_mb']:.2f} MB")
        print(f"Model: {summary['model_name']}")
        print(f"\nFiles saved to: {self.embeddings_dir}")
        
        return summary
    
    def verify_embeddings(self, sample_size: int = 5) -> None:
        """
        Verify embeddings by checking a sample.
        
        Args:
            sample_size: Number of samples to verify
        """
        print("\nVerifying embeddings...")
        
        master_file = self.embeddings_dir / "all_legal_embedded.json"
        if not master_file.exists():
            print("Master embedded file not found!")
            return
        
        with open(master_file, 'r', encoding='utf-8') as f:
            chunks = json.load(f)
        
        print(f"Total chunks: {len(chunks)}")
        
        # Check sample
        import random
        samples = random.sample(chunks, min(sample_size, len(chunks)))
        
        print(f"\nSample verification ({sample_size} chunks):")
        for i, chunk in enumerate(samples, 1):
            has_embedding = 'embedding' in chunk and chunk['embedding'] is not None
            embedding_len = len(chunk.get('embedding', [])) if has_embedding else 0
            
            print(f"{i}. {chunk['chunk_id']}")
            print(f"   Text length: {len(chunk['text'])} chars")
            print(f"   Has embedding: {has_embedding}")
            print(f"   Embedding dimension: {embedding_len}")
            print(f"   Section: {chunk['section_number']} - {chunk['section_title'][:50]}...")
            
            if has_embedding and embedding_len != self.embedding_dim:
                print(f"   ⚠️  WARNING: Expected {self.embedding_dim}, got {embedding_len}")
        
        print("\n✓ Verification complete")


def main():
    """Main execution function."""
    embedder = LegalEmbedder()
    
    # Generate embeddings
    summary = embedder.process_all_chunks()
    
    # Verify
    embedder.verify_embeddings(sample_size=5)
    
    print("\n" + "="*60)
    print("NEXT STEPS:")
    print("="*60)
    print("1. ✓ Embeddings generated")
    print("2. → Create ChromaDB vector database")
    print("3. → Build RAG retrieval pipeline")
    print("4. → Implement severity classification")
    print("5. → Create FastAPI backend")


if __name__ == "__main__":
    main()
