import json
import re
from pathlib import Path
from typing import Dict, List, Any, Tuple
from datetime import datetime

class TextChunker:
    
    def __init__(self, chunk_size: int = 500, overlap: int = 50):
        
        self.chunk_size = chunk_size
        self.overlap = overlap
        self.processed_dir = Path("data/processed")
        self.chunks_dir = Path("data/chunks")
        self.chunks_dir.mkdir(parents=True, exist_ok=True)
        
    def estimating_token_size(self, text: str) -> int:
        return int(len(text.split()) * 1.33)
    
    def split_text_into_sentences(self, text: str) -> int:
        
        text = re.sub(r'([.!?])\s+([A-Z])', r'\1\n\2', text)
        text = re.sub(r'\(([a-z])\)\s*', r'\n(\1) ', text)
        text = re.sub(r'([:.])(\s*Provided that)', r'\1\n\2', text)
        text = re.sub(r'([:.])(\s*Explanation)', r'\1\n\2', text)
        
        sentences = []
        for s in text.split('\n'):
            if s.strip():
                sentences.append(s.strip())
                
        return sentences

        #sentences = [s.strip() for s in text.split('\n') if s.strip()]
        
        
    def create_chunks_from_section(self, section: Dict[str, Any], doc_type: str) -> List[Dict[str, Any]]:
        content = section.get('content','')
        if not content or len(content) < 50:
            return []
        
        sentences = self.split_text_into_sentences(content)
        chunks = []
        current_chunk = []
        token_counter = 0
        
        
        for sentence in sentences:
            sentence_tokens = self.estimating_token_size(sentence)
            
            # If adding this sentence would exceed chunk size
            if token_counter + sentence_tokens > self.chunk_size and current_chunk:
                # Save current chunk
                chunk_text = ' '.join(current_chunk)
                chunks.append(self.create_chunk_metadata(
                    section, chunk_text, len(chunks), doc_type
                ))
                
                # Start new chunk with overlap
                if self.overlap > 0 and len(current_chunk) > 1:
                    # Keep last few sentences for overlap
                    overlap_sentences = []
                    overlap_tokens = 0
                    
                    for prev_sentence in reversed(current_chunk):
                        prev_tokens = self.estimating_token_size(prev_sentence)
                        if overlap_tokens + prev_tokens <= self.overlap:
                            overlap_sentences.insert(0, prev_sentence)
                            overlap_tokens += prev_tokens
                        else:
                            break
                    
                    current_chunk = overlap_sentences
                    current_tokens = overlap_tokens
                else:
                    current_chunk = []
                    current_tokens = 0
            
            current_chunk.append(sentence)
            token_counter += sentence_tokens
        
        # Add final chunk if it has content
        if current_chunk:
            chunk_text = ' '.join(current_chunk)
            chunks.append(self.create_chunk_metadata(
                section, chunk_text, len(chunks), doc_type
            ))
        
        return chunks

    def create_chunk_metadata(self, section: Dict[str, Any], chunk_text: str, chunk_index: int, doc_type: str) -> Dict[str, Any]:
        
        return {
            "chunk_id": f"{doc_type}_{section['section_number']}_chunk_{chunk_index:03d}",
            "document_type": doc_type,
            "section_number": section['section_number'],
            "section_title": section['title'],
            "chunk_index": chunk_index,
            "text": chunk_text,
            "token_count": self.estimating_token_size(chunk_text),
            "word_count": len(chunk_text.split()),
            "character_count": len(chunk_text),
            
            # Legal metadata from original section
            "offense_type": section.get('offense_type', 'unknown'),
            "punishment_severity": section.get('punishment_severity', 'unknown'),
            "involves_imprisonment": section.get('involves_imprisonment', False),
            "involves_fine": section.get('involves_fine', False),
            "keywords": section.get('keywords', []),
            
            # Chunk-specific metadata
            "created_at": datetime.now().isoformat(),
            "chunk_size_target": self.chunk_size,
            "overlap_tokens": self.overlap
        }
    
    def process_doc_type(self, doc_type: str)-> Dict[str, Any]:
        
        print(f"Processing {doc_type.upper()} ...")
        
        section_file = self.processed_dir / doc_type / f"{doc_type}_sections.json"
        
        if not section_file.exists():
            print(f"Section file not found: {section_file}")
            return {"success": False, "error": "Section file not found"}
        
        with open(section_file, 'r', encoding='utf-8') as f:
            sections = json.load(f)
            
        print(f"Loaded {len(sections)} sections")
        
        # Create chunks from all sections
        all_chunks = []
        for section in sections:
            section_chunks = self.create_chunks_from_section(section, doc_type)
            all_chunks.extend(section_chunks)
            
        # Save chunks
        chunks_file = self.chunks_dir / f"{doc_type}_chunks.json"
        with open(chunks_file, 'w', encoding='utf-8') as f:
            json.dump(all_chunks, f, indent=2, ensure_ascii=False)
        
        # Generate statistics
        total_tokens = sum(chunk['token_count'] for chunk in all_chunks)
        total_words = sum(chunk['word_count'] for chunk in all_chunks)
        avg_chunk_size = total_tokens / len(all_chunks) if all_chunks else 0
        
        stats = {
            "success": True,
            "document_type": doc_type,
            "total_sections": len(sections),
            "total_chunks": len(all_chunks),
            "total_tokens": total_tokens,
            "total_words": total_words,
            "average_chunk_size": round(avg_chunk_size, 1),
            "chunks_file": str(chunks_file.name)
        }
        
        print(f"Created {len(all_chunks)} chunks")
        print(f"   • Total tokens: {total_tokens:,}")
        print(f"   • Average chunk size: {avg_chunk_size:.1f} tokens")
        
        return stats
    
    def process_all_documents(self) -> Dict[str, Any]:
        print("Starting text chunking for all documents...")
        
        # Find all processed documents
        processed_docs = []
        for doc_dir in self.processed_dir.iterdir():
            if doc_dir.is_dir() and (doc_dir / f"{doc_dir.name}_sections.json").exists():
                processed_docs.append(doc_dir.name)
        
        print(f"Found {len(processed_docs)} processed documents: {', '.join(processed_docs)}")
        
        results = []
        total_chunks = 0
        total_tokens = 0
        
        for doc_type in processed_docs:
            result = self.process_doc_type(doc_type)
            results.append(result)
            
            if result["success"]:
                total_chunks += result["total_chunks"]
                total_tokens += result["total_tokens"]
        
        # Create master chunks file (for easy loading)
        master_chunks = []
        for doc_type in processed_docs:
            chunks_file = self.chunks_dir / f"{doc_type}_chunks.json"
            if chunks_file.exists():
                with open(chunks_file, 'r', encoding='utf-8') as f:
                    doc_chunks = json.load(f)
                    master_chunks.extend(doc_chunks)
        
        master_file = self.chunks_dir / "all_legal_chunks.json"
        with open(master_file, 'w', encoding='utf-8') as f:
            json.dump(master_chunks, f, indent=2, ensure_ascii=False)
        
        # Save chunking summary
        summary = {
            "total_documents": len(processed_docs),
            "total_chunks": total_chunks,
            "total_tokens": total_tokens,
            "chunk_size_target": self.chunk_size,
            "overlap_tokens": self.overlap,
            "processed_at": datetime.now().isoformat(),
            "results": results
        }
        
        summary_file = self.chunks_dir / "chunking_summary.json"
        with open(summary_file, 'w', encoding='utf-8') as f:
            json.dump(summary, f, indent=2, ensure_ascii=False)
        
        print(f"\n{'='*60}")
        print("CHUNKING SUMMARY")
        print(f"{'='*60}")
        print(f"Documents processed: {len(processed_docs)}")
        print(f"Total chunks created: {total_chunks:,}")
        print(f"Total tokens: {total_tokens:,}")
        if total_chunks > 0:
            print(f"Average tokens per chunk: {total_tokens/total_chunks:.1f}")
        else:
            print(f"Average tokens per chunk: 0 (no chunks created)")
        print(f"Master chunks file: {master_file.name}")
        
        return summary
    
if __name__ == "__main__":
    chunker = TextChunker(chunk_size= 500, overlap= 50)
    summary = chunker.process_all_documents()
    
    print(f'Chunking Completed')
    print(f" Check data/chunks for all chunked files")
    print(f"--- --- --- ---")
    
    print(f"Generating embeddings from chunks...")
    master_file = Path("legal-rag/data/chunks/all_legal_chunks.json")
    if master_file.exists():
        with open(master_file, 'r') as f:
            all_chunks = json.load(f)
            
    print(f"\nReady for embedding generation:")
    print(f"   • {len(all_chunks):,} chunks ready")
    print(f"   • Estimated embedding size: ~{len(all_chunks) * 384 * 4 / 1024 / 1024:.1f} MB")
    
