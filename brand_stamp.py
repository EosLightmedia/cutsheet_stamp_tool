import os
from io import BytesIO

from pdfrw import PageMerge, PdfReader, PdfWriter
from reportlab.lib.utils import ImageReader
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfgen import canvas

pdfmetrics.registerFont(TTFont("Karla-Medium", "stamp-assets/Karla-Medium.ttf"))

class BrandStamp:
    BRAND_STYLE = ['eos', 'ald', 'white']

    def __init__(self, white_pdf):
        self.white_pdf = white_pdf

    def lay_branding(self, prepared_by: int):
        chosen_style = self.BRAND_STYLE[prepared_by]
        watermark_top_path = os.path.join('stamp-assets', f'{chosen_style}-letterhead-top.png')
        watermark_bottom_path = os.path.join('stamp-assets', f'{chosen_style}-letterhead-bottom.png')
        img_top = ImageReader(watermark_top_path)
        img_bottom = ImageReader(watermark_bottom_path)
        width_top, height_top = img_top.getSize()
        width_bottom, height_bottom = img_bottom.getSize()
        pdf = PdfWriter()
        white_pdf_file = BytesIO(self.white_pdf)
        pdfreader_obj = PdfReader(white_pdf_file)
        total_pages = len(pdfreader_obj.pages)

        for page_number, page in enumerate(pdfreader_obj.pages, start=1):
            packet = BytesIO()
            media_box = page.Parent.MediaBox
            if media_box is None:
                media_box = page.MediaBox
                
            page_width, page_height = int(float(media_box[2])), int(float(media_box[3]))
            pdf_canvas = canvas.Canvas(packet, pagesize=(page_width, page_height))
            scale_x_top = page_width / width_top
            scale_y_top = height_top * scale_x_top
            scale_x_bottom = page_width / width_bottom
            scale_y_bottom = height_bottom * scale_x_bottom
            x_top = x_bottom = y_bottom = 0
            y_top = page_height - scale_y_top
            #pdf_canvas.drawImage(watermark_top_path, x_top, y_top, width=page_width, height=scale_y_top, mask='auto')
            pdf_canvas.drawImage(watermark_bottom_path, x_bottom, y_bottom, width=page_width, height=scale_y_bottom,
                                 mask='auto')
            # setColor to white and use the custom font
            pdf_canvas.setFillColorRGB(1, 1, 1)  # white color
            pdf_canvas.setFont("Karla-Medium", 10)  # use registered font

            page_number_str = f'{page_number}/{total_pages}'
            pdf_canvas.drawString(page_width - 50, 20, page_number_str)  # number position
            pdf_canvas.save()
            packet.seek(0)  # move to the beginning of the StringIO buffer
            stamp = PdfReader(packet)
            # add watermark to the page
            merger = PageMerge().add(page).add(stamp.pages[0])
            merger.render()
            pdf.addpage(merger.render())  # corrected line
        # Return BytesIO object
        branded_pdf = BytesIO()
        pdf.write(branded_pdf)
        branded_pdf.seek(0)
        return branded_pdf.getvalue()


if __name__ == '__main__':
    brand_stamp = BrandStamp('TEST PRINT.pdf')
    with open("branded.pdf", "wb") as out_file:
        out_file.write(brand_stamp.lay_branding(0).getvalue())