from pydantic import BaseModel, Field


class QuestionRequest(BaseModel):
    """
    This class defines the structure for question-based requests, including
    the question text, number of documents to retrieve, and LLM model selection.

    Attributes:
        question (str): The question to be answered
        n_documents (int): Number of documents to retrieve for context
        llm_model (str): Name of the LLM model to use for answer generation
    """

    question: str = Field(
        example="In quale stagione è stata inaugurata la Coppa del Mondo di sci alpino?",
    )
    n_documents: int = Field(example=10)
    llm_model: str = Field(
        example="gpt-4o-mini",
        description="The LLM model to use for generating answers",
    )


class ProcessResponse(BaseModel):
    message: str
    markdown_path: str
    vector_db_path: str
    chunk_size: int
    chunk_overlap: int


class VectorDBRequest(BaseModel):
    chunk_size: int = Field(
        default=1000, description="Size of text chunks for vectorization"
    )
    chunk_overlap: int = Field(default=100, description="Overlap between text chunks")
