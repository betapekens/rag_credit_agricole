from fastapi import APIRouter, HTTPException, UploadFile, File
from pathlib import Path
import shutil
from .schemas import QuestionRequest, ProcessResponse, VectorDBRequest
from .get_db import get_db
from utils import ocr_pipeline, vectorize
from langchain_openai import ChatOpenAI
from langchain.chains import RetrievalQA
import os
from dotenv import load_dotenv

router = APIRouter()
db = None


# Load environment variables
load_dotenv()
openai_api_key = os.getenv("OPENAI_API_KEY")


@router.post("/upload_pdf")
async def upload_pdf(file: UploadFile = File(...)):
    """
    Process uploaded PDF file through OCR pipeline and save as markdown.

    Args:
        file (UploadFile): Uploaded PDF file

    Returns:
        dict: Success message and path to generated markdown
    """
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
    """
    Creates a vector database from markdown content with specified chunking parameters.

    Args:
        request (VectorDBRequest): Request object containing chunk_size and chunk_overlap parameters

    Returns:
        ProcessResponse: Response object containing processing details and paths

    Raises:
        HTTPException: If markdown file not found or processing error occurs
    """
    try:
        global db
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
        db = get_db()

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
    """
    This function takes a question from the user and returns an answer using a QA chain
    that queries a Chroma vector database.

    Args:
        request (QuestionRequest): A request object containing the user's question and the number of documents.
                                 Expected to have a 'question' attribute.

    Returns:
        dict: A dictionary containing:
            - answer (str): The generated answer to the question
            - source_documents (list): List of source documents used to generate the answer

    Raises:
        HTTPException:
            - 400 if the vector database is not found
            - 500 if any other error occurs during processing
    """
    try:
        global db

        # Check if the Chroma database exists
        db_path = Path("chroma_db")
        if not db_path.exists() or not any(db_path.iterdir()):
            raise HTTPException(
                status_code=400,
                detail="Vector database not found. Please create the vector database first.",
            )

        # Use the existing QA chain or create a new one if it doesn't exist
        if db is None:
            db = get_db()

        # Create retriever
        retriever = db.as_retriever(
            search_type="similarity", search_kwargs={"k": request.n_documents}
        )

        # Set up LLM
        llm = ChatOpenAI(
            model=request.llm_model,
            temperature=0,
            max_tokens=None,
            timeout=None,
            max_retries=2,
            openai_api_key=openai_api_key,
        )

        # Create the RetrievalQA chain
        qa_chain = RetrievalQA.from_chain_type(
            llm=llm, retriever=retriever, return_source_documents=True
        )

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
