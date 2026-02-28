# SmartTutor
Ai Tutor for Remote India-Cost Optimized RAG
with 60% token optimization

📄 Step 1: OCR Extraction from Scanned NCERT Textbook
## 📄 Step 1: OCR Extraction from Scanned NCERT Textbook

Since the NCERT textbook is scanned (image-based PDF), we implemented OCR using Tesseract.

### Tools Used:
- pytesseract
- pdf2image
- Poppler (for PDF to image conversion)

### Process:
1. Installed Tesseract OCR.
2. Installed Poppler for Windows.
3. Converted PDF pages into images.
4. Applied OCR to extract text.
5. Saved extracted raw text into `raw_text.txt`.

### Output:
- Successfully extracted readable text from scanned NCERT textbook.
