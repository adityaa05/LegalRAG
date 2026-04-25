#!/usr/bin/env python3
"""
Improved Text Chunker

Improvements:
1. Keep section context intact
2. Better overlap strategy
3. Preserve metadata in every chunk
4. Don't split mid-sentence
"""

import json
from pathlib import Path
from typing import Dict, List, Any
from datetime import datetime


class ImprovedChunker:
    """Improved chunker that preserves context."""
    
    def __init__(self, chunk_size: int = 400, overlap: int = 50):
        self.chunk_size = chunk_size
        self.overlap = overlap
        self.processed_dir = Path("data/processed_v2")
        self.chunks_dir = Path("data/chunks_v2")
        self.chunks_dir.mkdir(parents=True, exist_ok=True)
    
    def estimate_tokens(self, text: str) -> int:
        """Estimate token count."""
        return int(len(text.split()) * 1.3)
    
    def chunk_section(self, section: Dict[str, Any], doc_type: str) -> List[Dict[str, Any]]:
        """
        Chunk a single section intelligently.
        
        Strategy:
        - If section is small enough, keep it whole
        - If large, split by sentences with overlap
        - Always include section metadata in every chunk
        """
        content = section['content']
        section_num = section['section_number']
        section_title = section['section_title']
        
        # Estimate tokens
        total_tokens = self.estimate_tokens(content)
        
        chunks = []
        
        # If small enough, keep whole
        if total_tokens <= self.chunk_size:
            chunk = {
                "chunk_id": f"{doc_type}_{section_num}_chunk_000",
                "document_type": doc_type,
                "section_number": section_num,
                "section_title": section_title,
                "chunk_index": 0,
                "total_chunks": 1,
                "text": content,
                "token_count": total_tokens,
                "word_count": len(content.split()),
                
                # Copy all metadata
                "offense_type": section.get('offense_type', 'unknown'),
                "bailable": section.get('bailable'),
                "cognizable": section.get('cognizable'),
                "punishment_severity": section.get('punishment_severity', 'unknown'),
                "involves_imprisonment": section.get('involves_imprisonment', False),
                "involves_fine": section.get('involves_fine', False),
                "maximum_punishment_years": section.get('maximum_punishment_years'),
                "keywords": section.get('keywords', [])
            }
            chunks.append(chunk)
        else:
            # Split into sentences
            sentences = self._split_sentences(content)
            
            current_chunk = []
            current_tokens = 0
            chunk_index = 0
            
            for sentence in sentences:
                sentence_tokens = self.estimate_tokens(sentence)
                
                if current_tokens + sentence_tokens > self.chunk_size and current_chunk:
                    # Save current chunk
                    chunk_text = ' '.join(current_chunk)
                    chunk = {
                        "chunk_id": f"{doc_type}_{section_num}_chunk_{chunk_index:03d}",
                        "document_type": doc_type,
                        "section_number": section_num,
                        "section_title": section_title,
                        "chunk_index": chunk_index,
                        "text": chunk_text,
                        "token_count": current_tokens,
                        "word_count": len(chunk_text.split()),
                        
                        # Metadata
                        "offense_type": section.get('offense_type', 'unknown'),
                        "bailable": section.get('bailable'),
                        "cognizable": section.get('cognizable'),
                        "punishment_severity": section.get('punishment_severity', 'unknown'),
                        "involves_imprisonment": section.get('involves_imprisonment', False),
                        "involves_fine": section.get('involves_fine', False),
                        "maximum_punishment_years": section.get('maximum_punishment_years'),
                        "keywords": section.get('keywords', [])
                    }
                    chunks.append(chunk)
                    
                    # Start new chunk with overlap
                    overlap_sentences = current_chunk[-2:] if len(current_chunk) >= 2 else current_chunk
                    current_chunk = overlap_sentences + [sentence]
                    current_tokens = sum(self.estimate_tokens(s) for s in current_chunk)
                    chunk_index += 1
                else:
                    current_chunk.append(sentence)
                    current_tokens += sentence_tokens
            
            # Save last chunk
            if current_chunk:
                chunk_text = ' '.join(current_chunk)
                chunk = {
                    "chunk_id": f"{doc_type}_{section_num}_chunk_{chunk_index:03d}",
                    "document_type": doc_type,
                    "section_number": section_num,
                    "section_title": section_title,
                    "chunk_index": chunk_index,
                    "text": chunk_text,
                    "token_count": current_tokens,
                    "word_count": len(chunk_text.split()),
                    
                    # Metadata
                    "offense_type": section.get('offense_type', 'unknown'),
                    "bailable": section.get('bailable'),
                    "cognizable": section.get('cognizable'),
                    "punishment_severity": section.get('punishment_severity', 'unknown'),
                    "involves_imprisonment": section.get('involves_imprisonment', False),
                    "involves_fine": section.get('involves_fine', False),
                    "maximum_punishment_years": section.get('maximum_punishment_years'),
                    "keywords": section.get('keywords', [])
                }
                chunks.append(chunk)
            
            # Update total_chunks
            for chunk in chunks:
                chunk['total_chunks'] = len(chunks)
        
        return chunks
    
    def _split_sentences(self, text: str) -> List[str]:
        """Split text into sentences."""
        import re
        # Simple sentence splitting
        sentences = re.split(r'(?<=[.!?])\s+', text)
        return [s.strip() for s in sentences if s.strip()]
    
    def process_all(self) -> Dict[str, Any]:
        """Process all documents."""
        print(f"\n{'='*60}")
        print("IMPROVED CHUNKING")
        print(f"{'='*60}")
        
        # Find all processed documents
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
            
            # Save per-document chunks
            chunks_file = self.chunks_dir / f"{doc_type}_chunks.json"
            with open(chunks_file, 'w', encoding='utf-8') as f:
                json.dump(doc_chunks, f, indent=2, ensure_ascii=False)
            
            all_chunks.extend(doc_chunks)
            total_sections += len(sections)
            
            print(f"  Sections: {len(sections)}, Chunks: {len(doc_chunks)}")
        
        # Save master file
        master_file = self.chunks_dir / "all_legal_chunks.json"
        with open(master_file, 'w', encoding='utf-8') as f:
            json.dump(all_chunks, f, indent=2, ensure_ascii=False)
        
        # Summary
        summary = {
            "total_documents": len(doc_dirs),
            "total_sections": total_sections,
            "total_chunks": len(all_chunks),
            "avg_chunk_size": sum(c['token_count'] for c in all_chunks) / len(all_chunks) if all_chunks else 0,
            "processed_at": datetime.now().isoformat()
        }
        
        print(f"\n{'='*60}")
        print("CHUNKING SUMMARY")
        print(f"{'='*60}")
        print(f"Documents: {summary['total_documents']}")
        print(f"Sections: {summary['total_sections']}")
        print(f"Chunks: {summary['total_chunks']:,}")
        print(f"Avg chunk size: {summary['avg_chunk_size']:.0f} tokens")
        print(f"Output: {self.chunks_dir}")
        
        return summary


if __name__ == "__main__":
    chunker = ImprovedChunker(chunk_size=400, overlap=50)
    chunker.process_all()
