from doctr.io import DocumentFile
from doctr.models import ocr_predictor, from_hub

reco_model = from_hub('Felix92/doctr-torch-parseq-multilingual-v1')

# Initialize the OCR predictor with the detection and recognition models
predictor = ocr_predictor(det_arch='db_resnet50',
                                       reco_arch=reco_model,
                                       pretrained=True)

doc = DocumentFile.from_images('Image_Invoice.png')
result = predictor(doc)
#result.show()
#print(result.export()) format in json
print(result.render())
# image = DocumentFile.from_images('Image_Invoice.png')
# pdf = DocumentFile.from_pdf('Invoice_Template.pdf')
# Load a custom detection model from huggingface hub
# det_model = from_hub('Felix92/doctr-tf-db-resnet50')
# Load a custom recognition model from huggingface hub
# reco_model = from_hub('Felix92/doctr-tf-crnn-vgg16-bn-french')
# You can easily plug in this models to the OCR predictor
# predictor = ocr_predictor(det_arch=det_model, reco_arch=reco_model)
# result = predictor(image)




        