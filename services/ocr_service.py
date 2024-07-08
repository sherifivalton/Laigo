import magic
import os
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
            if not os.path.exists(file_path):
                raise FileNotFoundError(f"The file '{file_path}' does not exist.")
            
            try:
                with open(file_path, 'rb') as file:
                    file.read()
            except Exception as e:
                raise IOError(f"Failed to read the file '{file_path}'. It may be corrupted. Error: {e}")
            
            file_type = self.check_file_type(file_path)

            if file_type == 'image':
                json_response = self.image_service.perform_ocr(file_path)
            elif file_type == 'pdf':
                json_response = self.pdf_service.perform_ocr(file_path)
            else:
                raise ValueError("Unsupported file type")
            
            if not json_response:
                return {"No content found"}
            
            return self.postprocessing_service.post_process_ocr(json_response)
            
        except FileNotFoundError as e:
            raise ValueError(f"File not found: {e}")
        except IOError as e:
            raise ValueError(f"File I/O error: {e}")
        except ValueError as e:
            raise ValueError(f"Value error: {e}")
        except Exception as e:
            raise ValueError(f"An unexpected error occurred: {e}")
    
    def check_file_type(self, file_path: str):
        try:
            mime = magic.Magic(mime=True)
            mime_type = mime.from_file(file_path)
            if mime_type.startswith('image'):
                try:
                    DocumentFile.from_images(file_path)
                    return 'image'
                except Exception:
                    pass
            if mime_type == 'application/pdf':
                try:
                    DocumentFile.from_pdf(file_path)
                    return 'pdf'
                except Exception:
                    pass
            try:
                DocumentFile.from_images(file_path)
                return 'image'
            except Exception:
                pass
            try:
                DocumentFile.from_pdf(file_path)
                return 'pdf'
            except Exception:
                pass
            raise ValueError("Unsupported file type or the file is corrupted")
        except Exception as e:
            raise ValueError(f"Error checking file type: {e}")
        
        
        