import fitz  # This is PyMuPDF
import pytesseract
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter

# 1. Point to your Tesseract Installation
# Ensure this path matches where you installed Tesseract
pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'

INPUT_PDF = r'e:\OL SCIENCE\science G-11  P-II E.pdf'
OUTPUT_PDF = r'E:\OL SCIENCE\science_digital_4.pdf'

def convert_no_poppler():
    print("--- 🚀 Starting OCR (No Poppler Required) ---")
    
    try:
        # Open the scanned PDF using fitz (PyMuPDF)
        doc = fitz.open(INPUT_PDF)
        c = canvas.Canvas(OUTPUT_PDF, pagesize=letter)
        
        print(f"📖 Reading {len(doc)} pages...")
        
        for page_num in range(len(doc)):
            page = doc.load_page(page_num)
            
            # This turns the page into an image (pixmap) WITHOUT Poppler
            pix = page.get_pixmap(matrix=fitz.Matrix(2, 2)) # 2x2 matrix increases resolution
            
            # Convert pixmap to a format Tesseract understands
            img_data = pix.tobytes("png")
            
            # Run OCR directly on the image data
            import io
            from PIL import Image
            text = pytesseract.image_to_string(Image.open(io.BytesIO(img_data)))
            
            # Write extracted text to the new PDF
            text_object = c.beginText(40, 750)
            text_object.setFont("Helvetica", 10)
            
            for line in text.split('\n'):
                text_object.textLine(line)
            
            c.drawText(text_object)
            c.showPage()
            print(f"✅ Processed page {page_num + 1}/{len(doc)}")

        c.save()
        print(f"\n✨ SUCCESS! Digital PDF saved at: {OUTPUT_PDF}")

    except Exception as e:
        print(f"\n❌ ERROR: {str(e)}")

if __name__ == "__main__":
    convert_no_poppler()