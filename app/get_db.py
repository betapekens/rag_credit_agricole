from langchain_chroma import Chroma
from langchain_community.embeddings import FastEmbedEmbeddings


def get_db() -> Chroma:
    """
    Creates and returns a RetrievalQA chain with specified number of documents to retrieve.

    Args:
        n_documents (int): Number of documents to retrieve for each query. Defaults to 10.

    Returns:
        RetrievalQA: A question-answering chain that combines document retrieval with LLM.
    """
    # Initialize embedding model and Chroma database
    embedding_model = FastEmbedEmbeddings()
    db = Chroma(persist_directory="chroma_db", embedding_function=embedding_model)

    return db
