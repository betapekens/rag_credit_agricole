from fastapi import APIRouter, HTTPException, UploadFile, File
from pathlib import Path
import shutil
from .schemas import QuestionRequest, ProcessResponse, VectorDBRequest
from .qa_chain import get_qa_chain
from utils import ocr_pipeline, vectorize

router = APIRouter()
qa_chain = None


@router.post("/upload_pdf")
async def upload_pdf(file: UploadFile = File(...)):
    try:
        # Save uploaded PDF to a fixed location
        pdf_path = Path("data/input.pdf")
        with pdf_path.open("wb") as buffer:
            shutil.copyfileobj(file.file, buffer)

        # Create path for markdown output
        md_path = Path("data/mds/output.md")
        md_path.parent.mkdir(parents=True, exist_ok=True)

        # Run OCR pipeline
        ocr_pipeline(pdf_input=str(pdf_path), md_output=str(md_path))

        return {
            "message": "PDF uploaded and processed successfully",
            "markdown_path": str(md_path),
        }

    except Exception as e:
        raise HTTPException(
            status_code=500, detail=f"Error uploading and processing PDF: {str(e)}"
        )


@router.post("/create_vector_db", response_model=ProcessResponse)
async def create_vector_db(request: VectorDBRequest):
    try:
        global qa_chain
        # Check if markdown file exists
        md_path = Path("data/mds/output.md")
        if not md_path.exists():
            raise HTTPException(
                status_code=400,
                detail="Markdown file not found. Please upload and process a PDF first.",
            )

        # Create path for vector database
        vector_db_path = Path("chroma_db")
        vector_db_path.mkdir(parents=True, exist_ok=True)

        # Vectorize the markdown content with custom chunk parameters
        vectorize(
            input_file=str(md_path),
            persist_directory=str(vector_db_path),
            chunk_size=request.chunk_size,
            chunk_overlap=request.chunk_overlap,
        )

        # Refresh the QA chain after creating new vectors
        qa_chain = get_qa_chain()

        return ProcessResponse(
            message="Vector database created successfully",
            markdown_path=str(md_path),
            vector_db_path=str(vector_db_path),
            chunk_size=request.chunk_size,
            chunk_overlap=request.chunk_overlap,
        )
    except HTTPException as http_exc:
        raise http_exc
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/ask")
def ask_question(request: QuestionRequest):
    try:
        global qa_chain
        # Check if the Chroma database exists
        db_path = Path("chroma_db")
        if not db_path.exists() or not any(db_path.iterdir()):
            raise HTTPException(
                status_code=400,
                detail="Vector database not found. Please create the vector database first.",
            )

        # Use the existing QA chain or create a new one if it doesn't exist
        if qa_chain is None:
            qa_chain = get_qa_chain()

        # Use invoke to run the RAG pipeline synchronously
        result = qa_chain.invoke({"query": request.question})
        return {
            "answer": result["result"],
            "source_documents": result["source_documents"],
        }
    except HTTPException as http_exc:
        raise http_exc
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
