#!/usr/bin/env python3
"""
Build database from manually curated sections
"""

import json
from pathlib import Path
from sentence_transformers import SentenceTransformer
import chromadb
from chromadb.config import Settings
from tqdm import tqdm

print("="*70)
print("BUILDING DATABASE FROM MANUAL SECTIONS")
print("="*70)

# Load manual sections
manual_file = Path("data/manual_sections/ipc_critical_sections.json")
with open(manual_file) as f:
    sections = json.load(f)

print(f"\nLoaded {len(sections)} manually curated sections")

# Create chunks (keep sections whole for now)
chunks = []
for section in sections:
    chunk = {
        "chunk_id": f"ipc_manual_{section['section_number']}_chunk_000",
        "document_type": "ipc",
        "section_number": section['section_number'],
        "section_title": section['section_title'],
        "chunk_index": 0,
        "total_chunks": 1,
        "text": f"{section['section_number']}. {section['section_title']}. {section['content']}",
        "token_count": len(section['content'].split()),
        "word_count": len(section['content'].split()),
        **{k: v for k, v in section.items() if k not in ['section_number', 'section_title', 'content']}
    }
    chunks.append(chunk)

print(f"Created {len(chunks)} chunks")

# Generate embeddings
print("\nLoading embedding model...")
model = SentenceTransformer('sentence-transformers/all-MiniLM-L6-v2')

print("Generating embeddings...")
texts = [chunk['text'] for chunk in chunks]
embeddings = model.encode(texts, normalize_embeddings=True, show_progress_bar=True)

for chunk, embedding in zip(chunks, embeddings):
    chunk['embedding'] = embedding.tolist()

print("✓ Embeddings generated")

# Build ChromaDB
print("\nBuilding ChromaDB...")
db_path = Path("data/chroma_db_manual")
db_path.mkdir(parents=True, exist_ok=True)

client = chromadb.PersistentClient(
    path=str(db_path),
    settings=Settings(anonymized_telemetry=False, allow_reset=True)
)

# Delete old collection
try:
    client.delete_collection("indian_laws")
except:
    pass

# Create new collection
collection = client.create_collection(
    name="indian_laws",
    metadata={"hnsw:space": "cosine"}
)

# Add chunks
ids = []
embeddings_list = []
documents = []
metadatas = []

for chunk in chunks:
    metadata = {
        "chunk_id": chunk['chunk_id'],
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
    
    ids.append(chunk['chunk_id'])
    embeddings_list.append(chunk['embedding'])
    documents.append(chunk['text'])
    metadatas.append(metadata)

collection.add(
    ids=ids,
    embeddings=embeddings_list,
    documents=documents,
    metadatas=metadatas
)

print(f"✓ Added {len(ids)} documents to database")

# Test retrieval
print("\nTesting retrieval...")
test_queries = [
    "punishment for murder",
    "causing death by negligence accident",
    "theft stolen property",
    "assault hurt with weapon",
    "defamation false accusation",
    "cheating fraud"
]

for query in test_queries:
    results = collection.query(
        query_texts=[query],
        n_results=2
    )
    
    print(f"\nQuery: '{query}'")
    for i, (doc, meta) in enumerate(zip(results['documents'][0], results['metadatas'][0]), 1):
        print(f"  {i}. Section {meta['section_number']}: {meta['section_title']}")
        print(f"     Severity: {meta['punishment_severity']}, Bailable: {meta['bailable']}")

print("\n" + "="*70)
print("DATABASE BUILD COMPLETE")
print("="*70)
print(f"Location: {db_path}")
print(f"Documents: {collection.count()}")
print("\nNext: Update API to use this database and re-test!")
