import pytesseract
import sys
from pdf2image import convert_from_bytes
from PIL import Image

# Set tesseract path on Linux cloud deployments
if sys.platform.startswith('linux'):
    pytesseract.pytesseract.tesseract_cmd = "/usr/bin/tesseract"

def extract_text_from_image(image_file):
    try:
        # Open in-memory image file using PIL
        img = Image.open(image_file)
        text = pytesseract.image_to_string(img)
        if not text.strip():
            return "Warning: OCR succeeded but no text was found in the image."
        return text
    except Exception as e:
        return f"Error extracting text from image: {str(e)}\n\n💡 Troubleshooting:\n- Ensure Tesseract OCR is installed on your machine.\n- For Windows, make sure Tesseract is added to your PATH or configured."

def extract_text_from_pdf(pdf_file):
    try:
        # Convert uploaded file-like object bytes directly
        pages = convert_from_bytes(pdf_file.read())
        text = ""
        for page in pages:
            text += pytesseract.image_to_string(page)
        if not text.strip():
            return "Warning: PDF parsed successfully but no text could be extracted from its pages."
        return text
    except Exception as e:
        return f"Error extracting text from PDF: {str(e)}\n\n💡 Troubleshooting:\n- Ensure 'poppler' and 'tesseract-ocr' are installed.\n- Check packages.txt and requirements.txt if running on Streamlit Cloud."
