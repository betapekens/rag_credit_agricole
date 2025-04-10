import sys
import os
import shutil

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from utils import vectorize


def test_vectorize():
    input_md = "tests/output.md"
    persist_directory = "tests/chroma_db"
    chunk_size = 1000
    chunk_overlap = 200

    # Ensure the input file exists
    assert os.path.exists(
        input_md
    ), f"Input markdown file '{input_md}' does not exist. Run 'test_ocr_pipeline' first."

    # Clean up from previous runs
    if os.path.exists(persist_directory):
        shutil.rmtree(persist_directory)

    # Run the vectorization
    vectorize(
        input_file=input_md,
        persist_directory=persist_directory,
        chunk_size=chunk_size,
        chunk_overlap=chunk_overlap,
    )

    # Assert the output directory exists
    assert os.path.exists(
        persist_directory
    ), f"Persist directory '{persist_directory}' was not created."

    # Assert the output directory is not empty
    assert (
        len(os.listdir(persist_directory)) > 0
    ), f"Persist directory '{persist_directory}' is empty."

    # Cleanup after test
    shutil.rmtree(persist_directory)
