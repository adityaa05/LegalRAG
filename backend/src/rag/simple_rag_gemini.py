#!/usr/bin/env python3
"""
Simple RAG with Gemini - Direct API approach

Bypasses LangChain to use Google's Generative AI SDK directly.
"""

import os
from pathlib import Path
from typing import List, Dict, Any
import chromadb
from sentence_transformers import SentenceTransformer
import google.generativeai as genai


class SimpleRAGGemini:
    """Simple RAG using Gemini API directly."""
    
    def __init__(self, api_key: str):
        """Initialize with Gemini API key."""
        # Configure Gemini
        genai.configure(api_key=api_key)
        # Try different model names - v1 API uses 'models/' prefix
        try:
            self.model = genai.GenerativeModel('models/gemini-1.5-flash')
        except:
            try:
                self.model = genai.GenerativeModel('gemini-pro')
            except:
                self.model = genai.GenerativeModel('models/gemini-pro')
        
        # Load embedding model
        print("Loading embedding model...")
        self.embedder = SentenceTransformer('sentence-transformers/all-MiniLM-L6-v2')
        
        # Connect to ChromaDB
        print("Connecting to ChromaDB...")
        self.chroma_client = chromadb.PersistentClient(path="data/chroma_db")
        self.collection = self.chroma_client.get_collection("indian_laws")
        
        print(f"✓ Connected! Database has {self.collection.count()} documents")
    
    def retrieve_context(self, query: str, n_results: int = 5) -> List[Dict[str, Any]]:
        """Retrieve relevant chunks from ChromaDB."""
        # Generate query embedding
        query_embedding = self.embedder.encode(query, normalize_embeddings=True).tolist()
        
        # Search ChromaDB
        results = self.collection.query(
            query_embeddings=[query_embedding],
            n_results=n_results
        )
        
        # Format results
        contexts = []
        for i in range(len(results['documents'][0])):
            contexts.append({
                'text': results['documents'][0][i],
                'metadata': results['metadatas'][0][i],
                'distance': results['distances'][0][i]
            })
        
        return contexts
    
    def generate_answer(self, query: str, contexts: List[Dict[str, Any]]) -> str:
        """Generate answer using Gemini."""
        # Build context string
        context_str = "\n\n".join([
            f"[Source: {ctx['metadata'].get('document_type', 'unknown').upper()} - Section {ctx['metadata'].get('section_number', 'unknown')}]\n{ctx['text']}"
            for ctx in contexts
        ])
        
        # Create prompt
        prompt = f"""You are a legal information assistant for Indian law. Use ONLY the law snippets below to answer the question.

Context from Indian Law:
{context_str}

Question: {query}

Instructions:
1. Use ONLY the law snippets provided above
2. Quote relevant law text as evidence
3. Provide a concise answer (3-5 sentences)
4. List the sources used (Act and Section numbers)
5. End with: "This is legal information only, not legal advice. Consult a qualified lawyer."

Answer:"""
        
        # Generate response
        try:
            response = self.model.generate_content(prompt)
            return response.text
        except Exception as e:
            return f"Error generating answer: {e}"
    
    def query(self, question: str) -> Dict[str, Any]:
        """Full RAG query."""
        print(f"\nQuery: {question}")
        print("-" * 60)
        
        # Retrieve
        print("Retrieving relevant documents...")
        contexts = self.retrieve_context(question)
        
        print(f"Found {len(contexts)} relevant chunks")
        for i, ctx in enumerate(contexts[:3], 1):
            print(f"  {i}. {ctx['metadata'].get('document_type', 'unknown').upper()} - Section {ctx['metadata'].get('section_number', 'unknown')}")
        
        # Generate
        print("\nGenerating answer with Gemini...")
        answer = self.generate_answer(question, contexts)
        
        return {
            'question': question,
            'answer': answer,
            'sources': contexts
        }
    
    def format_response(self, response: Dict[str, Any]) -> str:
        """Format response for display."""
        output = []
        output.append("=" * 60)
        output.append(f"QUESTION: {response['question']}")
        output.append("=" * 60)
        output.append(f"\nANSWER:\n{response['answer']}")
        output.append("\n" + "=" * 60)
        output.append(f"SOURCES ({len(response['sources'])}):")
        for i, src in enumerate(response['sources'][:5], 1):
            meta = src['metadata']
            output.append(f"{i}. {meta.get('document_type', 'unknown').upper()} - Section {meta.get('section_number', 'unknown')}: {meta.get('section_title', '')[:60]}...")
        output.append("=" * 60)
        
        return "\n".join(output)


def main():
    """Test the simple RAG."""
    api_key = "AIzaSyDd-lZhiaMojYL8_QMlt6s0PeAoClJipAA"
    
    print("Simple RAG with Gemini")
    print("=" * 60)
    
    # Initialize
    rag = SimpleRAGGemini(api_key)
    
    # Test queries
    test_queries = [
        "What is the punishment for murder in India?",
        "Is theft a bailable offense?",
        "What are the penalties for drunk driving?"
    ]
    
    for query in test_queries:
        response = rag.query(query)
        print("\n" + rag.format_response(response))
        print("\n")


if __name__ == "__main__":
    main()
