#!/usr/bin/env python3
"""
Inspect what's actually in the database
"""

import chromadb
from pathlib import Path

# Connect to new database
db_path = Path("data/chroma_db_v2")
client = chromadb.PersistentClient(path=str(db_path))
collection = client.get_collection("indian_laws")

print(f"Total documents: {collection.count():,}\n")

# Test specific queries
test_queries = [
    "punishment for murder",
    "theft stolen property",
    "assault hurt grievous",
    "negligent driving accident death",
    "drunk driving alcohol"
]

for query in test_queries:
    print(f"\nQuery: '{query}'")
    print("="*60)
    
    results = collection.query(
        query_texts=[query],
        n_results=3
    )
    
    for i, (doc, meta) in enumerate(zip(results['documents'][0], results['metadatas'][0]), 1):
        print(f"\n{i}. {meta['document_type'].upper()} Section {meta['section_number']}")
        print(f"   Title: {meta['section_title'][:60]}...")
        print(f"   Text: {doc[:150]}...")
        print(f"   Severity: {meta['punishment_severity']}")
        print(f"   Keywords: {meta.get('keywords', 'none')}")
