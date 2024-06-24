from PyPDF2 import PdfFileReader, PdfFileWriter
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4
from reportlab.lib.utils import ImageReader
from io import BytesIO


class BrandStamp:
    BRAND_STYLE = ['eos', 'ald', 'aux']

    def __init__(self, white_pdf: BytesIO):
        self.white_pdf: BytesIO = white_pdf

    def lay_image(self, canvas, image):
        canvas.drawImage(ImageReader(image), 0, 0, width=A4[0], height=A4[1])

    def lay_page_number(self, canvas, page_number):
        text_object = canvas.beginText()
        text_object.setTextOrigin(280, 40)  # Set xpos and ypos according to your requirement
        text_object.setFont("Helvetica", 40)
        text_object.textLine(text=f"{page_number + 1}")
        canvas.drawText(text_object)

    def lay_branding(self, prepared_by: int):
        chosen_style = self.BRAND_STYLE[prepared_by]
        pdf_reader = PdfFileReader(self.white_pdf)
        pdf_writer = PdfFileWriter()
        for page_number in range(pdf_reader.getNumPages()):
            pdf_page = pdf_reader.getPage(page_number)
            pdf_bytes = BytesIO()
            page_canvas = canvas.Canvas(pagesize=A4)
            self.lay_image(page_canvas, f'stamp-assets/{chosen_style}-coversheet.png')
            self.lay_page_number(page_canvas, page_number + 1)
            page_canvas.save()
            cm_page = PdfFileReader(pdf_bytes)
            watermark_page = cm_page.getPage(0)
            pdf_page.mergePage(watermark_page)
            pdf_writer.addPage(pdf_page)
        branded_pdf = BytesIO()
        pdf_writer.write(branded_pdf)
        branded_pdf.seek(0)
        return branded_pdf
