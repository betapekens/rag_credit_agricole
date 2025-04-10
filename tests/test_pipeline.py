import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from utils import ocr_pipeline
from utils import vectorize


def test_ocr_pipeline():
    input_pdf = "tests/cdm-cai.pdf"
    output_md = "tests/output.md"

    # Clean up from previous runs
    if os.path.exists(output_md):
        os.remove(output_md)

    ocr_pipeline(pdf_input=input_pdf, md_output=output_md)

    assert os.path.exists(output_md)
    with open(output_md, "r", encoding="utf-8") as f:
        content = f.read()
        assert len(content) > 1


def test_vectorize():
    input_md = "tests/output.md"
    persist_directory = "tests/chroma_db"
    chunk_size = 1000
    chunk_overlap = 200

    # Clean up from previous runs
    if os.path.exists(persist_directory):
        import shutil

        shutil.rmtree(persist_directory)

    vectorize(
        input_file=input_md,
        persist_directory=persist_directory,
        chunk_size=chunk_size,
        chunk_overlap=chunk_overlap,
    )

    assert os.path.exists(persist_directory)
