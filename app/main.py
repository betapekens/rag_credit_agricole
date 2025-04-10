from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field
from langchain_chroma import Chroma
from langchain_community.embeddings import FastEmbedEmbeddings
from langchain_openai import ChatOpenAI
from langchain.chains import RetrievalQA
from load_dotenv import load_dotenv
import os

# Initialize FastAPI app
app = FastAPI()

# Initialize embedding model and Chroma database
embedding_model = FastEmbedEmbeddings()
db = Chroma(persist_directory="chroma_db", embedding_function=embedding_model)

# Create retriever
retriever = db.as_retriever(search_type="similarity", search_kwargs={"k": 10})


# Load environment variables
load_dotenv()
openai_api_key = os.getenv("OPENAI_API_KEY")

# Set up LLM (OpenAI Chat model)
llm = ChatOpenAI(
    model="gpt-4o-mini",
    temperature=0,
    max_tokens=None,
    timeout=None,
    max_retries=2,
    openai_api_key=openai_api_key,
)

# Set up RAG pipeline
qa_chain = RetrievalQA.from_chain_type(
    llm=llm, retriever=retriever, return_source_documents=True
)


# Define request body schema
class QuestionRequest(BaseModel):
    question: str = Field(
        ...,
        example="In quale stagione è stata inaugurata la Coppa del Mondo di sci alpino?",
    )


# Create the endpoint to answer questions
@app.post("/ask")
def ask_question(request: QuestionRequest):
    try:
        # Use invoke to run the RAG pipeline synchronously
        result = qa_chain.invoke({"query": request.question})
        return {
            "answer": result["result"],
            "source_documents": result["source_documents"],
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
