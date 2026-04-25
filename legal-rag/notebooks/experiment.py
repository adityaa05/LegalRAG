import fitz
from pathlib import Path

pdf_path = "legal-rag/data/raw/the_payment_of_gratuity_act_1972_0_0.pdf"

doc_hold = None
doc_hold = fitz.open(str(Path(pdf_path)))

metadata = doc_hold.metadata
"""print(metadata)"""

if metadata.get('creationDate'):
    create_date = metadata.get('creationDate')
    print(create_date)
else:
    print("No date found")