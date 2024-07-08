import magic
from doctr.io import DocumentFile
from doctr.models import ocr_predictor, from_hub
from services.ocr_image_service import OcrImageService
from services.ocr_pdf_service import OcrPdfService
from services.postprocessing_service import PostProcessingService



class OcrService:
    
    def __init__(self):
        self.image_service = OcrImageService()
        self.pdf_service = OcrPdfService()
        self.postprocessing_service = PostProcessingService()

    def perform_ocr(self, file_path: str):
        json_response = {}        
        try:
            file_type = self.check_file_type(file_path)
            if file_type == 'image':
                json_response = self.image_service.perform_ocr(file_path)
            elif file_type == 'pdf':
                json_response = self.pdf_service.perform_ocr(file_path)
            else:
                raise ValueError("Unsupported file type")
        except Exception as e:
            raise ValueError(f"Error during OCR processing: {e}")
        
        if not json_response:
            return {"No content found"}
        return self.postprocessing_service.post_process_ocr(json_response)
    
    def check_file_type(self, file_path: str):
        try:
            mime = magic.Magic(mime=True)
            mime_type = mime.from_file(file_path)
            if mime_type.startswith('image'):
                return 'image'
            elif mime_type == 'application/pdf':
                return 'pdf'
            else:
                raise ValueError("Unsupported file type")
        except Exception as e:
            raise ValueError(f"Error checking file type: {e}")
        
        
        