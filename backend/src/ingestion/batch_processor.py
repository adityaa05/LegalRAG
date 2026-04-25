#!/usr/bin/env python3
"""
Batch Legal Document Processor

Processes multiple legal documents and provides quality evaluation.
"""

import fitz
import re
import json
import os
from pathlib import Path
from typing import Dict, List, Any, Optional
from datetime import datetime


class BatchLegalProcessor:
    """Batch processor for multiple legal documents."""
    
    def __init__(self):
        """Initialize the batch processor."""
        self.output_dir = Path("legal-rag/data/processed")
        self.output_dir.mkdir(parents=True, exist_ok=True)
        self.results = []
        
    def get_document_configs(self) -> List[Dict[str, str]]:
        """Define all documents to process with their configurations."""
        # Auto-discover PDF files in data/raw
        raw_dir = Path("legal-rag/data/raw")
        pdf_files = list(raw_dir.glob("*.pdf"))
        
        configs = []
        for pdf_file in pdf_files:
            # Generate doc_type from filename
            doc_type = pdf_file.stem.lower().replace(",", "").replace(" ", "_")
            
            configs.append({
                "file": str(pdf_file),
                "type": doc_type,
                "name": pdf_file.stem.replace("_", " ").title(),
                "expected_sections": "50-500",  # Flexible range
                "section_pattern": r'(?:^|\n)\s*(\d+[A-Z]*\.)\s*([^\n]{5,100})\s*[\n]+((?:[^\n]+\n?)*?)(?=\n\s*\d+[A-Z]*\.|$)'
            })
        
        return configs
    
    def process_single_document(self, config: Dict[str, str]) -> Dict[str, Any]:
        """Process a single document using its specific configuration."""
        file_path = Path(config["file"])
        
        if not file_path.exists():
            return {
                "success": False,
                "error": f"File not found: {file_path}",
                "config": config
            }
        
        print(f"\n{'='*60}")
        print(f"Processing: {config['name']} ({config['type']})")
        print(f"{'='*60}")
        
        try:
            # Use the enhanced processor
            processor = EnhancedLegalProcessor(str(file_path), config["type"], config.get("section_pattern"))
            processor.load_document()
            processor.extract_text()
            results = processor.save_processed_data()
            
            # Quality evaluation
            quality_score = self.evaluate_quality(results, config)
            
            result_data = {
                "success": True,
                "config": config,
                "results": results,
                "quality_score": quality_score,
                "evaluation": self.get_evaluation_summary(results, config, quality_score)
            }
            
            print(f"SUCCESS: {results['sections_found']} sections, Quality: {quality_score:.1f}/10")
            return result_data
            
        except Exception as e:
            print(f"ERROR: {e}")
            return {
                "success": False,
                "error": str(e),
                "config": config
            }
    
    def evaluate_quality(self, results: Dict[str, Any], config: Dict[str, str]) -> float:
        """Evaluate the quality of document processing."""
        score = 10.0
        
        # Check section count reasonableness
        sections_found = results["sections_found"]
        expected_range = config["expected_sections"].split("-")
        expected_min = int(expected_range[0])
        expected_max = int(expected_range[1])
        
        if sections_found < expected_min * 0.7:  # Too few sections
            score -= 3.0
        elif sections_found > expected_max * 1.5:  # Too many sections
            score -= 2.0
        elif expected_min <= sections_found <= expected_max:  # Perfect range
            score += 0.5
        
        # Check word count (should have substantial content)
        words = results["total_words"]
        if words < 10000:  # Too little content
            score -= 2.0
        elif words > 500000:  # Suspiciously large
            score -= 1.0
        
        # Check if processing completed without errors
        if results["sections_found"] > 0:
            score += 1.0
        
        return max(0.0, min(10.0, score))
    
    def get_evaluation_summary(self, results: Dict[str, Any], config: Dict[str, str], quality_score: float) -> str:
        """Generate evaluation summary."""
        sections = results["sections_found"]
        expected_range = config["expected_sections"]
        
        if quality_score >= 8.0:
            return f"EXCELLENT: {sections} sections detected (expected {expected_range})"
        elif quality_score >= 6.0:
            return f"GOOD: {sections} sections detected, minor issues"
        elif quality_score >= 4.0:
            return f"FAIR: {sections} sections detected, needs review"
        else:
            return f"POOR: {sections} sections detected, significant issues"
    
    def process_all_documents(self) -> Dict[str, Any]:
        """Process all configured documents."""
        print("Batch Legal Document Processor")
        print("Processing all legal documents...")
        
        configs = self.get_document_configs()
        results = []
        
        for config in configs:
            result = self.process_single_document(config)
            results.append(result)
            self.results.append(result)
        
        # Generate summary report
        summary = self.generate_summary_report(results)
        
        # Save batch results
        batch_file = self.output_dir / "batch_processing_results.json"
        with open(batch_file, 'w', encoding='utf-8') as f:
            json.dump(results, f, indent=2, ensure_ascii=False)
        
        return summary
    
    def generate_summary_report(self, results: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Generate a summary report of all processing."""
        successful = [r for r in results if r["success"]]
        failed = [r for r in results if not r["success"]]
        
        total_sections = sum(r["results"]["sections_found"] for r in successful)
        total_words = sum(r["results"]["total_words"] for r in successful)
        avg_quality = sum(r["quality_score"] for r in successful) / len(successful) if successful else 0
        
        summary = {
            "total_documents": len(results),
            "successful": len(successful),
            "failed": len(failed),
            "total_sections": total_sections,
            "total_words": total_words,
            "average_quality_score": round(avg_quality, 1),
            "details": results
        }
        
        print(f"\n{'='*60}")
        print(" BATCH PROCESSING SUMMARY")
        print(f"{'='*60}")
        print(f"Documents processed: {summary['total_documents']}")
        print(f"Successful: {summary['successful']}")
        print(f"Failed: {summary['failed']}")
        print(f"Total sections extracted: {summary['total_sections']:,}")
        print(f"Total words: {summary['total_words']:,}")
        print(f"Average quality score: {summary['average_quality_score']}/10")
        
        # Individual results
        print(f"\n Individual Results:")
        for result in results:
            if result["success"]:
                config = result["config"]
                res = result["results"]
                qual = result["quality_score"]
                print(f"{config['name']}: {res['sections_found']} sections, {qual:.1f}/10 quality")
            else:
                config = result["config"]
                print(f"{config['name']}: {result['error']}")
        
        return summary


class EnhancedLegalProcessor:
    """Enhanced processor with configurable section patterns."""
    
    def __init__(self, pdf_path: str, doc_type: str, section_pattern: Optional[str] = None):
        """Initialize with custom section pattern."""
        self.pdf_path = Path(pdf_path)
        self.doc_type = doc_type.lower()
        self.custom_pattern = section_pattern
        
        self.doc = None
        self.raw_text = ""
        self.sections = []
        self.metadata = {}
        
        self.output_dir = Path("legal-rag/data/processed")
        self.output_dir.mkdir(parents=True, exist_ok=True)
        
        print(f"Document: {self.pdf_path.name}")
        print(f"Type: {self.doc_type}")

    def load_document(self) -> None:
        """Load PDF document."""
        try:
            self.doc = fitz.open(self.pdf_path)
            print(f"Pages: {self.doc.page_count}")
            
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
        """Extract text from all pages."""
        if not self.doc:
            self.load_document()
            
        print(f"Extracting text...")
        all_text = []
        
        for page_num in range(self.doc.page_count):
            page = self.doc[page_num]
            text = page.get_text()
            all_text.append(text)
        
        self.raw_text = "\n".join(all_text)
        self.metadata['raw_text_length'] = len(self.raw_text)
        self.metadata['estimated_words'] = len(self.raw_text.split())
        
        print(f"Characters: {len(self.raw_text):,}")
        return self.raw_text

    def clean_text(self) -> str:
        """Clean extracted text."""
        print("Cleaning text...")
        text = self.raw_text
        
        # Basic cleaning
        text = re.sub(r' +', ' ', text)
        text = re.sub(r'\n\s*\n\s*\n+', '\n\n', text)
        text = re.sub(r'\n\s*\d+\s*\n', '\n', text)
        
        # Document-specific cleaning
        cleaning_patterns = {
            'ipc': [
                (r'THE INDIAN PENAL CODE.*?CHAPTER I\s+INTRODUCTION', 'CHAPTER I INTRODUCTION'),
                (r'ARRANGEMENT OF SECTIONS.*?(?=CHAPTER|PREAMBLE)', '')
            ],
            'crpc': [
                (r'THE CODE OF CRIMINAL PROCEDURE.*?(?=CHAPTER|Section)', '')
            ],
            'constitution': [
                (r'THE CONSTITUTION OF INDIA.*?(?=PART|Article)', '')
            ]
        }
        
        if self.doc_type in cleaning_patterns:
            for pattern, replacement in cleaning_patterns[self.doc_type]:
                text = re.sub(pattern, replacement, text, flags=re.DOTALL | re.IGNORECASE)
        
        cleaned_text = text.strip()
        self.metadata['cleaned_text_length'] = len(cleaned_text)
        self.metadata['compression_ratio'] = round(len(cleaned_text) / len(self.raw_text), 3)
        
        print(f"Compression: {self.metadata['compression_ratio']:.1%}")
        return cleaned_text

    def identify_sections(self, cleaned_text: str) -> List[Dict[str, Any]]:
        """Identify sections using custom or default patterns."""
        print("Identifying sections...")
        
        # Use custom pattern if provided, otherwise use default
        if self.custom_pattern:
            section_pattern = self.custom_pattern
        else:
            # Default pattern
            section_pattern = r'(?:^|\n)\s*(\d+[A-Z]*\.)\s*([^\n]{10,100})\s*[\n]+([^0-9\n][^\n]*(?:\n(?!\s*\d+[A-Z]*\.)[^\n]*)*)'
        
        matches = list(re.finditer(section_pattern, cleaned_text, re.MULTILINE))
        print(f"Found {len(matches)} potential sections")
        
        sections = []
        for i, match in enumerate(matches):
            section_num = match.group(1).rstrip('.')
            section_title = match.group(2).strip()
            
            # Extract content
            if len(match.groups()) >= 3 and match.group(3):
                content = match.group(3).strip()
            else:
                start_pos = match.start()
                if i + 1 < len(matches):
                    end_pos = matches[i + 1].start()
                    full_content = cleaned_text[start_pos:end_pos]
                else:
                    full_content = cleaned_text[start_pos:]
                
                content_lines = full_content.split('\n')
                content = '\n'.join(content_lines[1:]).strip() if len(content_lines) > 1 else ""
            
            # Skip very short sections
            if len(content) < 20:
                continue
            
            section_data = {
                "section_number": section_num,
                "title": section_title,
                "content": content,
                "word_count": len(content.split()) if content else 0,
                "character_count": len(content)
            }
            sections.append(section_data)
        
        print(f"Valid sections: {len(sections)}")
        return sections

    def save_processed_data(self) -> Dict[str, Any]:
        """Save all processed data."""
        print("Processing and saving...")
        
        cleaned_text = self.clean_text()
        self.sections = self.identify_sections(cleaned_text)
        
        # Create document directory
        doc_dir = self.output_dir / self.doc_type
        doc_dir.mkdir(exist_ok=True)
        
        # Save files
        files_created = []
        
        # Raw text
        raw_file = doc_dir / f"{self.doc_type}_raw.txt"
        with open(raw_file, 'w', encoding='utf-8') as f:
            f.write(self.raw_text)
        files_created.append(raw_file.name)
        
        # Cleaned text
        clean_file = doc_dir / f"{self.doc_type}_cleaned.txt"
        with open(clean_file, 'w', encoding='utf-8') as f:
            f.write(cleaned_text)
        files_created.append(clean_file.name)
        
        # Sections
        sections_file = doc_dir / f"{self.doc_type}_sections.json"
        with open(sections_file, 'w', encoding='utf-8') as f:
            json.dump(self.sections, f, indent=2, ensure_ascii=False)
        files_created.append(sections_file.name)
        
        # Metadata
        self.metadata['sections_count'] = len(self.sections)
        metadata_file = doc_dir / f"{self.doc_type}_metadata.json"
        with open(metadata_file, 'w', encoding='utf-8') as f:
            json.dump(self.metadata, f, indent=2, ensure_ascii=False)
        files_created.append(metadata_file.name)
        
        return {
            'document_type': self.doc_type,
            'pages_processed': self.metadata['page_count'],
            'sections_found': len(self.sections),
            'total_words': self.metadata.get('estimated_words', 0),
            'files_created': files_created
        }


if __name__ == "__main__":
    # Run batch processing
    processor = BatchLegalProcessor()
    summary = processor.process_all_documents()
    
    print(f"\n Processing complete!")
    print(f"Check data/processed/ for all generated files.")
    print(f"Batch results saved to: data/processed/batch_processing_results.json")