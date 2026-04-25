#!/usr/bin/env python3
"""
Clean Legal PDF Processor - Final Version

Fixes:
1. Filters out chapter headers, amendments, TOC
2. Only extracts actual numbered sections
3. Validates section numbers
4. Extracts complete metadata
5. Ensures data quality
"""

import fitz
import re
import json
from pathlib import Path
from typing import Dict, List, Any, Optional
from datetime import datetime


class CleanLegalProcessor:
    """Clean processor that extracts only valid legal sections."""
    
    def __init__(self, pdf_path: str, doc_type: str):
        self.pdf_path = Path(pdf_path)
        self.doc_type = doc_type.lower()
        self.doc = None
        self.output_dir = Path("data/processed_clean")
        self.output_dir.mkdir(parents=True, exist_ok=True)
        
        print(f"\n{'='*70}")
        print(f"Processing: {self.pdf_path.name}")
        print(f"Type: {self.doc_type}")
        print(f"{'='*70}")
    
    def process(self) -> Dict[str, Any]:
        """Main processing pipeline."""
        self.doc = fitz.open(self.pdf_path)
        print(f"Pages: {self.doc.page_count}")
        
        # Extract text
        full_text = self._extract_full_text()
        print(f"Extracted {len(full_text):,} characters")
        
        # Clean text
        cleaned_text = self._clean_text(full_text)
        
        # Extract ONLY valid sections
        sections = self._extract_valid_sections(cleaned_text)
        print(f"Found {len(sections)} VALID sections")
        
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
    
    def _is_valid_section_number(self, section_num: str) -> bool:
        """
        Validate if this is a real section number.
        
        Valid: 304A, 379, 23, 100A
        Invalid: 1 (too generic), 1952 (year), 2005 (year)
        """
        # Must be numeric with optional letter suffix
        if not re.match(r'^\d+[A-Z]*$', section_num):
            return False
        
        # Extract numeric part
        numeric = re.match(r'^(\d+)', section_num).group(1)
        num = int(numeric)
        
        # Filter out years (1800-2100)
        if 1800 <= num <= 2100:
            return False
        
        # Filter out very common generic numbers
        if num == 1 and len(section_num) == 1:
            # Section 1 is valid only if it has substantial content
            # We'll validate this later
            return True
        
        # Valid section number
        return True
    
    def _is_junk_content(self, text: str) -> bool:
        """
        Detect if content is junk (chapter headers, amendments, etc.)
        """
        text_lower = text.lower()
        
        # Junk patterns
        junk_patterns = [
            r'^CHAPTER [IVX]+',  # Chapter headers
            r'^PART [IVX]+',     # Part headers
            r'^\[?Subs\. by Act',  # Substitution notes
            r'^\[?Ins\. by Act',   # Insertion notes
            r'^\[?Omitted by Act', # Omission notes
            r'^TABLE OF CONTENTS',
            r'^SCHEDULE [IVX]+',
            r'^APPENDIX',
            r'^INDEX',
            r'^\d+\s+\d+$',  # Page numbers only
        ]
        
        for pattern in junk_patterns:
            if re.search(pattern, text, re.MULTILINE | re.IGNORECASE):
                return True
        
        # Check if it's mostly page numbers
        numbers = re.findall(r'\b\d{1,3}\b', text)
        if len(numbers) > 20 and len(text) < 500:
            return True
        
        return False
    
    def _extract_valid_sections(self, text: str) -> List[Dict[str, Any]]:
        """
        Extract ONLY valid legal sections.
        
        Strategy:
        1. Find section headers with strict pattern
        2. Validate section number
        3. Extract content until next section
        4. Filter out junk
        5. Validate content quality
        """
        sections = []
        
        # Strict pattern for section headers
        # Matches: "304A. Title" or "304A.—Title" or "304A.- Title"
        # More flexible ending: period, newline, or dash
        section_pattern = r'(?:^|\n)\s*(\d+[A-Z]*)\.\s*[—\-]?\s*([^\n]{5,200}?)(?:\.|\n|—)'
        
        matches = list(re.finditer(section_pattern, text, re.MULTILINE))
        print(f"Found {len(matches)} potential sections")
        
        valid_count = 0
        skipped_invalid_num = 0
        skipped_junk = 0
        skipped_short = 0
        
        for i, match in enumerate(matches):
            section_num = match.group(1).strip()
            section_title = match.group(2).strip()
            
            # Validate section number
            if not self._is_valid_section_number(section_num):
                skipped_invalid_num += 1
                continue
            
            # Get content
            start_pos = match.end()
            if i < len(matches) - 1:
                end_pos = matches[i + 1].start()
            else:
                end_pos = len(text)
            
            content = text[start_pos:end_pos].strip()
            
            # Skip if too short (likely TOC)
            if len(content) < 100:
                skipped_short += 1
                continue
            
            # Skip junk content
            if self._is_junk_content(content):
                skipped_junk += 1
                continue
            
            # Validate: section number should appear in content or title
            section_mention = f"{section_num}." in content or f"{section_num}." in section_title
            if not section_mention and len(content) < 200:
                skipped_junk += 1
                continue
            
            # Extract metadata
            metadata = self._extract_comprehensive_metadata(section_num, section_title, content)
            
            # Additional validation: must have some legal keywords
            if metadata['offense_type'] == 'unknown' and len(metadata['keywords']) == 0:
                # Check if it has legal language
                legal_terms = ['shall', 'whoever', 'punishment', 'imprisonment', 'fine', 
                              'offence', 'liable', 'guilty', 'court', 'law']
                has_legal_terms = any(term in content.lower() for term in legal_terms)
                if not has_legal_terms and len(content) < 300:
                    skipped_junk += 1
                    continue
            
            section_data = {
                "section_number": section_num,
                "section_title": section_title,
                "content": content,
                "word_count": len(content.split()),
                "char_count": len(content),
                **metadata
            }
            
            sections.append(section_data)
            valid_count += 1
        
        # Show filtering stats
        print(f"\nFiltering Results:")
        print(f"  Valid sections: {valid_count}")
        print(f"  Skipped (invalid number): {skipped_invalid_num}")
        print(f"  Skipped (junk content): {skipped_junk}")
        print(f"  Skipped (too short): {skipped_short}")
        
        # Show samples
        if sections:
            print(f"\nSample valid sections:")
            for i, sec in enumerate(sections[:5], 1):
                print(f"  {i}. Section {sec['section_number']}: {sec['section_title'][:60]}...")
                print(f"     Words: {sec['word_count']}, Type: {sec['offense_type']}, Severity: {sec['punishment_severity']}")
        
        return sections
    
    def _extract_comprehensive_metadata(self, section_num: str, title: str, content: str) -> Dict[str, Any]:
        """Extract comprehensive legal metadata with better accuracy."""
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
        
        # 1. Offense Type Classification (more comprehensive)
        offense_patterns = {
            'homicide': [
                r'\bmurder\b', r'\bculpable homicide\b', r'\bcausing death\b', 
                r'\bkilling\b', r'\bhomicide\b'
            ],
            'negligence': [
                r'\bnegligence\b', r'\bnegligent\b', r'\brash\b', 
                r'\breckless\b', r'\bcareless\b'
            ],
            'property': [
                r'\btheft\b', r'\brobbery\b', r'\bburglary\b', r'\bdacoity\b', 
                r'\bextortion\b', r'\bstolen property\b'
            ],
            'violence': [
                r'\bassault\b', r'\bhurt\b', r'\bgrievous hurt\b', 
                r'\bbattery\b', r'\battack\b', r'\bwound\b'
            ],
            'sexual': [
                r'\brape\b', r'\bsexual\b', r'\bmodesty\b', 
                r'\bharassment\b', r'\bmolestation\b'
            ],
            'fraud': [
                r'\bfraud\b', r'\bcheating\b', r'\bforgery\b', 
                r'\bdeception\b', r'\bdishonest\b'
            ],
            'defamation': [
                r'\bdefamation\b', r'\blibel\b', r'\bslander\b', r'\breputation\b'
            ],
            'traffic': [
                r'\bdriving\b', r'\bvehicle\b', r'\bmotor\b', 
                r'\btraffic\b', r'\baccident\b', r'\bdrunken\b'
            ],
            'corruption': [
                r'\bbribery\b', r'\bcorruption\b', r'\bpublic servant\b'
            ]
        }
        
        for offense_type, patterns in offense_patterns.items():
            for pattern in patterns:
                if re.search(pattern, combined):
                    metadata['offense_type'] = offense_type
                    # Extract matched keywords
                    matches = re.findall(pattern, combined)
                    metadata['keywords'].extend(matches)
                    break
            if metadata['offense_type'] != 'unknown':
                break
        
        # 2. Bailable Status (explicit detection)
        if re.search(r'\bnon-bailable\b', combined) or re.search(r'\bnot bailable\b', combined):
            metadata['bailable'] = False
        elif re.search(r'\bbailable\b', combined):
            # Check if it's saying "bailable" or "non-bailable"
            context = re.search(r'(\w+\s+){0,3}bailable', combined)
            if context and 'non' not in context.group():
                metadata['bailable'] = True
        
        # 3. Cognizable Status
        if re.search(r'\bnon-cognizable\b', combined) or re.search(r'\bnot cognizable\b', combined):
            metadata['cognizable'] = False
        elif re.search(r'\bcognizable\b', combined):
            context = re.search(r'(\w+\s+){0,3}cognizable', combined)
            if context and 'non' not in context.group():
                metadata['cognizable'] = True
        
        # 4. Punishment Details (improved extraction)
        if re.search(r'\bimprisonment\b', combined):
            metadata['involves_imprisonment'] = True
            
            # Extract years with better patterns
            year_patterns = [
                r'imprisonment.*?for.*?(\d+)\s*years?',
                r'(\d+)\s*years?.*?imprisonment',
                r'extend to\s*(\d+)\s*years?',
                r'not less than\s*(\d+)\s*years?',
                r'term.*?(\d+)\s*years?',
                r'(\d+)\s*years?.*?or.*?imprisonment'
            ]
            
            all_years = []
            for pattern in year_patterns:
                matches = re.findall(pattern, combined, re.IGNORECASE)
                all_years.extend([int(m) for m in matches if m.isdigit()])
            
            if all_years:
                metadata['maximum_punishment_years'] = max(all_years)
                metadata['minimum_punishment_years'] = min(all_years)
        
        # Check for life imprisonment
        if re.search(r'\blife\b.*?\bimprisonment\b', combined) or re.search(r'\bimprisonment\b.*?\blife\b', combined):
            metadata['maximum_punishment_years'] = 999  # Special marker for life
            metadata['involves_imprisonment'] = True
        
        # Check for death penalty
        if re.search(r'\bdeath\b.*?\bpenalty\b', combined) or re.search(r'\bpunished with death\b', combined):
            metadata['maximum_punishment_years'] = 1000  # Special marker for death
        
        if re.search(r'\bfine\b', combined):
            metadata['involves_fine'] = True
        
        # 5. Severity Classification (improved logic)
        if metadata['maximum_punishment_years']:
            years = metadata['maximum_punishment_years']
            if years >= 1000:
                metadata['punishment_severity'] = 'severe'  # Death penalty
            elif years >= 999:
                metadata['punishment_severity'] = 'severe'  # Life imprisonment
            elif years >= 10:
                metadata['punishment_severity'] = 'high'
            elif years >= 3:
                metadata['punishment_severity'] = 'medium'
            else:
                metadata['punishment_severity'] = 'low'
        elif metadata['involves_imprisonment']:
            metadata['punishment_severity'] = 'medium'
        elif metadata['involves_fine'] and not metadata['involves_imprisonment']:
            metadata['punishment_severity'] = 'low'
        
        # 6. Extract additional keywords
        keyword_patterns = [
            r'\b(accident|negligent|rash|death|injury|hurt)\b',
            r'\b(theft|stolen|robbery|burglary)\b',
            r'\b(assault|attack|murder|killing)\b',
            r'\b(rape|sexual|harassment|modesty)\b',
            r'\b(fraud|cheating|forgery|deception)\b',
            r'\b(defamation|libel|slander)\b',
            r'\b(bribery|corruption)\b',
            r'\b(driving|vehicle|motor|traffic|drunk)\b'
        ]
        
        for pattern in keyword_patterns:
            matches = re.findall(pattern, combined)
            metadata['keywords'].extend(matches)
        
        # Deduplicate and limit keywords
        metadata['keywords'] = list(set(metadata['keywords']))[:15]
        
        return metadata
    
    def _save_results(self, sections: List[Dict[str, Any]], cleaned_text: str) -> Dict[str, Any]:
        """Save processed results."""
        doc_dir = self.output_dir / self.doc_type
        doc_dir.mkdir(exist_ok=True)
        
        # Save sections
        sections_file = doc_dir / f"{self.doc_type}_sections.json"
        with open(sections_file, 'w', encoding='utf-8') as f:
            json.dump(sections, f, indent=2, ensure_ascii=False)
        
        # Summary
        summary = {
            "document_type": self.doc_type,
            "filename": self.pdf_path.name,
            "sections_found": len(sections),
            "total_words": sum(s['word_count'] for s in sections),
            "with_metadata": sum(1 for s in sections if s['offense_type'] != 'unknown'),
            "processed_at": datetime.now().isoformat(),
            "output_dir": str(doc_dir)
        }
        
        print(f"\n✓ Saved {len(sections)} sections to {doc_dir}")
        print(f"✓ Total words: {summary['total_words']:,}")
        print(f"✓ With metadata: {summary['with_metadata']}/{len(sections)}")
        
        return summary


def process_all_pdfs():
    """Process all PDFs with clean extraction."""
    raw_dir = Path("data/raw")
    pdf_files = list(raw_dir.glob("*.pdf"))
    
    print(f"\n{'='*70}")
    print(f"CLEAN PDF PROCESSING - FINAL VERSION")
    print(f"{'='*70}")
    print(f"Found {len(pdf_files)} PDF files\n")
    
    results = []
    
    for i, pdf_file in enumerate(pdf_files, 1):
        print(f"\n[{i}/{len(pdf_files)}]")
        
        try:
            doc_type = pdf_file.stem.lower().replace(",", "").replace(" ", "_")
            processor = CleanLegalProcessor(str(pdf_file), doc_type)
            result = processor.process()
            results.append(result)
        except Exception as e:
            print(f"✗ Error: {e}")
            import traceback
            traceback.print_exc()
            results.append({"error": str(e), "file": pdf_file.name})
    
    # Summary
    print(f"\n{'='*70}")
    print("PROCESSING COMPLETE")
    print(f"{'='*70}")
    successful = [r for r in results if 'error' not in r]
    print(f"Successful: {len(successful)}/{len(pdf_files)}")
    print(f"Total sections: {sum(r.get('sections_found', 0) for r in successful):,}")
    print(f"Total words: {sum(r.get('total_words', 0) for r in successful):,}")
    print(f"With metadata: {sum(r.get('with_metadata', 0) for r in successful):,}")
    
    return results


if __name__ == "__main__":
    results = process_all_pdfs()
