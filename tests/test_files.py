import os
import sys
import pytest

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from services.ocr_service import OcrService


SAMPLES_DIR = "samples"

def test_pdf_file():
    file_path = os.path.join(SAMPLES_DIR, "PDF-Invoice_MultiPage.pdf")
    ocr_service = OcrService()
    file_type = ocr_service.check_file_type(file_path)
    assert file_type == "pdf", f"Expected 'pdf', but got '{file_type}'"

def test_image_file():
    file_path = os.path.join(SAMPLES_DIR, "Image_Invoice.png")
    ocr_service = OcrService()
    file_type = ocr_service.check_file_type(file_path)
    assert file_type == "image", f"Expected 'image', but got '{file_type}'"

def test_corrupt_image_file():
    file_path = os.path.join(SAMPLES_DIR, "Image_Corrupt.png")
    ocr_service = OcrService()
    with pytest.raises(ValueError, match="Unsupported file type or the file is corrupted"):
        ocr_service.check_file_type(file_path)

def test_corrupt_pdf_file():
    file_path = os.path.join(SAMPLES_DIR, "PDF_Corrupt - Corrupt.pdf")
    ocr_service = OcrService()
    with pytest.raises(ValueError, match="Unsupported file type or the file is corrupted"):
        ocr_service.check_file_type(file_path)

def test_image_no_text_file():
    file_path = os.path.join(SAMPLES_DIR, "Image_Invoice _No_Text.png")
    ocr_service = OcrService()
    file_type = ocr_service.check_file_type(file_path)
    assert file_type == "image", f"Expected 'image', but got '{file_type}'"