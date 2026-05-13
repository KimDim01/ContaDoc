import pytesseract
from PIL import Image
from pdf2image import convert_from_path
import os

class OCRProcessor:
    def __init__(self):
        # Tesseract needs to be installed on the OS
        # pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'
        pass

    def image_to_text(self, image_path: str) -> str:
        """Extracts text from an image file."""
        image = Image.open(image_path)
        text = pytesseract.image_to_string(image, lang='por+eng')
        return text

    def scanned_pdf_to_text(self, pdf_path: str) -> str:
        """Converts a scanned PDF to images and then extracts text."""
        pages = convert_from_path(pdf_path)
        full_text = []
        for page in pages:
            text = pytesseract.image_to_string(page, lang='por+eng')
            full_text.append(text)
        return "\n\n".join(full_text)

ocr_processor = OCRProcessor()
