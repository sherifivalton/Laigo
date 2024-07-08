import os
from doctr.io import DocumentFile
from doctr.models import ocr_predictor, from_hub


class OcrPdfService:

    def __init__(self):
        self.reco_model = from_hub('Felix92/doctr-torch-parseq-multilingual-v1')
        self.predictor = ocr_predictor(det_arch='db_resnet50', reco_arch=self.reco_model, pretrained=True)

    def perform_ocr(self, file_path: str):
        try:
            doc = DocumentFile.from_pdf(file_path)
            result = self.predictor(doc)
            ocr_output = result.export()
            
            if not self.has_text(ocr_output):
                raise ValueError("There is no text in the PDF, please provide a PDF with text")

            return ocr_output
        except Exception as e:
            raise ValueError(f"Error during OCR processing: {e}")
    
    def has_text(self, ocr_output):
        for page in ocr_output.get('pages', []):
            for block in page.get('blocks', []):
                for line in block.get('lines', []):
                    if line.get('words'):
                        return True
        return False