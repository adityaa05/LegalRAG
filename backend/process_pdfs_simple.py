#!/usr/bin/env python3
"""
Simple PDF processor - processes all PDFs in data/raw/
"""

from pathlib import Path
import sys
sys.path.append('src/ingestion')

from pdf_processor import LegalDocProcessor

def main():
    # Find all PDFs
    raw_dir = Path("data/raw")
    pdf_files = list(raw_dir.glob("*.pdf"))
    
    print(f"Found {len(pdf_files)} PDF files in {raw_dir}")
    
    if not pdf_files:
        print("No PDF files found!")
        return
    
    # Process each PDF
    for i, pdf_file in enumerate(pdf_files, 1):
        print(f"\n{'='*60}")
        print(f"Processing {i}/{len(pdf_files)}: {pdf_file.name}")
        print(f"{'='*60}")
        
        try:
            # Generate doc_type from filename
            doc_type = pdf_file.stem.lower().replace(",", "").replace(" ", "_")
            
            # Process
            processor = LegalDocProcessor(str(pdf_file), doc_type)
            processor.load_document()
            processor.extract_text()
            results = processor.save_processed_data()
            
            print(f"✓ Success: {results['sections_found']} sections, {results['total_words']:,} words")
            
        except Exception as e:
            print(f"✗ Error: {e}")
    
    print(f"\n{'='*60}")
    print("Processing complete!")
    print(f"{'='*60}")

if __name__ == "__main__":
    main()
