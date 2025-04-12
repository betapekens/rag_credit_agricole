from fastapi import FastAPI, HTTPException, UploadFile, File
from pydantic import BaseModel, Field
from langchain_chroma import Chroma
from langchain_community.embeddings import FastEmbedEmbeddings
from langchain_openai import ChatOpenAI
from langchain.chains import RetrievalQA
from pathlib import Path
import shutil
from utils import ocr_pipeline, vectorize
from dotenv import load_dotenv
import os

# Initialize FastAPI app
app = FastAPI()

# Load environment variables
load_dotenv()
openai_api_key = os.getenv("OPENAI_API_KEY")


def get_qa_chain():
    # Initialize embedding model and Chroma database
    embedding_model = FastEmbedEmbeddings()
    db = Chroma(persist_directory="chroma_db", embedding_function=embedding_model)

    # Create retriever
    retriever = db.as_retriever(search_type="similarity", search_kwargs={"k": 10})

    # Set up LLM
    llm = ChatOpenAI(
        model="gpt-4o-mini",
        temperature=0,
        max_tokens=None,
        timeout=None,
        max_retries=2,
        openai_api_key=openai_api_key,
    )

    # Return new QA chain
    return RetrievalQA.from_chain_type(
        llm=llm, retriever=retriever, return_source_documents=True
    )


# Define request body schemas
class QuestionRequest(BaseModel):
    question: str = Field(
        ...,
        example="In quale stagione è stata inaugurata la Coppa del Mondo di sci alpino?",
    )


class ProcessResponse(BaseModel):
    message: str
    markdown_path: str
    vector_db_path: str


@app.post("/process_pdf", response_model=ProcessResponse)
async def process_pdf(file: UploadFile = File(...)):
    try:
        # Save uploaded PDF to a fixed location
        pdf_path = Path("data/input.pdf")
        with pdf_path.open("wb") as buffer:
            shutil.copyfileobj(file.file, buffer)

        # Create paths for output
        md_path = Path("data/mds/output.md")
        vector_db_path = Path("chroma_db")

        # Ensure directories exist
        md_path.parent.mkdir(parents=True, exist_ok=True)
        vector_db_path.mkdir(parents=True, exist_ok=True)

        # Run OCR pipeline
        ocr_pipeline(pdf_input=str(pdf_path), md_output=str(md_path))

        # Vectorize the markdown content
        vectorize(input_file=str(md_path), persist_directory=str(vector_db_path))

        return ProcessResponse(
            message="PDF processed successfully",
            markdown_path=str(md_path),
            vector_db_path=str(vector_db_path),
        )

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error processing PDF: {str(e)}")


@app.post("/ask")
def ask_question(request: QuestionRequest):
    try:
        # Get a fresh QA chain with the latest database
        qa_chain = get_qa_chain()

        # Use invoke to run the RAG pipeline synchronously
        result = qa_chain.invoke({"query": request.question})
        return {
            "answer": result["result"],
            "source_documents": result["source_documents"],
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
