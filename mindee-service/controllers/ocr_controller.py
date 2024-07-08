from fastapi import APIRouter, File, UploadFile, HTTPException
from fastapi.responses import JSONResponse, PlainTextResponse
import shutil
import os
from services.ocr_service import OcrService

router = APIRouter()

UPLOAD_DIR = "uploaded_files"
if not os.path.exists(UPLOAD_DIR):
    os.makedirs(UPLOAD_DIR)

@router.post("/upload")
async def upload_file(files: UploadFile = File(...)):
    file_path = os.path.join(UPLOAD_DIR, files.filename)
    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(files.file, buffer)

    try:
        ocr_result = OcrService().perform_ocr(file_path)
        # return JSONResponse(content={"file_path": file_path, "ocr_result": ocr_result})
        return PlainTextResponse(content=ocr_result)
    except ValueError as e:
        raise HTTPException(status_code=500, detail=str(e))