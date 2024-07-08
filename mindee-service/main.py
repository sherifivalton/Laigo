from fastapi import FastAPI
from controllers import ocr_controller

app = FastAPI()

app.include_router(ocr_controller.router, prefix="/api/ocr", tags=["OCR"])

@app.get("/")
async def root():
    return {"message": "Hello World"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)