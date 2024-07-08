from pydantic import BaseModel
from typing import Any, Dict, List, Optional

class OCRResult(BaseModel):
    text: str
    numbers: List[float]

class OCRResponse(BaseModel):
    file_path: str
    ocr_result: OCRResult

class ErrorResponse(BaseModel):
    detail: str