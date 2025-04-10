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

    ocr_pipeline(pdf_input=input_pdf, md_output=output_md)

    assert os.path.exists(output_md)
    with open(output_md, "r", encoding="utf-8") as f:
        content = f.read()
        assert len(content) > 1
