# RAG Credit Agricole

A Retrieval-Augmented Generation (RAG) system for analyzing PDF documents using OCR and vector embeddings.

## Features

- PDF document OCR processing using Mistral AI
- Markdown conversion of OCR results 
- Vector embeddings using FastEmbed
- Document retrieval using ChromaDB
- Question answering using LangChain and OpenAI

## Project Structure

```
├── app/
│   └── main.py           # FastAPI application
├── data/
│   ├── mds/             # Markdown output files
│   └── pdfs/            # PDF input files
├── notebooks/           # Jupyter notebooks
├── utils/
│   ├── ocr_to_markdown.py  # OCR processing utilities
│   └── vector_db.py        # Vector database utilities
├── .env                 # Environment variables
├── .gitignore          # Git ignore file
├── README.md           # Project documentation
└── requirements.txt    # Python dependencies
```

## Setup

1. Create a virtual environment and activate it:
```bash
python -m venv venv
source venv/bin/activate  # Linux/Mac
# or
.\venv\Scripts\activate  # Windows
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Create `.env` file with required API keys:
```
MISTRAL_API_KEY=your_mistral_api_key
OPENAI_API_KEY=your_openai_api_key
```

## Usage

1. Place PDF files in `data/pdfs/` directory

2. Run OCR processing:
```bash
python utils/ocr_to_markdown.py
```

3. Convert to vector database:
```bash
python utils/vector_db.py
```

4. Start the API server:
```bash
uvicorn app.main:app --reload
```

5. Query the API:
```bash
curl -X POST http://localhost:8000/ask \
  -H "Content-Type: application/json" \
  -d '{"question":"In quale stagione è stata inaugurata la Coppa del Mondo di sci alpino?"}'
```