#!/usr/bin/env python3
"""
Embed Clean Chunks
"""

import json
from pathlib import Path
from sentence_transformers import SentenceTransformer
from tqdm import tqdm
from datetime import datetime


def embed_chunks():
    """Generate embeddings for clean chunks."""
    print(f"\n{'='*70}")
    print("EMBEDDING GENERATION")
    print(f"{'='*70}\n")
    
    # Load chunks
    chunks_file = Path("data/chunks_clean/all_clean_chunks.json")
    if not chunks_file.exists():
        print("✗ No chunks found!")
        return False
    
    print(f"Loading chunks from: {chunks_file.name}")
    with open(chunks_file, 'r', encoding='utf-8') as f:
        chunks = json.load(f)
    
    print(f"Loaded {len(chunks):,} chunks")
    
    # Load model
    print("\nLoading embedding model...")
    model = SentenceTransformer('sentence-transformers/all-MiniLM-L6-v2')
    print("✓ Model loaded")
    
    # Generate embeddings
    print("\nGenerating embeddings...")
    texts = [chunk['text'] for chunk in chunks]
    
    batch_size = 32
    embeddings = []
    
    for i in tqdm(range(0, len(texts), batch_size), desc="Batches"):
        batch = texts[i:i+batch_size]
        batch_embeddings = model.encode(batch, normalize_embeddings=True)
        embeddings.extend(batch_embeddings.tolist())
    
    # Add embeddings to chunks
    for chunk, embedding in zip(chunks, embeddings):
        chunk['embedding'] = embedding
        chunk['embedded_at'] = datetime.now().isoformat()
        chunk['embedding_model'] = 'sentence-transformers/all-MiniLM-L6-v2'
    
    # Save
    output_dir = Path("data/embeddings_clean")
    output_dir.mkdir(parents=True, exist_ok=True)
    
    output_file = output_dir / "all_clean_embedded.json"
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(chunks, f, indent=2, ensure_ascii=False)
    
    print(f"\n✓ Saved {len(chunks):,} embedded chunks")
    print(f"✓ Output: {output_file}")
    
    return True


if __name__ == "__main__":
    success = embed_chunks()
    if not success:
        exit(1)
