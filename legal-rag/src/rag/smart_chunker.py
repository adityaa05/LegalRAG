#!/usr/bin/env python3
"""
Smart Chunker - Works with clean extracted sections
"""

import json
from pathlib import Path
from typing import Dict, List, Any
from datetime import datetime


class SmartChunker:
    """Smart chunker for clean sections."""
    
    def __init__(self, chunk_size: int = 400, overlap: int = 50):
        self.chunk_size = chunk_size
        self.overlap = overlap
        self.processed_dir = Path("data/processed_clean")
        self.chunks_dir = Path("data/chunks_clean")
        self.chunks_dir.mkdir(parents=True, exist_ok=True)
    
    def estimate_tokens(self, text: str) -> int:
        """Estimate token count."""
        return int(len(text.split()) * 1.3)
    
    def chunk_section(self, section: Dict[str, Any], doc_type: str) -> List[Dict[str, Any]]:
        """Chunk a section intelligently."""
        content = section['content']
        section_num = section['section_number']
        section_title = section['section_title']
        
        total_tokens = self.estimate_tokens(content)
        
        chunks = []
        
        # If small, keep whole
        if total_tokens <= self.chunk_size:
            chunk = self._create_chunk(
                doc_type, section, section_num, section_title,
                content, 0, 1
            )
            chunks.append(chunk)
        else:
            # Split by sentences
            sentences = self._split_sentences(content)
            
            current_chunk = []
            current_tokens = 0
            chunk_index = 0
            
            for sentence in sentences:
                sentence_tokens = self.estimate_tokens(sentence)
                
                if current_tokens + sentence_tokens > self.chunk_size and current_chunk:
                    # Save chunk
                    chunk_text = ' '.join(current_chunk)
                    chunk = self._create_chunk(
                        doc_type, section, section_num, section_title,
                        chunk_text, chunk_index, -1  # Will update total later
                    )
                    chunks.append(chunk)
                    
                    # Overlap
                    overlap_sentences = current_chunk[-2:] if len(current_chunk) >= 2 else current_chunk
                    current_chunk = overlap_sentences + [sentence]
                    current_tokens = sum(self.estimate_tokens(s) for s in current_chunk)
                    chunk_index += 1
                else:
                    current_chunk.append(sentence)
                    current_tokens += sentence_tokens
            
            # Last chunk
            if current_chunk:
                chunk_text = ' '.join(current_chunk)
                chunk = self._create_chunk(
                    doc_type, section, section_num, section_title,
                    chunk_text, chunk_index, -1
                )
                chunks.append(chunk)
            
            # Update total_chunks
            for chunk in chunks:
                chunk['total_chunks'] = len(chunks)
        
        return chunks
    
    def _create_chunk(self, doc_type: str, section: Dict[str, Any], 
                     section_num: str, section_title: str, 
                     text: str, chunk_index: int, total_chunks: int) -> Dict[str, Any]:
        """Create a chunk with all metadata."""
        return {
            "chunk_id": f"{doc_type}_{section_num}_chunk_{chunk_index:03d}",
            "document_type": doc_type,
            "section_number": section_num,
            "section_title": section_title,
            "chunk_index": chunk_index,
            "total_chunks": total_chunks,
            "text": text,
            "token_count": self.estimate_tokens(text),
            "word_count": len(text.split()),
            
            # Copy metadata
            "offense_type": section.get('offense_type', 'unknown'),
            "bailable": section.get('bailable'),
            "cognizable": section.get('cognizable'),
            "punishment_severity": section.get('punishment_severity', 'unknown'),
            "involves_imprisonment": section.get('involves_imprisonment', False),
            "involves_fine": section.get('involves_fine', False),
            "maximum_punishment_years": section.get('maximum_punishment_years'),
            "keywords": section.get('keywords', [])
        }
    
    def _split_sentences(self, text: str) -> List[str]:
        """Split text into sentences."""
        import re
        sentences = re.split(r'(?<=[.!?])\s+', text)
        return [s.strip() for s in sentences if s.strip()]
    
    def process_all(self) -> Dict[str, Any]:
        """Process all documents."""
        print(f"\n{'='*70}")
        print("SMART CHUNKING")
        print(f"{'='*70}")
        
        doc_dirs = [d for d in self.processed_dir.iterdir() if d.is_dir()]
        print(f"Found {len(doc_dirs)} documents\n")
        
        all_chunks = []
        total_sections = 0
        
        for doc_dir in doc_dirs:
            doc_type = doc_dir.name
            sections_file = doc_dir / f"{doc_type}_sections.json"
            
            if not sections_file.exists():
                continue
            
            print(f"Processing: {doc_type}")
            
            with open(sections_file, 'r', encoding='utf-8') as f:
                sections = json.load(f)
            
            doc_chunks = []
            for section in sections:
                chunks = self.chunk_section(section, doc_type)
                doc_chunks.extend(chunks)
            
            # Save per-document
            chunks_file = self.chunks_dir / f"{doc_type}_chunks.json"
            with open(chunks_file, 'w', encoding='utf-8') as f:
                json.dump(doc_chunks, f, indent=2, ensure_ascii=False)
            
            all_chunks.extend(doc_chunks)
            total_sections += len(sections)
            
            print(f"  Sections: {len(sections)}, Chunks: {len(doc_chunks)}")
        
        # Save master file
        master_file = self.chunks_dir / "all_clean_chunks.json"
        with open(master_file, 'w', encoding='utf-8') as f:
            json.dump(all_chunks, f, indent=2, ensure_ascii=False)
        
        # Summary
        print(f"\n{'='*70}")
        print("CHUNKING SUMMARY")
        print(f"{'='*70}")
        print(f"Documents: {len(doc_dirs)}")
        print(f"Sections: {total_sections}")
        print(f"Chunks: {len(all_chunks):,}")
        print(f"Avg chunk size: {sum(c['token_count'] for c in all_chunks) / len(all_chunks):.0f} tokens")
        
        return {"total_chunks": len(all_chunks)}


if __name__ == "__main__":
    chunker = SmartChunker(chunk_size=400, overlap=50)
    chunker.process_all()
