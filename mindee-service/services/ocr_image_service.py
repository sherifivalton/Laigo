import os
from doctr.io import DocumentFile
from doctr.models import ocr_predictor, from_hub


class OcrImageService:

    def __init__(
        self
    ):
        self.reco_model = from_hub(
            'Felix92/doctr-torch-parseq-multilingual-v1')
        self.predictor = ocr_predictor(det_arch='db_resnet50',
                                       reco_arch=self.reco_model, pretrained=True)

    def perform_ocr(self, file_path: str):
        try:
            doc = DocumentFile.from_images(file_path)
            result = self.predictor(doc)
            return result.export()
        except Exception as e:
            raise ValueError(f"Error during OCR processing: {e}")
