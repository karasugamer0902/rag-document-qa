from pypdf import PdfReader
import re

def get_pdf_page_count(file_path: str):
    reader = PdfReader(file_path)
    return len(reader.pages)

def extract_pdf_text(file_path: str):
    reader = PdfReader(file_path)
    full_text = ""
    for page in reader.pages:
        page_text = page.extract_text() or ""
        full_text += f"{page_text}\n\n"
    return full_text

def clean_text(text: str):
    cleaned_text = text.replace("", "")
    cleaned_text = re.sub(
        r"\n{3,}",
        "\n\n",
        cleaned_text
    )

    return cleaned_text

def chunk_text(text: str, chunk_size: int, overlap: int):
    if not 0 <= overlap < chunk_size:
        raise ValueError("overlap 必須大於等於 0 且小於 chunk_size")

    chunks = []
    step = chunk_size - overlap

    for start in range(0, len(text), step):
        chunk = text[start:start + chunk_size ]
        chunks.append(chunk)

    return chunks

def process_pdf(file_path: str):
    text = extract_pdf_text(file_path)
    cleaned_text = clean_text(text)
    chunks = chunk_text(cleaned_text, 500, 100)

    return chunks
