from langchain_chroma import Chroma
from langchain_community.embeddings import FastEmbedEmbeddings
from langchain_openai import ChatOpenAI
from langchain.chains import RetrievalQA
import os
from dotenv import load_dotenv

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
