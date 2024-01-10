from reportlab.lib.utils import ImageReader
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from datetime import datetime
from box_module import eosBox
from io import BytesIO


class Stamp:
    FORMATS = ["%Y/%m/%d", "%m/%d/%Y", "%d/%m/%Y"]

    def __init__(self, stamp_data: dict):

        print(f'stamp_data: {stamp_data}')

        self.buffer = BytesIO()
        self.folder_id = stamp_data["folderID"]
        self.project_name = stamp_data["projectName"]
        self.project_number = stamp_data["projectNumber"]
        self.prepared_by = stamp_data["preparedBy"]
        self.prepared_for = stamp_data["preparedFor"]
        self.is_revision = stamp_data["isRevision"]
        self.revision_number = stamp_data["revisionNumber"]
        self.date = stamp_data["date"]
        self.note = stamp_data["note"]

        self.page_width, self.page_height = A4
        self.pdf_canvas = canvas.Canvas(self.buffer)

        pdfmetrics.registerFont(TTFont('Karla-Medium', 'static/Karla-Medium.ttf'))
        self.pdf_canvas.setFont('Karla-Medium', 12)

    def _draw_box(self, origin: tuple, size: tuple, color):
        self.pdf_canvas.setFillColor(color)
        self.pdf_canvas.rect(origin[0], origin[1], size[0], size[1], fill=True)

    def _get_logo(self):
        if self.prepared_by == 0:
            return "eos-logo.png"
        elif self.prepared_by == 1:
            return "abn-logo.png"

    def _place_logo(self):
        logo = self._get_logo()
        logo_img = ImageReader(logo)
        self.pdf_canvas.drawImage(logo_img, self.page_width - 100, 10, 80, 80)

    def apply_stamp_to_img(self, page_image_bytes, pdf_name: str, page_num: int, page_total: int):
        # Place image
        scale = 0.85
        pdf_image = ImageReader(page_image_bytes)
        self.pdf_canvas.drawImage(pdf_image, self.page_width * 0.075, self.page_height * 0.15, self.page_width * scale, self.page_height * scale)

        # Draw footer
        self._draw_box((0, 0), (self.page_width, self.page_height * 0.15), 'black')
        self._draw_box((5, 30), (self.page_width - 10, (self.page_height * 0.15) - 35), 'white')

        self.pdf_canvas.setFillColor('grey')

        self.pdf_canvas.drawString(10, 105, 'TYPE')
        self.pdf_canvas.drawString(200, 100, 'PROJECT NAME')
        self.pdf_canvas.drawString(200, 80, 'JOB CODE')
        self.pdf_canvas.drawString(200, 60, 'PREPARED FOR')
        self.pdf_canvas.drawString(200, 40, 'PROJECT PHASE')

        self.pdf_canvas.setFillColor('black')

        self.pdf_canvas.drawString(250, 100, str(self.project_name).upper())
        self.pdf_canvas.drawString(250, 80, str(self.project_number).upper())
        self.pdf_canvas.drawString(250, 60, str(self.prepared_for).upper())
        self.pdf_canvas.drawString(250, 40, str(self.note).upper())

        # Type
        type_label = pdf_name.split('_')[0]
        self.pdf_canvas.setFont('Karla-Medium', 60)
        self.pdf_canvas.drawString(10, 50, str(type_label).upper())

        self.pdf_canvas.setFillColor('white')
        self.pdf_canvas.setFont('Karla-Medium', 10)

        self.pdf_canvas.drawString(
            15,
            15,
            f"{['ISSUED DATE: ', 'REVISED DATE: '][int(self.is_revision)]}{self.date}")

        self.pdf_canvas.drawString(500, 15, f"PAGE {page_num:02} OF {page_total:02}")

        self.pdf_canvas.showPage()

    def save_pdf(self):
        self.pdf_canvas.save()
        pdf_bytes = self.buffer.getvalue()
        self.buffer.close()
        return pdf_bytes

