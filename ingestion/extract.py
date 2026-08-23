"""
extract.py
Reads PDF policy documents from data/, extracts text page by page,
and splits it into overlapping chunks ready for embedding.
"""

import os
import re
from pathlib import Path
from pypdf import PdfReader

DATA_DIR = Path(__file__).parent.parent / "data"
CHUNK_SIZE = 800       # target characters per chunk
CHUNK_OVERLAP = 150    # overlap between consecutive chunks


def clean_text(text: str) -> str:
    """Collapse excess whitespace and strip odd PDF artifacts."""
    text = re.sub(r"\s+", " ", text)
    text = text.strip()
    return text


def extract_pdf_pages(pdf_path: Path):
    """Yield (page_number, page_text) for every non-empty page in a PDF."""
    reader = PdfReader(str(pdf_path))
    for i, page in enumerate(reader.pages, start=1):
        raw = page.extract_text() or ""
        cleaned = clean_text(raw)
        if cleaned:
            yield i, cleaned


def chunk_text(text: str, chunk_size: int = CHUNK_SIZE, overlap: int = CHUNK_OVERLAP):
    """Split text into overlapping chunks, breaking on sentence boundaries where possible."""
    if len(text) <= chunk_size:
        return [text]

    chunks = []
    start = 0
    text_len = len(text)

    while start < text_len:
        end = min(start + chunk_size, text_len)

        # try to break at a sentence boundary near the target end
        if end < text_len:
            boundary = text.rfind(". ", start, end)
            if boundary != -1 and boundary > start + (chunk_size // 2):
                end = boundary + 1

        chunk = text[start:end].strip()
        if chunk:
            chunks.append(chunk)

        start = end - overlap if end - overlap > start else end

    return chunks


def process_document(pdf_path: Path):
    """
    Process a single PDF into a list of chunk records:
    { "text": ..., "source": filename, "page": page_number, "chunk_id": ... }
    """
    records = []
    doc_name = pdf_path.stem

    for page_num, page_text in extract_pdf_pages(pdf_path):
        chunks = chunk_text(page_text)
        for idx, chunk in enumerate(chunks):
            records.append({
                "text": chunk,
                "source": doc_name,
                "page": page_num,
                "chunk_id": f"{doc_name}_p{page_num}_c{idx}",
            })

    return records


def process_all_documents():
    """Process every PDF in data/ and return a combined list of chunk records."""
    all_records = []
    pdf_files = sorted(DATA_DIR.glob("*.pdf"))

    if not pdf_files:
        print(f"No PDFs found in {DATA_DIR}")
        return all_records

    for pdf_path in pdf_files:
        print(f"Processing {pdf_path.name} ...")
        records = process_document(pdf_path)
        print(f"  -> {len(records)} chunks")
        all_records.extend(records)

    print(f"\nTotal chunks across all documents: {len(all_records)}")
    return all_records


if __name__ == "__main__":
    records = process_all_documents()
    if records:
        print("\nSample chunk:")
        print(records[0])
