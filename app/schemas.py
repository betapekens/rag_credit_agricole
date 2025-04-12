from pydantic import BaseModel, Field


class QuestionRequest(BaseModel):
    question: str = Field(
        example="In quale stagione è stata inaugurata la Coppa del Mondo di sci alpino?",
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
