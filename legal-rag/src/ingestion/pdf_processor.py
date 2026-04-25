#!/usr/bin/env python3
"""
Legal PDF Document Processor - Debugged Version

Fixed the NoneType comparison error and improved section detection.
"""

import fitz
import re
import json
import os
from pathlib import Path
from typing import Dict, List, Any, Optional
from datetime import datetime


class LegalDocProcessor:
    """Legal document processor for Indian law texts."""
    
    def __init__(self, pdf_path: str, doc_type: str = "unknown"):
        """Initialize processor with PDF path and document type."""
        print("Initializing Legal Document Processor")
        
        self.pdf_path = Path(pdf_path)
        self.doc_type = doc_type.lower()
        
        self.doc = None
        self.raw_text = ""
        self.sections = []
        self.metadata = {}
        
        # Create output directories
        self.output_dir = Path("data/processed")
        self.output_dir.mkdir(parents=True, exist_ok=True)
        
        print(f"Document: {self.pdf_path.name}")
        print(f"Type: {self.doc_type}")

    def load_document(self) -> None:
        """Load PDF document and extract basic metadata."""
        try:
            self.doc = fitz.open(self.pdf_path)
            print(f"PDF loaded successfully. Pages: {self.doc.page_count}")
            
            self.metadata = {
                'filename': self.pdf_path.name,
                'page_count': self.doc.page_count,
                'processed_at': datetime.now().isoformat(),
                'document_type': self.doc_type,
                'file_size_mb': round(self.pdf_path.stat().st_size / (1024 * 1024), 2)
            }
            
        except Exception as e:
            print(f"Error loading PDF: {e}")
            raise

    def extract_text(self) -> str:
        """Extract raw text from all pages."""
        if not self.doc:
            self.load_document()
            
        print(f"Extracting text from {self.doc.page_count} pages...")
        all_text = []
        
        for page_num in range(self.doc.page_count):
            page = self.doc[page_num]
            text = page.get_text()
            
            # Show sample from first few pages for debugging
            if page_num < 2:
                sample = text[:200].replace('\n', ' ')
                print(f"Page {page_num + 1} sample: {sample}...")
            
            all_text.append(text)
        
        self.raw_text = "\n".join(all_text)
        
        # Update metadata
        self.metadata['raw_text_length'] = len(self.raw_text)
        self.metadata['estimated_words'] = len(self.raw_text.split())
        
        print(f"Text extraction complete. Characters: {len(self.raw_text):,}")
        return self.raw_text   

    def clean_text(self) -> str:
        """Clean extracted text by removing artifacts and normalizing spacing."""
        print("Cleaning text...")
        text = self.raw_text
        
        # Normalize whitespace
        text = re.sub(r' +', ' ', text)  # Multiple spaces to single
        text = re.sub(r'\n\s*\n\s*\n+', '\n\n', text)  # Max double newlines
        
        # Remove page numbers (isolated numbers on their own lines)
        text = re.sub(r'\n\s*\d+\s*\n', '\n', text)
        
        # Document-specific cleaning for IPC
        if self.doc_type == 'ipc':
            # Remove the table of contents section - this is key!
            text = re.sub(r'THE INDIAN PENAL CODE.*?CHAPTER I\s+INTRODUCTION', 'CHAPTER I INTRODUCTION', text, flags=re.DOTALL | re.IGNORECASE)
            text = re.sub(r'ARRANGEMENT OF SECTIONS.*?(?=CHAPTER|PREAMBLE)', '', text, flags=re.DOTALL | re.IGNORECASE)
            
        cleaned_text = text.strip()
        
        # Update metadata
        self.metadata['cleaned_text_length'] = len(cleaned_text)
        self.metadata['compression_ratio'] = round(len(cleaned_text) / len(self.raw_text), 3)
        
        print(f"Text cleaning complete. Compression: {self.metadata['compression_ratio']:.1%}")
        return cleaned_text

    def identify_sections(self, cleaned_text: str) -> List[Dict[str, Any]]:
        """Parse document into structured sections with legal metadata."""
        print("Identifying sections...")
        
        sections = []
        
        # More specific pattern for IPC sections
        if self.doc_type == 'ipc':
            # Look for actual sections with content, not just table of contents
            # Pattern: number + period + title + actual content (not just a short line)
            section_pattern = r'(?:^|\n)\s*(\d+[A-Z]*\.)\s*([^\n]{10,100})\s*[\n]+([^0-9\n][^\n]*(?:\n(?!\s*\d+[A-Z]*\.)[^\n]*)*)'
        else:
            # Generic pattern for other documents
            section_pattern = r'(?:^|\n)\s*(?:Section\s+)?(\d+[A-Z]*\.?)\s*([^\n]+)'
        
        matches = list(re.finditer(section_pattern, cleaned_text, re.MULTILINE))
        print(f"Found {len(matches)} potential sections")
        
        # Debug: Show first few matches to understand what we're capturing
        print("Sample matches:")
        for i, match in enumerate(matches[:5]):
            section_num = match.group(1).rstrip('.')
            section_title = match.group(2).strip()
            print(f"  {i+1}. Section {section_num}: {section_title[:60]}...")
        
        for i, match in enumerate(matches):
            section_num = match.group(1).rstrip('.')
            section_title = match.group(2).strip()
            
            # For IPC, we have the content in group 3
            if self.doc_type == 'ipc' and len(match.groups()) >= 3:
                content = match.group(3).strip()
            else:
                # Extract content until next section (fallback method)
                start_pos = match.start()
                if i + 1 < len(matches):
                    end_pos = matches[i + 1].start()
                    full_content = cleaned_text[start_pos:end_pos]
                else:
                    full_content = cleaned_text[start_pos:]
                
                # Remove section header from content
                content_lines = full_content.split('\n')
                if len(content_lines) > 1:
                    content = '\n'.join(content_lines[1:]).strip()
                else:
                    content = ""
            
            # Skip sections that are too short (likely table of contents)
            if len(content) < 20:
                continue
                
            # Extract legal metadata
            legal_metadata = self._extract_legal_metadata(section_num, section_title, content)
            
            section_data = {
                "section_number": section_num,
                "title": section_title,
                "content": content,
                "word_count": len(content.split()) if content else 0,
                "character_count": len(content),
                **legal_metadata
            }
            sections.append(section_data)
        
        # Show final results
        print(f"Section parsing complete. Valid sections: {len(sections)}")
        if sections:
            print("Final examples:")
            for i, section in enumerate(sections[:3]):
                print(f"  {i+1}. Section {section['section_number']}: {section['title'][:50]}...")
            
        return sections

    def _extract_legal_metadata(self, section_num: str, title: str, content: str) -> Dict[str, Any]:
        """Extract legal-specific metadata for RAG system."""
        metadata = {
            'offense_type': 'unknown',
            'bailable': None,
            'cognizable': None,
            'punishment_severity': 'unknown',
            'involves_imprisonment': False,
            'involves_fine': False,
            'maximum_punishment_years': None,
            'keywords': []
        }
        
        if not content:
            return metadata
        
        content_lower = content.lower()
        title_lower = title.lower()
        combined_text = (title_lower + " " + content_lower)
        
        # Extract keywords for better searching
        legal_keywords = []
        keyword_patterns = [
            r'\b(murder|homicide|death|killing)\b',
            r'\b(theft|robbery|dacoity|extortion|burglary)\b',
            r'\b(assault|hurt|grievous|violence|battery)\b',
            r'\b(rape|sexual|modesty|harassment)\b',
            r'\b(fraud|cheating|forgery|deception)\b',
            r'\b(bribery|corruption|misconduct)\b',
            r'\b(defamation|libel|slander)\b',
            r'\b(conspiracy|abetment|attempt)\b'
        ]
        
        for pattern in keyword_patterns:
            matches = re.findall(pattern, combined_text)
            legal_keywords.extend(matches)
        
        metadata['keywords'] = list(set(legal_keywords))
        
        # Classify offense types
        if any(word in combined_text for word in ['murder', 'culpable homicide', 'death', 'killing']):
            metadata['offense_type'] = 'homicide'
            metadata['punishment_severity'] = 'severe'
        elif any(word in combined_text for word in ['theft', 'robbery', 'dacoity', 'extortion', 'burglary']):
            metadata['offense_type'] = 'property'
        elif any(word in combined_text for word in ['assault', 'hurt', 'grievous', 'violence', 'battery']):
            metadata['offense_type'] = 'violence'
        elif any(word in combined_text for word in ['rape', 'sexual', 'outraging', 'modesty', 'harassment']):
            metadata['offense_type'] = 'sexual'
            metadata['punishment_severity'] = 'severe'
        elif any(word in combined_text for word in ['fraud', 'cheating', 'forgery', 'deception']):
            metadata['offense_type'] = 'fraud'
        elif any(word in combined_text for word in ['bribery', 'corruption', 'misconduct']):
            metadata['offense_type'] = 'corruption'
        elif any(word in combined_text for word in ['defamation', 'libel', 'slander']):
            metadata['offense_type'] = 'defamation'
            
        # Detect punishment characteristics
        if 'imprisonment' in content_lower:
            metadata['involves_imprisonment'] = True
            
            # Extract punishment duration
            years_patterns = [
                r'(\d+)\s*years?',
                r'(\d+)\s*year',
                r'imprisonment.*?(\d+).*?years?'
            ]
            
            for pattern in years_patterns:
                years_match = re.search(pattern, content_lower)
                if years_match:
                    metadata['maximum_punishment_years'] = int(years_match.group(1))
                    break
        
        if 'fine' in content_lower:
            metadata['involves_fine'] = True
            
        # Determine bailable/cognizable (simplified logic)
        if metadata['offense_type'] in ['homicide', 'sexual'] or 'non-bailable' in content_lower:
            metadata['bailable'] = False
            metadata['cognizable'] = True
        elif 'bailable' in content_lower:
            metadata['bailable'] = True
            
        # FIXED: Use .get() with default value to avoid None comparison
        max_years = metadata.get('maximum_punishment_years') or 0
        
        # Determine punishment severity
        if 'death' in content_lower or 'life' in content_lower:
            metadata['punishment_severity'] = 'severe'
        elif max_years >= 7:
            metadata['punishment_severity'] = 'high'
        elif max_years >= 3:
            metadata['punishment_severity'] = 'medium'
        elif metadata['involves_imprisonment'] or metadata['involves_fine']:
            metadata['punishment_severity'] = 'low'
        
        return metadata

    def save_processed_data(self) -> Dict[str, Any]:
        """Save all processed data to structured files."""
        print("Processing and saving data...")
        
        # Process the document
        cleaned_text = self.clean_text()
        self.sections = self.identify_sections(cleaned_text)
        
        # Create document-specific directory
        doc_dir = self.output_dir / self.doc_type
        doc_dir.mkdir(exist_ok=True)
        
        # Save raw text
        raw_file = doc_dir / f"{self.doc_type}_raw.txt"
        with open(raw_file, 'w', encoding='utf-8') as f:
            f.write(self.raw_text)
        
        # Save cleaned text
        clean_file = doc_dir / f"{self.doc_type}_cleaned.txt"
        with open(clean_file, 'w', encoding='utf-8') as f:
            f.write(cleaned_text)
        
        # Save structured sections
        sections_file = doc_dir / f"{self.doc_type}_sections.json"
        with open(sections_file, 'w', encoding='utf-8') as f:
            json.dump(self.sections, f, indent=2, ensure_ascii=False)
        
        # Update and save metadata
        self.metadata.update({
            'sections_count': len(self.sections),
            'avg_section_length': (
                sum(s['word_count'] for s in self.sections) / len(self.sections)
                if self.sections else 0
            ),
            'offense_types_found': list(set(s.get('offense_type', 'unknown') for s in self.sections)),
            'severity_distribution': self._get_severity_distribution()
        })
        
        metadata_file = doc_dir / f"{self.doc_type}_metadata.json"
        with open(metadata_file, 'w', encoding='utf-8') as f:
            json.dump(self.metadata, f, indent=2, ensure_ascii=False)
        
        # Create summary report
        self._create_summary_report(doc_dir, cleaned_text)
        
        stats = {
            'document_type': self.doc_type,
            'pages_processed': self.metadata['page_count'],
            'sections_found': len(self.sections),
            'total_words': self.metadata.get('estimated_words', 0),
            'files_created': [
                raw_file.name,
                clean_file.name,
                sections_file.name,
                metadata_file.name
            ]
        }
        
        print(f"Processing complete! Generated {len(stats['files_created'])} files")
        print(f"Output directory: {doc_dir}")
        
        return stats
    
    def _get_severity_distribution(self) -> Dict[str, int]:
        """Get distribution of punishment severities."""
        distribution = {}
        for section in self.sections:
            severity = section.get('punishment_severity', 'unknown')
            distribution[severity] = distribution.get(severity, 0) + 1
        return distribution
    
    def _create_summary_report(self, output_dir: Path, cleaned_text: str):
        """Create human-readable summary report."""
        report_file = output_dir / f"{self.doc_type}_summary.md"
        
        report = f"""# {self.doc_type.upper()} Processing Summary

## Document Information
- **Filename**: {self.metadata['filename']}
- **Pages**: {self.metadata['page_count']}
- **File Size**: {self.metadata['file_size_mb']} MB
- **Processed**: {self.metadata['processed_at'][:19]}

## Text Statistics
- **Raw Text**: {self.metadata['raw_text_length']:,} characters
- **Cleaned Text**: {self.metadata.get('cleaned_text_length', 0):,} characters
- **Estimated Words**: {self.metadata['estimated_words']:,}
- **Sections Found**: {len(self.sections)}
- **Compression Ratio**: {self.metadata.get('compression_ratio', 0):.1%}

## Analysis Results
- **Offense Types**: {', '.join(self.metadata.get('offense_types_found', []))}
- **Severity Distribution**: {self.metadata.get('severity_distribution', {})}

## Section Examples
"""
        
        if self.sections:
            report += "| Section | Title | Words | Type | Severity |\n"
            report += "|---------|-------|-------|------|----------|\n"
            
            for section in self.sections[:15]:  # First 15 sections
                title = section['title'][:40] + "..." if len(section['title']) > 40 else section['title']
                report += f"| {section['section_number']} | {title} | {section['word_count']} | {section.get('offense_type', 'N/A')} | {section.get('punishment_severity', 'N/A')} |\n"
            
            if len(self.sections) > 15:
                report += f"\n**Total**: {len(self.sections)} sections with {sum(s['word_count'] for s in self.sections):,} words\n"
        
        report += f"""
## Next Steps
1. **Text Chunking**: Break sections into smaller chunks (500-800 tokens)
2. **Embedding Generation**: Create vector embeddings using sentence-transformers
3. **Vector Database**: Store embeddings in ChromaDB
4. **RAG Pipeline**: Build retrieval and generation system

## Files Generated
- `{self.doc_type}_raw.txt` - Original extracted text
- `{self.doc_type}_cleaned.txt` - Cleaned and preprocessed text
- `{self.doc_type}_sections.json` - Structured sections with metadata
- `{self.doc_type}_metadata.json` - Processing metadata and statistics
- `{self.doc_type}_summary.md` - This summary report

Generated by Legal RAG System
"""
        
        with open(report_file, 'w', encoding='utf-8') as f:
            f.write(report)


# Simple test script
if __name__ == "__main__":
    print("Legal Document Processor - Debugged Version")
    print("=" * 50)
    
    # Process just the IPC file for testing
    pdf_file = "legal-rag/data/raw/IPC_indiacode.pdf"
    doc_type = "ipc"
    
    if Path(pdf_file).exists():
        print(f"\nProcessing: {pdf_file}")
        try:
            processor = LegalDocProcessor(pdf_file, doc_type)
            processor.load_document()
            processor.extract_text()
            results = processor.save_processed_data()
            
            print(f"\nSUCCESS!")
            print(f"Document: {results['document_type']}")
            print(f"Pages: {results['pages_processed']}")
            print(f"Sections: {results['sections_found']}")
            print(f"Words: {results['total_words']:,}")
            print(f"\nFiles created in data/processed/{doc_type}/:")
            for file in results['files_created']:
                print(f"  - {file}")
                
        except Exception as e:
            print(f"ERROR: {e}")
            import traceback
            traceback.print_exc()
    else:
        print(f"File not found: {pdf_file}")
        print("Please ensure your IPC PDF is in data/raw/")
        
    print("\nCheck data/processed/ipc/ for the generated files!")