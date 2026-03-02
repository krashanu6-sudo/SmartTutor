📚 Smart Tutor – AI Textbook Ingestion Engine
🧠 Project Overview

This module is the core engine of the Smart Tutor system.

It is responsible for:

Fetching textbooks from Supabase storage

Extracting text from scanned PDFs using OCR

Cleaning and preprocessing the text

Breaking text into smart overlapping chunks

Generating embeddings (vector representations)

Storing them in FAISS for fast similarity search

Retrieving relevant content based on user questions

This system is designed for Class 9–12 textbooks.

🏗️ How The System Works
Step 1: User selects

Class (example: class_09)

Subject (example: maths)

Chapter file (example: ch_01.pdf)

Step 2: System downloads PDF

The selected chapter is downloaded from Supabase Storage.

Step 3: OCR Extraction

Since many textbooks are scanned PDFs, we use:

Poppler → converts PDF to images

Tesseract OCR → extracts text from images

Step 4: Text Cleaning

We remove:

Extra spaces

Unwanted characters

Noise from OCR

Step 5: Smart Chunking

Text is split into chunks using:

Chunk size: 600 words

Overlap: 100 words

This ensures:

Context continuity

Better semantic understanding

Step 6: Embedding Generation

We use:

sentence-transformers/all-MiniLM-L6-v2

Each chunk is converted into a numeric vector representation.

Step 7: FAISS Indexing

We store vectors inside FAISS for:

Fast similarity search

Low memory usage

Scalable retrieval

Step 8: Semantic Search

When a user asks a question:

Question is converted to embedding

FAISS finds top 5 most relevant chunks

Relevant content is returned

📂 Supabase Storage Structure

The bucket must follow this format:

books/
│
├── class_9/
│   ├── Maths/
│   │   ├── Maths_Ch01.pdf
│   │   ├── Maths_Ch02.pdf
│   ├── science/
│
├── class_10/
│   ├── maths/
│   ├── science/
│
├── class_11/
├── class_12/

⚠ Folder names are case-sensitive.

⚙️ Installation Guide
1️⃣ Clone the repository
git clone https://github.com/krashanu6-sudo/SmartTutor.git
2️⃣ Create Virtual Environment
py -3.11 -m venv venv
venv\Scripts\activate
3️⃣ Install Dependencies
pip install -r requirements.txt
4️⃣ Install Required Tools (Windows)
Install Tesseract OCR

Download and install:
https://github.com/tesseract-ocr/tesseract

Default path:

C:\Program Files\Tesseract-OCR\tesseract.exe
Install Poppler

Download:
https://github.com/oschwartz10612/poppler-windows/releases

Extract to:

C:\poppler

Make sure:

C:\poppler\Library\bin

contains:

pdfinfo.exe
pdftoppm.exe
5️⃣ Create .env File

Inside project root:

SUPABASE_URL=your_project_url
SUPABASE_KEY=your_publishable_key
BUCKET_NAME=books

⚠ Do NOT commit .env file.

▶ Running The System
python main.py

You will be asked:

Enter class:
Enter subject:
Enter chapter:
Enter your question:

Example:

class_9
Maths
Maths_Ch01.pdf
What are real numbers?

The system will:

Download the chapter

Extract text

Build vector index

Retrieve relevant content

💾 Index Caching

After first run:

faiss_index.bin

chunks.json

Are saved locally.

Next time, system loads index directly (faster performance).

🧩 Technologies Used

Python 3.11

Supabase (Cloud Storage)

Tesseract OCR

Poppler

SentenceTransformers

FAISS

NumPy

🎯 Why This Module Is Important

This is the foundation layer of the Smart Tutor system.

Without this:

No document ingestion

No semantic retrieval

No context pruning

No cost optimization

This module enables:

Low-cost retrieval

Faster LLM queries

Scalable textbook indexing

🚀 Future Integration

This module will connect with:

FastAPI backend

LLM model (OpenAI / Gemini / etc.)

Context pruning layer

Token cost comparison system

👑 Contribution

This module handles the complete ingestion and vectorization pipeline and serves as the core retrieval engine for the Smart Tutor system.
