#!/usr/bin/env python3
"""
Build Clean Vector Database
"""

import json
from pathlib import Path
import chromadb
from chromadb.config import Settings


def build_database():
    """Build ChromaDB with clean data."""
    print(f"\n{'='*70}")
    print("BUILDING CLEAN VECTOR DATABASE")
    print(f"{'='*70}\n")
    
    # Load embedded chunks
    embeddings_file = Path("data/embeddings_clean/all_clean_embedded.json")
    
    if not embeddings_file.exists():
        print("✗ No embedded chunks found!")
        return False
    
    print(f"Loading chunks from: {embeddings_file.name}")
    with open(embeddings_file, 'r', encoding='utf-8') as f:
        chunks = json.load(f)
    
    print(f"Loaded {len(chunks):,} chunks")
    
    # Initialize ChromaDB
    db_path = Path("data/chroma_db_clean")
    db_path.mkdir(parents=True, exist_ok=True)
    
    print(f"\nInitializing ChromaDB at: {db_path}")
    client = chromadb.PersistentClient(
        path=str(db_path),
        settings=Settings(anonymized_telemetry=False, allow_reset=True)
    )
    
    # Delete old collection
    try:
        client.delete_collection("indian_laws")
        print("Deleted old collection")
    except:
        pass
    
    # Create new collection
    collection = client.create_collection(
        name="indian_laws",
        metadata={"hnsw:space": "cosine"}
    )
    print("Created new collection")
    
    # Prepare data
    print(f"\nIngesting {len(chunks):,} chunks...")
    
    ids = []
    embeddings = []
    documents = []
    metadatas = []
    seen_ids = set()
    
    for chunk in chunks:
        if 'embedding' not in chunk or not chunk['embedding']:
            continue
        
        # Handle duplicates
        chunk_id = chunk['chunk_id']
        if chunk_id in seen_ids:
            counter = 1
            while f"{chunk_id}_dup{counter}" in seen_ids:
                counter += 1
            chunk_id = f"{chunk_id}_dup{counter}"
        
        seen_ids.add(chunk_id)
        
        # Prepare metadata
        metadata = {
            "chunk_id": chunk_id,
            "document_type": chunk['document_type'],
            "section_number": chunk['section_number'],
            "section_title": chunk['section_title'],
            "chunk_index": chunk['chunk_index'],
            "token_count": chunk['token_count'],
            "word_count": chunk['word_count'],
            "offense_type": chunk.get('offense_type', 'unknown'),
            "punishment_severity": chunk.get('punishment_severity', 'unknown'),
            "involves_imprisonment": str(chunk.get('involves_imprisonment', False)),
            "involves_fine": str(chunk.get('involves_fine', False)),
            "bailable": str(chunk.get('bailable', 'unknown')),
            "cognizable": str(chunk.get('cognizable', 'unknown')),
            "maximum_punishment_years": chunk.get('maximum_punishment_years', 0) or 0,
            "keywords": ','.join(chunk.get('keywords', []))
        }
        
        ids.append(chunk_id)
        embeddings.append(chunk['embedding'])
        documents.append(chunk['text'])
        metadatas.append(metadata)
    
    # Add in batches
    batch_size = 1000
    for i in range(0, len(ids), batch_size):
        batch_end = min(i + batch_size, len(ids))
        print(f"  Batch {i//batch_size + 1}/{(len(ids) + batch_size - 1)//batch_size}...", end='\r')
        
        collection.add(
            ids=ids[i:batch_end],
            embeddings=embeddings[i:batch_end],
            documents=documents[i:batch_end],
            metadatas=metadatas[i:batch_end]
        )
    
    print(f"\n✓ Ingested {len(ids):,} chunks")
    
    # Verify
    count = collection.count()
    print(f"✓ Database contains {count:,} documents")
    
    # Test query
    print("\nTesting retrieval...")
    results = collection.query(
        query_texts=["punishment for murder"],
        n_results=3
    )
    
    if results['documents']:
        print("✓ Retrieval working!")
        print("\nSample results:")
        for i, (doc, meta) in enumerate(zip(results['documents'][0][:3], results['metadatas'][0][:3]), 1):
            print(f"  {i}. {meta['document_type'].upper()} Section {meta['section_number']}")
            print(f"     {doc[:80]}...")
    
    print(f"\n{'='*70}")
    print("DATABASE BUILD COMPLETE")
    print(f"{'='*70}")
    print(f"Location: {db_path}")
    print(f"Collection: indian_laws")
    print(f"Documents: {count:,}")
    
    return True


if __name__ == "__main__":
    success = build_database()
    if not success:
        exit(1)
