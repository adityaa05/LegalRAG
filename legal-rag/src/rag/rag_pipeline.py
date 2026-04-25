#!/usr/bin/env python3
"""
RAG Pipeline for Legal Q&A System

Retrieval-Augmented Generation pipeline using LangChain and ChromaDB.
"""

import os
from typing import Dict, List, Any, Optional
from pathlib import Path
import chromadb
from langchain.prompts import PromptTemplate
from langchain_community.vectorstores import Chroma
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_openai import ChatOpenAI
from langchain.chains import RetrievalQA
from langchain.schema import Document

from severity_classifier import SeverityClassifier, SeverityLevel


class LegalRAGPipeline:
    """RAG pipeline for legal document Q&A."""
    
    def __init__(
        self,
        chroma_persist_dir: str = "legal-rag/data/chroma_db",
        collection_name: str = "indian_laws",
        model_name: str = "gpt-4-turbo",
        embedding_model: str = "sentence-transformers/all-MiniLM-L6-v2"
    ):
        """
        Initialize RAG pipeline.
        
        Args:
            chroma_persist_dir: ChromaDB persistence directory
            collection_name: Name of the collection
            model_name: LLM model name (OpenAI or local)
            embedding_model: Embedding model name
        """
        self.chroma_persist_dir = Path(chroma_persist_dir)
        self.collection_name = collection_name
        self.model_name = model_name
        
        print("Initializing Legal RAG Pipeline...")
        
        # Initialize embeddings
        print(f"Loading embedding model: {embedding_model}")
        self.embeddings = HuggingFaceEmbeddings(
            model_name=embedding_model,
            model_kwargs={'device': 'cpu'},
            encode_kwargs={'normalize_embeddings': True}
        )
        
        # Initialize vector store
        print(f"Connecting to ChromaDB: {self.chroma_persist_dir}")
        self.vectorstore = Chroma(
            collection_name=collection_name,
            embedding_function=self.embeddings,
            persist_directory=str(self.chroma_persist_dir)
        )
        
        # Initialize LLM
        print(f"Initializing LLM: {model_name}")
        self.llm = self._initialize_llm(model_name)
        
        # Initialize severity classifier
        self.severity_classifier = SeverityClassifier()
        
        # Create retrieval chain
        self.qa_chain = self._create_qa_chain()
        
        print("✓ RAG Pipeline initialized successfully")
    
    def _initialize_llm(self, model_name: str):
        """
        Initialize LLM (OpenAI or local).
        
        Args:
            model_name: Model identifier
            
        Returns:
            LLM instance
        """
        # Check for OpenAI API key
        if "gpt" in model_name.lower():
            api_key = os.getenv("OPENAI_API_KEY")
            if not api_key:
                raise ValueError(
                    "OPENAI_API_KEY not found in environment. "
                    "Set it with: export OPENAI_API_KEY='your-key'"
                )
            
            return ChatOpenAI(
                model_name=model_name,
                temperature=0.1,  # Low temperature for factual responses
                max_tokens=1000
            )
        else:
            # For local models, use HuggingFace or Ollama
            raise NotImplementedError(
                f"Local model {model_name} not yet implemented. "
                "Use OpenAI models (gpt-4-turbo, gpt-3.5-turbo) for now."
            )
    
    def _create_prompt_template(self) -> PromptTemplate:
        """
        Create prompt template for legal Q&A.
        
        Returns:
            PromptTemplate instance
        """
        template = """You are a legal information assistant for Indian law. Use ONLY the retrieved law snippets below to answer the question. If the snippets do not provide a clear answer, say "Insufficient information — consult a lawyer."

Context:
{context}

Question: {question}

Instructions:
1. Use ONLY the law snippets provided above
2. Quote verbatim any law text used as evidence
3. Do NOT add any facts beyond the snippets
4. Provide a concise answer (3-6 sentences) stating whether the law likely applies
5. Include explicit caveats about limitations
6. After your answer, list the sources used (Act and Section numbers)
7. Always end with: "This is legal information only and not legal advice. Consult a qualified lawyer for your specific situation."

Answer:"""
        
        return PromptTemplate(
            template=template,
            input_variables=["context", "question"]
        )
    
    def _create_qa_chain(self):
        """
        Create RetrievalQA chain.
        
        Returns:
            RetrievalQA chain
        """
        prompt = self._create_prompt_template()
        
        chain = RetrievalQA.from_chain_type(
            llm=self.llm,
            chain_type="stuff",  # Stuff all retrieved docs into context
            retriever=self.vectorstore.as_retriever(
                search_kwargs={"k": 5}  # Retrieve top 5 chunks
            ),
            return_source_documents=True,
            chain_type_kwargs={"prompt": prompt}
        )
        
        return chain
    
    def retrieve_relevant_chunks(
        self,
        query: str,
        k: int = 5,
        filter_metadata: Optional[Dict[str, Any]] = None
    ) -> List[Document]:
        """
        Retrieve relevant chunks for a query.
        
        Args:
            query: Query string
            k: Number of chunks to retrieve
            filter_metadata: Optional metadata filters
            
        Returns:
            List of Document objects
        """
        if filter_metadata:
            retriever = self.vectorstore.as_retriever(
                search_kwargs={"k": k, "filter": filter_metadata}
            )
        else:
            retriever = self.vectorstore.as_retriever(search_kwargs={"k": k})
        
        docs = retriever.get_relevant_documents(query)
        return docs
    
    def extract_citations(self, source_documents: List[Document]) -> List[Dict[str, str]]:
        """
        Extract citations from source documents.
        
        Args:
            source_documents: List of source Document objects
            
        Returns:
            List of citation dictionaries
        """
        citations = []
        seen = set()
        
        for doc in source_documents:
            metadata = doc.metadata
            
            # Create unique identifier
            citation_id = f"{metadata.get('document_type', 'unknown')}_{metadata.get('section_number', 'unknown')}"
            
            if citation_id not in seen:
                citations.append({
                    "act": metadata.get('document_type', 'Unknown Act').upper(),
                    "section": metadata.get('section_number', 'Unknown'),
                    "title": metadata.get('section_title', ''),
                    "text_snippet": doc.page_content[:200] + "..." if len(doc.page_content) > 200 else doc.page_content
                })
                seen.add(citation_id)
        
        return citations
    
    def determine_severity(self, source_documents: List[Document]) -> Dict[str, Any]:
        """
        Determine severity from source documents.
        
        Args:
            source_documents: List of source Document objects
            
        Returns:
            Severity information dictionary
        """
        if not source_documents:
            return {
                "level": SeverityLevel.UNKNOWN.value,
                "reasoning": "No relevant documents found",
                "confidence": 0.0,
                "summary": self.severity_classifier.get_severity_summary(SeverityLevel.UNKNOWN)
            }
        
        # Use the first (most relevant) document for severity
        doc = source_documents[0]
        metadata = doc.metadata
        
        severity_level, reasoning, confidence = self.severity_classifier.classify(
            metadata=metadata,
            text=doc.page_content
        )
        
        return {
            "level": severity_level.value,
            "reasoning": reasoning,
            "confidence": confidence,
            "summary": self.severity_classifier.get_severity_summary(severity_level)
        }
    
    def query(self, question: str) -> Dict[str, Any]:
        """
        Query the RAG pipeline.
        
        Args:
            question: User question
            
        Returns:
            Response dictionary with answer, citations, and severity
        """
        print(f"\nProcessing query: '{question}'")
        
        try:
            # Run QA chain
            result = self.qa_chain({"query": question})
            
            answer = result.get("result", "")
            source_documents = result.get("source_documents", [])
            
            # Extract citations
            citations = self.extract_citations(source_documents)
            
            # Determine severity
            severity = self.determine_severity(source_documents)
            
            # Build response
            response = {
                "question": question,
                "answer": answer,
                "citations": citations,
                "severity": severity,
                "num_sources": len(source_documents),
                "disclaimer": "⚠️ This is legal information only and not legal advice. Consult a qualified lawyer for your specific situation."
            }
            
            return response
            
        except Exception as e:
            print(f"Error processing query: {e}")
            return {
                "question": question,
                "answer": f"Error: {str(e)}",
                "citations": [],
                "severity": {
                    "level": SeverityLevel.UNKNOWN.value,
                    "reasoning": "Error occurred",
                    "confidence": 0.0
                },
                "num_sources": 0,
                "disclaimer": "⚠️ An error occurred. Please try again or consult a lawyer."
            }
    
    def format_response(self, response: Dict[str, Any]) -> str:
        """
        Format response for display.
        
        Args:
            response: Response dictionary
            
        Returns:
            Formatted string
        """
        output = []
        output.append("="*60)
        output.append(f"QUESTION: {response['question']}")
        output.append("="*60)
        
        # Answer
        output.append("\nANSWER:")
        output.append(response['answer'])
        
        # Severity
        severity = response['severity']
        output.append(f"\nSEVERITY: {severity['summary']['icon']} {severity['level']}")
        output.append(f"Reasoning: {severity['reasoning']}")
        output.append(f"Confidence: {severity['confidence']:.0%}")
        output.append(f"Action: {severity['summary']['action']}")
        
        # Citations
        if response['citations']:
            output.append(f"\nSOURCES ({len(response['citations'])}):")
            for i, citation in enumerate(response['citations'], 1):
                output.append(f"{i}. {citation['act']} - Section {citation['section']}: {citation['title']}")
                output.append(f"   \"{citation['text_snippet']}\"")
        
        # Disclaimer
        output.append(f"\n{response['disclaimer']}")
        output.append("="*60)
        
        return "\n".join(output)


def main():
    """Main execution function for testing."""
    print("Legal RAG Pipeline - Test Mode")
    print("="*60)
    
    # Initialize pipeline
    try:
        pipeline = LegalRAGPipeline()
    except Exception as e:
        print(f"Error initializing pipeline: {e}")
        print("\nMake sure:")
        print("1. ChromaDB is populated (run vector_store.py)")
        print("2. OPENAI_API_KEY is set in environment")
        return
    
    # Test queries
    test_queries = [
        "What is the punishment for murder in India?",
        "Is theft a bailable offense?",
        "What are the penalties for drunk driving?",
        "Punishment for dowry harassment"
    ]
    
    print("\nRunning test queries...\n")
    
    for query in test_queries:
        response = pipeline.query(query)
        print(pipeline.format_response(response))
        print("\n")


if __name__ == "__main__":
    main()
