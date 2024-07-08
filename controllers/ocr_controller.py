from fastapi import APIRouter, File, UploadFile, HTTPException
from fastapi.responses import JSONResponse
import shutil
import os
from pydantic import BaseModel
from typing import List, Dict, Any
from services.ocr_service import OcrService

router = APIRouter()

UPLOAD_DIR = "uploaded_files"
if not os.path.exists(UPLOAD_DIR):
    os.makedirs(UPLOAD_DIR)

class OCRResponse(BaseModel):
    file_path: str
    ocr_result: Dict[str, Any]

class ErrorResponse(BaseModel):
    detail: str

@router.post(
    "/upload",
    response_model=OCRResponse,
    responses={
        200: {
            "description": "Successful Response",
            "content": {
                "application/json": {
                    "example": {
                        "file_path": "uploaded_files/Image-Invoice.png",
                        "ocr_result": {
                            "text": "Invoice 2022435\nTax invoice\nYour Business\nName\nBILL TO\n19/7/2022\nYour Client\nIssue date:\nDue date:\n3/8/2022\n100 Harris St\nSydney NSW NSW 2009\nReference:\n2022435\nAustralia\nTotal due (AUD)\nInvoice No.\nIssue date\nDue date\n$2,510.00\n2022435\n19/7/2022\n3/8/2022\nUnit price...",
                            "numbers": [2022435, 19, 7, 2022, 3, 8, 2022, 100, 2009]
                        }
                    }
                }
            }
        },
    400: {
            "description": "Value Error",
            "model": ErrorResponse,
            "content": {
                "application/json": {
                    "examples": {
                        "unsupported_file": {
                            "summary": "Unsupported file type",
                            "value": {"detail": "Value error: Unsupported file type"}
                        },
                        "no_text_in_image": {
                            "summary": "No text in image",
                            "value": {"detail": "Value error: There is no text in the image, please provide an image with text"}
                        },
                        "no_text_in_pdf": {
                            "summary": "No text in PDF",
                            "value": {"detail": "Value error: There is no text in the PDF, please provide a PDF with text"}
                        },
                        "ocr_processing_error": {
                            "summary": "OCR processing error",
                            "value": {"detail": "Value error: Error during OCR processing: There is no text in the image, please provide an image with text"}
                        }
                    }
                }
            }
        },
        404: {
            "description": "File Not Found",
            "model": ErrorResponse,
            "content": {
                "application/json": {
                    "example": {
                        "detail": "File not found: The file 'filename' does not exist."
                    }
                }
            }
        },
        422: {
            "description": "File I/O Error",
            "model": ErrorResponse,
            "content": {
                "application/json": {
                    "example": {
                        "detail": "File I/O error: Failed to read the file 'filename'. It may be corrupted. Error: [specific error]"
                    }
                }
            }
        }
    },
    summary="Upload a File for OCR",
    description="This endpoint allows you to upload an image or PDF file for OCR processing. The response includes the extracted text and any identified numbers."
)
async def upload_file(files: UploadFile = File(...)):
    file_path = os.path.join(UPLOAD_DIR, files.filename)
    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(files.file, buffer)

    try:
        ocr_result = OcrService().perform_ocr(file_path)
        return JSONResponse(content={"file_path": file_path, "ocr_result": ocr_result})
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except FileNotFoundError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except IOError as e:
        raise HTTPException(status_code=422, detail=str(e))