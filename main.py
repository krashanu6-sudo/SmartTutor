import os
import re
import faiss
import pytesseract
import numpy as np
from pdf2image import convert_from_path
from dotenv import load_dotenv
from supabase import create_client
from sentence_transformers import SentenceTransformer

# ==============================
# LOAD ENVIRONMENT VARIABLES
# ==============================

load_dotenv()

SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")
BUCKET_NAME = os.getenv("BUCKET_NAME")

supabase = create_client(SUPABASE_URL, SUPABASE_KEY)

# ==============================
# PATH CONFIGURATION
# ==============================

pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"
POPPLER_PATH = r"C:\Users\krash\Downloads\Release-25.12.0-0\poppler-25.12.0\Library\bin"

model = SentenceTransformer("all-MiniLM-L6-v2")

# ==============================
# STEP 1: DOWNLOAD PDF
# ==============================


def download_pdf(class_name, subject, chapter):
    path = f"{class_name}/{subject}/{chapter}.pdf"
    print(f"\nDownloading: {path}")

    data = supabase.storage.from_(BUCKET_NAME).download(path)

    with open("temp.pdf", "wb") as f:
        f.write(data)

    print("Download complete ✅")


# ==============================
# STEP 2: OCR EXTRACTION
# ==============================


def extract_text():
    print("\nExtracting text...")
    pages = convert_from_path("temp.pdf", poppler_path=POPPLER_PATH)

    full_text = ""

    for i, page in enumerate(pages):
        print(f"Processing page {i+1}")
        text = pytesseract.image_to_string(page, lang="hin+eng")
        full_text += text + " "

    return full_text


# ==============================
# STEP 3: CLEAN TEXT
# ==============================


def clean_text(text):
    text = re.sub(r"\s+", " ", text)
    return text.strip()


# ==============================
# STEP 4: CHUNK TEXT
# ==============================




def chunk_text(text, max_chars=1000, overlap=200):
    """
    Advanced semantic chunking
    - Paragraph aware
    - Sentence aware
    - Hindi + English support
    """

    # Split into paragraphs first
    paragraphs = text.split("\n")

    chunks = []
    current_chunk = ""

    for para in paragraphs:

        # Split paragraph into sentences
        sentences = re.split(r'(?<=[.!?।])\s+', para)

        for sentence in sentences:

            if len(current_chunk) + len(sentence) <= max_chars:
                current_chunk += sentence + " "
            else:
                chunks.append(current_chunk.strip())
                current_chunk = sentence + " "

    if current_chunk:
        chunks.append(current_chunk.strip())

    # Add overlap between chunks
    final_chunks = []

    for i in range(len(chunks)):
        if i == 0:
            final_chunks.append(chunks[i])
        else:
            overlap_text = chunks[i-1][-overlap:]
            final_chunks.append(overlap_text + " " + chunks[i])

    return final_chunks


# ==============================
# STEP 5: STORE CHUNKS IN SUPABASE
# ==============================


def store_chunks_to_supabase(class_name, subject, chapter, chunks):
    print("\nUploading chunks + embeddings to Supabase...")

    # Delete old entries
    supabase.table("book_chunks") \
        .delete() \
        .eq("class", class_name) \
        .eq("subject", subject) \
        .eq("chapter", chapter) \
        .execute()

    data_to_insert = []

    # Generate embeddings once
    embeddings = model.encode(chunks)

    for i, chunk in enumerate(chunks):
        data_to_insert.append({
            "class": class_name,
            "subject": subject,
            "chapter": chapter,
            "chunk_index": i,
            "content": chunk,
            "embedding": embeddings[i].tolist()  # convert numpy to list
        })

    supabase.table("book_chunks").insert(data_to_insert).execute()

    print("Chunks + embeddings stored in Supabase ✅")


# ==============================
# STEP 6: BUILD FAISS INDEX
# ==============================


def build_faiss_index(chunks):
    print("\nGenerating embeddings...")
    embeddings = model.encode(chunks)

    dimension = embeddings.shape[1]
    index = faiss.IndexFlatL2(dimension)
    index.add(np.array(embeddings))

    print("FAISS index built ✅")
    return index


# ==============================
# STEP 7: SEARCH
# ==============================


def search(index, chunks, query, top_k=5):
    query_embedding = model.encode([query])
    distances, indices = index.search(query_embedding, top_k)

    results = []
    for idx in indices[0]:
        results.append(chunks[idx])

    return results


# ==============================
# MAIN EXECUTION
# ==============================

if __name__ == "__main__":

    print("=== Smart Tutor Ingestion System ===")

    class_name = input("Enter class (example: class_09): ").strip()
    subject = input("Enter subject (example: maths): ").strip()
    chapter = input("Enter chapter file name (example: ch_01.pdf): ").strip()

    # Download PDF
    download_pdf(class_name, subject, chapter)

    # Extract + Process
    raw_text = extract_text()
    cleaned_text = clean_text(raw_text)
    chunks = chunk_text(cleaned_text)

    print("\nTotal chunks created:", len(chunks))

    # Store in Supabase for teammate
    store_chunks_to_supabase(class_name, subject, chapter, chunks)

    # Build FAISS locally
    index = build_faiss_index(chunks)

    # Ask question
    query = input("\nEnter your question: ")
    results = search(index, chunks, query)

    print("\nTop relevant results:\n")

    for i, result in enumerate(results):
        print(f"\n--- Result {i+1} ---\n")
        print(result[:500])

    # Save FAISS locally
    faiss.write_index(index, "faiss_index.bin")
    print("\nFAISS index saved locally ✅")
