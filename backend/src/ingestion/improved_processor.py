#!/usr/bin/env python3
"""
Improved Legal PDF Processor

Fixes:
1. Better section content extraction (not just TOC)
2. Improved metadata extraction
3. Skip table of contents pages
4. Better bailable/cognizable detection
"""

import fitz
import re
import json
from pathlib import Path
from typing import Dict, List, Any
from datetime import datetime


class ImprovedLegalProcessor:
    """Improved processor for legal documents."""
    
    def __init__(self, pdf_path: str, doc_type: str):
        self.pdf_path = Path(pdf_path)
        self.doc_type = doc_type.lower()
        self.doc = None
        self.output_dir = Path("data/processed_v2")
        self.output_dir.mkdir(parents=True, exist_ok=True)
        
        print(f"\n{'='*60}")
        print(f"Processing: {self.pdf_path.name}")
        print(f"Type: {self.doc_type}")
        print(f"{'='*60}")
    
    def process(self) -> Dict[str, Any]:
        """Main processing pipeline."""
        # Load PDF
        self.doc = fitz.open(self.pdf_path)
        print(f"Pages: {self.doc.page_count}")
        
        # Extract full text
        full_text = self._extract_full_text()
        print(f"Extracted {len(full_text)} characters")
        
        # Clean text
        cleaned_text = self._clean_text(full_text)
        
        # Find sections with FULL content
        sections = self._extract_sections_with_content(cleaned_text)
        print(f"Found {len(sections)} sections with content")
        
        # Save
        return self._save_results(sections, cleaned_text)
    
    def _extract_full_text(self) -> str:
        """Extract all text from PDF."""
        text_parts = []
        for page_num in range(self.doc.page_count):
            page = self.doc[page_num]
            text = page.get_text()
            text_parts.append(text)
        return "\n".join(text_parts)
    
    def _clean_text(self, text: str) -> str:
        """Clean extracted text."""
        # Remove excessive whitespace
        text = re.sub(r'\n\s*\n\s*\n+', '\n\n', text)
        text = re.sub(r' +', ' ', text)
        return text.strip()
    
    def _extract_sections_with_content(self, text: str) -> List[Dict[str, Any]]:
        """
        Extract sections with FULL content, not just headers.
        
        Strategy:
        1. Find section headers (e.g., "304A. Causing death by negligence")
        2. Extract ALL text until next section header
        3. Skip if content is too short (TOC entry)
        """
        sections = []
        
        # Pattern for section headers
        # Matches: "304A. Title of section" or "304A.—Title of section"
        section_pattern = r'(?:^|\n)\s*(\d+[A-Z]*)\.\s*[—\-]?\s*([^\n]{10,150}?)[\.\n]'
        
        matches = list(re.finditer(section_pattern, text, re.MULTILINE))
        print(f"Found {len(matches)} potential sections")
        
        for i, match in enumerate(matches):
            section_num = match.group(1)
            section_title = match.group(2).strip()
            
            # Get content from this section to next section
            start_pos = match.end()
            if i < len(matches) - 1:
                end_pos = matches[i + 1].start()
            else:
                end_pos = len(text)
            
            content = text[start_pos:end_pos].strip()
            
            # Skip if too short (likely TOC)
            if len(content) < 50:
                continue
            
            # Skip if it's clearly a TOC (contains lots of page numbers)
            if len(re.findall(r'\b\d{1,3}\b', content)) > 10:
                continue
            
            # Extract metadata
            metadata = self._extract_metadata(section_num, section_title, content)
            
            section_data = {
                "section_number": section_num,
                "section_title": section_title,
                "content": content,
                "word_count": len(content.split()),
                "char_count": len(content),
                **metadata
            }
            
            sections.append(section_data)
        
        # Show samples
        if sections:
            print("\nSample sections:")
            for i, sec in enumerate(sections[:3], 1):
                print(f"  {i}. Section {sec['section_number']}: {sec['section_title'][:50]}...")
                print(f"     Words: {sec['word_count']}, Severity: {sec['punishment_severity']}")
        
        return sections
    
    def _extract_metadata(self, section_num: str, title: str, content: str) -> Dict[str, Any]:
        """Extract comprehensive legal metadata."""
        metadata = {
            'offense_type': 'unknown',
            'bailable': None,
            'cognizable': None,
            'punishment_severity': 'unknown',
            'involves_imprisonment': False,
            'involves_fine': False,
            'maximum_punishment_years': None,
            'minimum_punishment_years': None,
            'keywords': []
        }
        
        combined = (title + " " + content).lower()
        
        # 1. Offense Type Classification
        offense_keywords = {
            'homicide': ['murder', 'culpable homicide', 'causing death', 'killing'],
            'negligence': ['negligence', 'negligent', 'rash', 'reckless'],
            'property': ['theft', 'robbery', 'burglary', 'dacoity', 'extortion'],
            'violence': ['assault', 'hurt', 'grievous hurt', 'battery', 'attack'],
            'sexual': ['rape', 'sexual', 'modesty', 'harassment', 'molestation'],
            'fraud': ['fraud', 'cheating', 'forgery', 'deception', 'dishonest'],
            'corruption': ['bribery', 'corruption', 'misconduct', 'public servant'],
            'defamation': ['defamation', 'libel', 'slander', 'reputation'],
            'traffic': ['driving', 'vehicle', 'motor', 'traffic', 'accident']
        }
        
        for offense_type, keywords in offense_keywords.items():
            if any(kw in combined for kw in keywords):
                metadata['offense_type'] = offense_type
                metadata['keywords'].extend([kw for kw in keywords if kw in combined])
                break
        
        # 2. Bailable Status
        if 'non-bailable' in combined or 'not bailable' in combined:
            metadata['bailable'] = False
        elif 'bailable' in combined:
            metadata['bailable'] = True
        
        # 3. Cognizable Status
        if 'non-cognizable' in combined or 'not cognizable' in combined:
            metadata['cognizable'] = False
        elif 'cognizable' in combined:
            metadata['cognizable'] = True
        
        # 4. Punishment Details
        if 'imprisonment' in combined:
            metadata['involves_imprisonment'] = True
            
            # Extract years
            year_patterns = [
                r'imprisonment.*?(\d+)\s*years?',
                r'(\d+)\s*years?.*?imprisonment',
                r'extend to\s*(\d+)\s*years?',
                r'not less than\s*(\d+)\s*years?'
            ]
            
            all_years = []
            for pattern in year_patterns:
                matches = re.findall(pattern, combined)
                all_years.extend([int(m) for m in matches])
            
            if all_years:
                metadata['maximum_punishment_years'] = max(all_years)
                metadata['minimum_punishment_years'] = min(all_years)
        
        if 'fine' in combined:
            metadata['involves_fine'] = True
        
        # 5. Severity Classification
        if 'death' in combined and 'sentence' in combined:
            metadata['punishment_severity'] = 'severe'
        elif 'life' in combined and 'imprisonment' in combined:
            metadata['punishment_severity'] = 'severe'
        elif metadata['maximum_punishment_years']:
            years = metadata['maximum_punishment_years']
            if years >= 10:
                metadata['punishment_severity'] = 'high'
            elif years >= 3:
                metadata['punishment_severity'] = 'medium'
            else:
                metadata['punishment_severity'] = 'low'
        elif metadata['involves_imprisonment']:
            metadata['punishment_severity'] = 'medium'
        elif metadata['involves_fine'] and not metadata['involves_imprisonment']:
            metadata['punishment_severity'] = 'low'
        
        # 6. Special keywords for better search
        special_keywords = [
            'accident', 'negligent', 'rash', 'death', 'injury', 'hurt',
            'theft', 'stolen', 'robbery', 'assault', 'attack', 'murder',
            'rape', 'sexual', 'fraud', 'cheating', 'defamation', 'bribery'
        ]
        
        for kw in special_keywords:
            if kw in combined and kw not in metadata['keywords']:
                metadata['keywords'].append(kw)
        
        metadata['keywords'] = list(set(metadata['keywords']))[:10]  # Limit to 10
        
        return metadata
    
    def _save_results(self, sections: List[Dict[str, Any]], cleaned_text: str) -> Dict[str, Any]:
        """Save processed results."""
        doc_dir = self.output_dir / self.doc_type
        doc_dir.mkdir(exist_ok=True)
        
        # Save sections
        sections_file = doc_dir / f"{self.doc_type}_sections.json"
        with open(sections_file, 'w', encoding='utf-8') as f:
            json.dump(sections, f, indent=2, ensure_ascii=False)
        
        # Save cleaned text
        text_file = doc_dir / f"{self.doc_type}_cleaned.txt"
        with open(text_file, 'w', encoding='utf-8') as f:
            f.write(cleaned_text)
        
        # Summary
        summary = {
            "document_type": self.doc_type,
            "filename": self.pdf_path.name,
            "sections_found": len(sections),
            "total_words": sum(s['word_count'] for s in sections),
            "processed_at": datetime.now().isoformat(),
            "output_dir": str(doc_dir)
        }
        
        print(f"\n✓ Saved {len(sections)} sections to {doc_dir}")
        print(f"✓ Total words: {summary['total_words']:,}")
        
        return summary


def process_all_pdfs():
    """Process all PDFs in data/raw/."""
    raw_dir = Path("data/raw")
    pdf_files = list(raw_dir.glob("*.pdf"))
    
    print(f"\n{'='*60}")
    print(f"IMPROVED PDF PROCESSING")
    print(f"{'='*60}")
    print(f"Found {len(pdf_files)} PDF files\n")
    
    results = []
    
    for i, pdf_file in enumerate(pdf_files, 1):
        print(f"\n[{i}/{len(pdf_files)}] Processing {pdf_file.name}")
        
        try:
            doc_type = pdf_file.stem.lower().replace(",", "").replace(" ", "_")
            processor = ImprovedLegalProcessor(str(pdf_file), doc_type)
            result = processor.process()
            results.append(result)
        except Exception as e:
            print(f"✗ Error: {e}")
            results.append({"error": str(e), "file": pdf_file.name})
    
    # Summary
    print(f"\n{'='*60}")
    print("PROCESSING COMPLETE")
    print(f"{'='*60}")
    successful = [r for r in results if 'error' not in r]
    print(f"Successful: {len(successful)}/{len(pdf_files)}")
    print(f"Total sections: {sum(r.get('sections_found', 0) for r in successful):,}")
    print(f"Total words: {sum(r.get('total_words', 0) for r in successful):,}")
    
    return results


if __name__ == "__main__":
    results = process_all_pdfs()
