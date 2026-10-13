import json
import re
from pathlib import Path

from pypdf import PdfReader


BASE_DIR = Path(__file__).resolve().parent.parent

PDF_DIR = BASE_DIR / "knowledge" / "pdfs"
WEBSITE_DIR = BASE_DIR / "knowledge" / "website"
PROCESSED_DIR = BASE_DIR / "knowledge" / "processed"

OUTPUT_FILE = PROCESSED_DIR / "knowledge_chunks.json"


def clean_text(text):
    if not text:
        return ""

    text = text.replace("\x00", " ")
    text = re.sub(r"\s+", " ", text)

    return text.strip()


def chunk_text(text, chunk_size=1200, overlap=200):
    text = clean_text(text)

    if not text:
        return []

    chunks = []
    start = 0

    while start < len(text):
        end = start + chunk_size
        chunk = text[start:end].strip()

        if chunk:
            chunks.append(chunk)

        if end >= len(text):
            break

        start = end - overlap

    return chunks


def process_pdf(file_path):
    documents = []

    try:
        reader = PdfReader(str(file_path))

        for page_number, page in enumerate(reader.pages, start=1):
            text = page.extract_text() or ""
            text = clean_text(text)

            if not text:
                continue

            page_chunks = chunk_text(text)

            for chunk_number, chunk in enumerate(page_chunks, start=1):
                documents.append({
                    "source_type": "pdf",
                    "source_name": file_path.name,
                    "page": page_number,
                    "chunk": chunk_number,
                    "content": chunk
                })

    except Exception as exc:
        print(f"Could not process {file_path.name}: {exc}")

    return documents


def process_text_file(file_path):
    documents = []

    try:
        text = file_path.read_text(
            encoding="utf-8",
            errors="ignore"
        )

        chunks = chunk_text(text)

        for chunk_number, chunk in enumerate(chunks, start=1):
            documents.append({
                "source_type": "website",
                "source_name": file_path.name,
                "page": None,
                "chunk": chunk_number,
                "content": chunk
            })

    except Exception as exc:
        print(f"Could not process {file_path.name}: {exc}")

    return documents


def build_knowledge_base():
    PROCESSED_DIR.mkdir(parents=True, exist_ok=True)

    all_documents = []

    print("\nReading PDF knowledge...\n")

    for file_path in sorted(PDF_DIR.glob("*.pdf")):
        print(f"Processing PDF: {file_path.name}")

        docs = process_pdf(file_path)

        print(f"  -> {len(docs)} knowledge chunks created")

        all_documents.extend(docs)

    print("\nReading website knowledge...\n")

    for file_path in sorted(WEBSITE_DIR.glob("*.txt")):
        print(f"Processing website file: {file_path.name}")

        docs = process_text_file(file_path)

        print(f"  -> {len(docs)} knowledge chunks created")

        all_documents.extend(docs)

    OUTPUT_FILE.write_text(
        json.dumps(
            all_documents,
            indent=2,
            ensure_ascii=False
        ),
        encoding="utf-8"
    )

    print("\n--------------------------------")
    print("Doctyn knowledge base created")
    print("--------------------------------")
    print(f"Total chunks: {len(all_documents)}")
    print(f"Saved to: {OUTPUT_FILE}")


if __name__ == "__main__":
    build_knowledge_base()
