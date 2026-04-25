#!/usr/bin/env python3
"""
RAG Pipeline for Legal Q&A System - Gemini Version

Uses Google Gemini instead of OpenAI.
"""

import os
from typing import Dict, List, Any, Optional
from pathlib import Path
import chromadb
from langchain.prompts import PromptTemplate
from langchain_community.vectorstores import Chroma
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.chains import RetrievalQA
from langchain.schema import Document

from severity_classifier import SeverityClassifier, SeverityLevel


class LegalRAGPipelineGemini:
    """RAG pipeline for legal document Q&A using Gemini."""
    
    def __init__(
        self,
        chroma_persist_dir: str = "data/chroma_db",
        collection_name: str = "indian_laws",
        model_name: str = "gemini-1.5-flash",
        embedding_model: str = "sentence-transformers/all-MiniLM-L6-v2",
        google_api_key: Optional[str] = None
    ):
        """
        Initialize RAG pipeline with Gemini.
        
        Args:
            chroma_persist_dir: ChromaDB persistence directory
            collection_name: Name of the collection
            model_name: Gemini model name
            embedding_model: Embedding model name
            google_api_key: Google API key (or set GOOGLE_API_KEY env var)
        """
        self.chroma_persist_dir = Path(chroma_persist_dir)
        self.collection_name = collection_name
        self.model_name = model_name
        
        print("Initializing Legal RAG Pipeline (Gemini)...")
        
        # Set API key
        if google_api_key:
            os.environ["GOOGLE_API_KEY"] = google_api_key
        
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
        print(f"Initializing Gemini: {model_name}")
        self.llm = self._initialize_llm(model_name)
        
        # Initialize severity classifier
        self.severity_classifier = SeverityClassifier()
        
        # Create retrieval chain
        self.qa_chain = self._create_qa_chain()
        
        print("✓ RAG Pipeline initialized successfully")
    
    def _initialize_llm(self, model_name: str):
        """
        Initialize Gemini LLM.
        
        Args:
            model_name: Model identifier
            
        Returns:
            LLM instance
        """
        api_key = os.getenv("GOOGLE_API_KEY")
        if not api_key:
            raise ValueError(
                "GOOGLE_API_KEY not found in environment. "
                "Set it with: export GOOGLE_API_KEY='your-key'"
            )
        
        # Use the correct model name format
        return ChatGoogleGenerativeAI(
            model="gemini-1.5-flash-latest",
            temperature=0.1,  # Low temperature for factual responses
            max_output_tokens=1000,
            google_api_key=api_key,
            convert_system_message_to_human=True  # Required for Gemini
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
            chain_type="stuff",
            retriever=self.vectorstore.as_retriever(
                search_kwargs={"k": 5}
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
        """Extract citations from source documents."""
        citations = []
        seen = set()
        
        for doc in source_documents:
            metadata = doc.metadata
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
        """Determine severity from source documents."""
        if not source_documents:
            return {
                "level": SeverityLevel.UNKNOWN.value,
                "reasoning": "No relevant documents found",
                "confidence": 0.0,
                "summary": self.severity_classifier.get_severity_summary(SeverityLevel.UNKNOWN)
            }
        
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
            Response dictionary
        """
        print(f"\nProcessing query: '{question}'")
        
        try:
            result = self.qa_chain({"query": question})
            
            answer = result.get("result", "")
            source_documents = result.get("source_documents", [])
            
            citations = self.extract_citations(source_documents)
            severity = self.determine_severity(source_documents)
            
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
        """Format response for display."""
        output = []
        output.append("="*60)
        output.append(f"QUESTION: {response['question']}")
        output.append("="*60)
        
        output.append("\nANSWER:")
        output.append(response['answer'])
        
        severity = response['severity']
        # Handle case where summary might be missing (error case)
        if 'summary' in severity:
            output.append(f"\nSEVERITY: {severity['summary']['icon']} {severity['level']}")
            output.append(f"Reasoning: {severity['reasoning']}")
            output.append(f"Confidence: {severity['confidence']:.0%}")
            output.append(f"Action: {severity['summary']['action']}")
        else:
            output.append(f"\nSEVERITY: {severity['level']}")
            output.append(f"Reasoning: {severity['reasoning']}")
        
        if response['citations']:
            output.append(f"\nSOURCES ({len(response['citations'])}):")
            for i, citation in enumerate(response['citations'], 1):
                output.append(f"{i}. {citation['act']} - Section {citation['section']}: {citation['title']}")
                output.append(f"   \"{citation['text_snippet']}\"")
        
        output.append(f"\n{response['disclaimer']}")
        output.append("="*60)
        
        return "\n".join(output)


def main():
    """Main execution function for testing."""
    print("Legal RAG Pipeline - Gemini Version")
    print("="*60)
    
    # Set API key
    api_key = "AIzaSyDd-lZhiaMojYL8_QMlt6s0PeAoClJipAA"
    
    try:
        pipeline = LegalRAGPipelineGemini(google_api_key=api_key)
    except Exception as e:
        print(f"Error initializing pipeline: {e}")
        print("\nMake sure ChromaDB is populated (run vector_store.py)")
        return
    
    # Test query
    test_query = "What is the punishment for murder in India?"
    
    print(f"\nTesting with query: '{test_query}'")
    response = pipeline.query(test_query)
    print(pipeline.format_response(response))


if __name__ == "__main__":
    main()
