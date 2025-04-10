import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from utils import ocr_pipeline


def test_ocr_pipeline():
    input_pdf = "tests/cdm-cai.pdf"
    output_md = "tests/output.md"

    # Clean up from previous runs
    if os.path.exists(output_md):
        os.remove(output_md)

    # Run the OCR pipeline
    ocr_pipeline(pdf_input=input_pdf, md_output=output_md)

    # Assert the output file exists
    assert os.path.exists(
        output_md
    ), f"Output markdown file '{output_md}' was not created."

    # Assert the output file is not empty
    with open(output_md, "r", encoding="utf-8") as f:
        content = f.read()
        assert len(content.strip()) > 0, "Output markdown file is empty."
