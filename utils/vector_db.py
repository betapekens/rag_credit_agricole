import logging
from pathlib import Path
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_chroma import Chroma
from langchain_community.embeddings import FastEmbedEmbeddings

# Configure logging
logging.basicConfig(level=logging.INFO)
# Disable Chroma's auto logging
logging.getLogger("chromadb").setLevel(logging.WARNING)


def process_text_to_embeddings(
    text: str, persist_directory: str, chunk_size: int, chunk_overlap: int
) -> Chroma:
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=chunk_size, chunk_overlap=chunk_overlap
    )
    chunks = splitter.split_text(text)

    logging.info("Initializing embedding model.")
    embedding_model = FastEmbedEmbeddings()

    logging.info("Creating Chroma database from text chunks.")
    return Chroma.from_texts(
        chunks, embedding_model, persist_directory=persist_directory
    )


def vectorize(
    input_file: str = "data/mds/output.md",
    persist_directory: str = "chroma_db",
    chunk_size: int = 1000,
    chunk_overlap: int = 200,
):
    # Ensure the input_file is treated as a Path
    file_path = Path(input_file)

    # Load text from the file
    if not file_path.exists():
        logging.error(f"File not found at: {file_path}")
        raise FileNotFoundError(f"File not found at: {file_path}")
    else:
        logging.info(f"Reading text from file: {file_path}")
        text = file_path.read_text(encoding="utf-8")

    # Process text and store embeddings
    logging.info("Processing text to generate embeddings.")
    process_text_to_embeddings(text, persist_directory, chunk_size, chunk_overlap)

    logging.info(f"Embeddings successfully stored in {persist_directory}")


if __name__ == "__main__":
    vectorize()
