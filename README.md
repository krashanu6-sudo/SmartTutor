# 📚 Smart Tutor – Ingestion & Chunking System

This module is responsible for:

1. Downloading textbook PDFs from Supabase Storage
2. Extracting text from the PDF
3. Cleaning the text
4. Performing advanced semantic chunking
5. Generating embeddings for each chunk
6. Storing chunks + embeddings in Supabase
7. Building a local FAISS index (for testing retrieval)

---

# 🧠 What This Module Does (Simple Explanation)

Think of this system like:

Step 1 → Take a big textbook  
Step 2 → Break it into small understandable pieces  
Step 3 → Convert each piece into numbers (embeddings)  
Step 4 → Store everything in the cloud  
Step 5 → Allow teammates to search inside it  

This prepares the data for the AI Tutor.

---

# 🗂 Project Flow

Supabase Storage (PDF)
        ↓
Text Extraction
        ↓
Clean Text
        ↓
Advanced Chunking
        ↓
Embedding Generation
        ↓
Supabase Table (book_chunks)
        ↓
Teammate builds vector search

---

# 📦 Supabase Setup

### Bucket Name
Store PDFs inside:


class_9/Science/Science_Ch01.pdf
class_9/Hindi/Hindi_Ch01.pdf


Folder structure must match:


class_name/subject/chapter.pdf


---

# 🗄 Supabase Table Structure

Table Name: `book_chunks`

Columns:

- id (auto)
- class (text)
- subject (text)
- chapter (text)
- chunk_index (integer)
- content (text)
- embedding (jsonb)

---

# ⚙️ How To Run

### 1. Activate Virtual Environment


venv\Scripts\activate


### 2. Install Requirements


pip install -r requirements.txt


(If no requirements file, manually install:)

pip install faiss-cpu sentence-transformers pymupdf supabase python-dotenv


### 3. Set Environment Variables (.env)


SUPABASE_URL=your_url
SUPABASE_KEY=your_key
BUCKET_NAME=your_bucket_name


### 4. Run Program


python main.py


Then enter:


class_9
Science
Science_Ch01


---

# 📊 What Gets Stored In Cloud

For each chunk we store:

- Clean text content
- Embedding vector (JSON format)
- Class, subject, chapter metadata

Example row:

| class   | subject  | chapter        | chunk_index | content        | embedding |
|----------|-----------|---------------|--------------|----------------|-----------|
| class_9 | Science  | Science_Ch01 | 0            | Matter is...   | [0.234...]|

---

# 🔍 How Teammates Can Use This

They can fetch chunks using:

```python
data = supabase.table("book_chunks") \
    .select("*") \
    .eq("class", "class_9") \
    .eq("subject", "Science") \
    .eq("chapter", "Science_Ch01") \
    .execute()

Then rebuild FAISS index from stored embeddings.

This allows distributed vector search.
