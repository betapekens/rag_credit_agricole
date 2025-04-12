import os
from pathlib import Path
from mistralai import Mistral, DocumentURLChunk
from dotenv import load_dotenv
import logging


def load_api_key() -> str:
    """
    Load the Mistral API key from the environment variables.

    Returns:
        str: The Mistral API key.

    Raises:
        EnvironmentError: If the API key is not found in the environment.
    """
    load_dotenv()
    api_key = os.getenv("MISTRAL_API_KEY")
    if not api_key:
        raise EnvironmentError("Missing MISTRAL_API_KEY in environment.")
    return api_key


def upload_pdf(client: Mistral, pdf_path: Path):
    """
    Upload a PDF file to the Mistral API for OCR processing.

    Args:
        client (Mistral): The Mistral API client.
        pdf_path (Path): The path to the PDF file.

    Returns:
        dict: The response from the file upload API.

    Raises:
        FileNotFoundError: If the PDF file does not exist.
    """
    if not pdf_path.exists():
        raise FileNotFoundError(f"PDF not found at: {pdf_path}")
    return client.files.upload(
        file={
            "file_name": pdf_path.stem,
            "content": pdf_path.read_bytes(),
        },
        purpose="ocr",
    )


def run_ocr(client: Mistral, file_id: str) -> dict:
    """
    Perform OCR on an uploaded PDF file using the Mistral API.

    Args:
        client (Mistral): The Mistral API client.
        file_id (str): The ID of the uploaded file.

    Returns:
        dict: The OCR response containing extracted text and metadata.
    """
    signed_url = client.files.get_signed_url(file_id=file_id, expiry=1)
    response = client.ocr.process(
        document=DocumentURLChunk(document_url=signed_url.url),
        model="mistral-ocr-latest",
        include_image_base64=True,
    )
    return response


def ocr_pipeline(
    pdf_input: str = "data/pdfs/cdm-cai.pdf", md_output: str = "data/mds/output.md"
):
    """
    Complete OCR pipeline to process a PDF and save the extracted text as Markdown.

    Args:
        pdf_input (str): Path to the input PDF file.
        md_output (str): Path to save the output Markdown file.
    """
    api_key = load_api_key()

    logging.basicConfig(level=logging.INFO)
    logging.getLogger("httpx").setLevel(logging.WARNING)
    logging.info("Connecting to Mistral API...")
    client = Mistral(api_key=api_key)

    logging.info("Uploading PDF for OCR...")
    pdf_path = Path(pdf_input)
    uploaded_file = upload_pdf(client, pdf_path)

    logging.info("Running OCR on the uploaded PDF...")
    ocr_response = run_ocr(client, uploaded_file.id)
    markdown_content = "\n\n".join(page.markdown for page in ocr_response.pages)

    logging.info("OCR completed. Saving results to markdown file...")
    Path(md_output).parent.mkdir(parents=True, exist_ok=True)
    Path(md_output).write_text(markdown_content, encoding="utf-8")

    logging.info(f"Markdown content saved to {md_output}")


if __name__ == "__main__":
    ocr_pipeline()
