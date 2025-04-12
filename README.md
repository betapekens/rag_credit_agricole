# RAG Credit Agricole

A Retrieval-Augmented Generation (RAG) system for analyzing PDF documents using OCR and vector embeddings.

## Setup

1. Create a virtual environment and activate it:
```bash
uv venv
. venv/bin/activate
```

2. Install dependencies:
```bash
uv pip install -r requirements.txt
```

3. Create `.env` file with required API keys:
```
MISTRAL_API_KEY=your_mistral_api_key
OPENAI_API_KEY=your_openai_api_key
```
4. Load `.env` with:
```bash
. .env
```

## Commits

### Pre-commit Hooks

To ensure code quality and consistency, set up pre-commit hooks:

2. Install the hooks defined in `.pre-commit-config.yaml`:
  ```bash
  pre-commit install
  ```

3. Run the hooks manually on all files:
  ```bash
  pre-commit run --all-files
  ```

Pre-commit hooks will now automatically run on every commit to check and format your code.


## Usage

1. Start the API server:
```bash
docker build -t rag-api .
docker run --name rag-api-container -p 8000:8000 rag-api
```

2. Upload a PDF file:
```bash
curl -X POST http://localhost:8000/upload_pdf \
  -H "Content-Type: multipart/form-data" \
  -F "file=@data/pdfs/your_pdf.pdf"
```

3. Create the vector database (with optional chunking parameters):
```bash
curl -X POST http://localhost:8000/create_vector_db \
  -H "Content-Type: application/json" \
  -d '{
    "chunk_size": 1000,
    "chunk_overlap": 100
  }'
```

4. Query the API:
```bash
curl -X POST http://localhost:8000/ask \
  -H "Content-Type: application/json" \
  -d '{"question":"In quale stagione è stata inaugurata la Coppa del Mondo di sci alpino?"}'
```

  Alternatively, you can access the FastAPI Swagger UI for an interactive experience. Open your browser and navigate to [http://localhost:8000/docs](http://localhost:8000/docs) to explore and test the API endpoints.

## TODO
- Better implementation of `.env` for docker deployement.
- Implement error handling for missing or invalid `.env` configurations.
- Write detailed documentation for API endpoints.
- Add logging and monitoring for the API service.
- Explore integration with cloud-based vector databases.
- Add examples of real-world use cases in the documentation.