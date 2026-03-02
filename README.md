# SmartTutor
Ai Tutor for Remote India-Cost Optimized RAG
with 60% token optimization

# 📚 Smart Tutor – Document Ingestion & Vector Engine

## 🚀 Overview

This module handles:

- Supabase PDF fetching
- OCR extraction (Tesseract + Poppler)
- Text cleaning
- Overlapping chunking
- Embedding generation (SentenceTransformers)
- FAISS vector indexing
- Semantic retrieval

This is the core ingestion and retrieval engine for the Smart Tutor system (Class 9–12).

---

## 🏗️ Architecture

Supabase → Download PDF  
→ OCR Extraction  
→ Text Cleaning  
→ Chunking  
→ Embeddings  
→ FAISS Index  
→ Semantic Search  

---

## ⚙️ Setup

1. Create virtual environment
2. Install requirements:


pip install -r requirements.txt


3. Create `.env`:


SUPABASE_URL=your_url
SUPABASE_KEY=your_key
BUCKET_NAME=books


4. Run:


python main.py


---

## 📌 Notes

- Folder structure in Supabase must follow:
  books/class_xx/subject/chapter.pdf
- Case sensitive paths.
- Index is cached locally after first build
