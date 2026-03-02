  
import os
import re
import json
import faiss
import pytesseract
from pdf2image import convert_from_path
from dotenv import load_dotenv
from supabase import create_client
from vector_store import build_index, search

# Load env
load_dotenv()

SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")
BUCKET_NAME = os.getenv("BUCKET_NAME")

supabase = create_client(SUPABASE_URL, SUPABASE_KEY)

# Set paths
pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"
POPPLER_PATH = r"C:\Users\krash\Downloads\Release-25.12.0-0\poppler-25.12.0\Library\bin"


def download_pdf(class_name, subject, chapter):
    path = f"{class_name}/{subject}/{chapter}.pdf"
    print(f"\nDownloading: {path}")

    data = supabase.storage.from_(BUCKET_NAME).download(path)

    with open("temp.pdf", "wb") as f:
        f.write(data)

    print("Download complete ✅")


def extract_text():
    print("\nExtracting text...")
    pages = convert_from_path("temp.pdf", poppler_path=POPPLER_PATH)

    full_text = ""

    for i, page in enumerate(pages):
        print(f"Processing page {i+1}")
        text = pytesseract.image_to_string(page)
        full_text += text + " "

    return full_text


def clean_text(text):
    text = re.sub(r'\s+', ' ', text)
    text = re.sub(r'[^a-zA-Z0-9.,;:()\- ]', '', text)
    return text.strip()


def chunk_text(text, chunk_size=600, overlap=100):
    words = text.split()
    chunks = []
    step = chunk_size - overlap

    for i in range(0, len(words), step):
        chunk = " ".join(words[i:i+chunk_size])
        chunks.append(chunk)

    return chunks


if __name__ == "__main__":

    print("=== Smart Tutor Ingestion System ===")

    class_name = input("Enter class (example: class_09): ").strip()
    subject = input("Enter subject (example: maths): ").strip()
    chapter = input("Enter chapter file name (example: ch_01.pdf): ").strip()

    download_pdf(class_name, subject, chapter)

    raw = extract_text()
    cleaned = clean_text(raw)
    chunks = chunk_text(cleaned)

    print("\nTotal chunks created:", len(chunks))

    index = build_index(chunks)
    print("FAISS index built ✅")

    query = input("\nEnter your question: ")

    results = search(index, chunks, query)

    print("\nTop relevant results:\n")

    for i, r in enumerate(results):
        print(f"\n--- Result {i+1} ---\n")
        print(r[:500])

    # Save index and chunks
    faiss.write_index(index, "faiss_index.bin")

    with open("chunks.json", "w", encoding="utf-8") as f:
        json.dump(chunks, f)

    print("\nIndex and chunks saved successfully ✅")