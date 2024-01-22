from reportlab.lib.utils import ImageReader
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from numpy import interp
from io import BytesIO


class Stamp:

    def __init__(self, stamp_data: dict):

        self.buffer = BytesIO()
        self.is_gradient: bool = stamp_data["isGradient"]
        self.folder_id = stamp_data["folderID"]
        self.project_name = stamp_data["projectName"]
        self.project_number = stamp_data["projectNumber"]
        self.prepared_by: int = stamp_data["preparedBy"]
        self.prepared_for = stamp_data["preparedFor"]
        self.is_revision: bool = stamp_data["isRevision"]
        self.show_page_number: bool = stamp_data["showPageNumbers"]
        self.revision_number: int = stamp_data["revisionNumber"]
        self.date = stamp_data["date"]
        self.note = stamp_data["note"]
        self.disclaimer: list[bool] = stamp_data["disclaimer"]

        self.page_width, self.page_height = A4
        self.pdf_canvas = canvas.Canvas(self.buffer)

        pdfmetrics.registerFont(TTFont('Karla-Medium', 'static/Karla-Medium.ttf'))

        self.pdf_canvas.setFont('Karla-Medium', 12)

    def _draw_box(self, origin: tuple, size: tuple, color):
        self.pdf_canvas.setFillColor(color)
        self.pdf_canvas.rect(origin[0], origin[1], size[0], size[1], fill=True)

    def _get_footer_bg(self):
        if self.prepared_by == 0:  # Eos
            if self.is_gradient:
                return ""   # Eos gradient
            else:
                return ""   # Eos flat
        if self.prepared_by == 1:  # Ald
            if self.is_gradient:
                return ""  # Ald gradient
            else:
                return ""  # Ald flat

    def apply_stamp_to_img(self, page_image_bytes, pdf_name: str, page_num: int, page_total: int):
        # Place Pdf Image
        scale = 0.85
        pdf_image = ImageReader(page_image_bytes)
        self.pdf_canvas.drawImage(pdf_image, self.page_width * 0.075, self.page_height * 0.15, self.page_width * scale,
                                  self.page_height * scale)

        # Draw footer
        self._draw_box((0, 0), (self.page_width, self.page_height * 0.15), 'black')

        gradient_path = self._get_footer_bg()
        self.pdf_canvas.drawImage(gradient_path, 5, 10, self.page_width - 10, self.page_height * 0.15)

        # Details
        self.pdf_canvas.setFont('Karla-Medium', 12)
        self.pdf_canvas.setFillColor('grey')

        self.pdf_canvas.drawString(10, 105, 'TYPE')
        self.pdf_canvas.drawString(200, 100, 'PROJECT NAME')
        self.pdf_canvas.drawString(200, 80, 'JOB CODE')
        self.pdf_canvas.drawString(200, 60, 'PREPARED FOR')
        if len(self.note) > 0:
            self.pdf_canvas.drawString(200, 40, 'NOTE')

        self.pdf_canvas.setFillColor('black')

        self.pdf_canvas.drawString(300, 100, str(self.project_name).upper())
        self.pdf_canvas.drawString(300, 80, str(self.project_number).upper())
        self.pdf_canvas.drawString(300, 60, str(self.prepared_for).upper())
        self.pdf_canvas.drawString(300, 40, str(self.note).upper())

        # Disclaimer
        disclaimers = [
            'Disclaimer 1',
            'Disclaimer 2',
            'Disclaimer 3'
        ]

        # Type
        if '_' in pdf_name:
            type_label = pdf_name.split('_')[0]
        else:
            type_label = pdf_name.split('.')[0]

        self.pdf_canvas.setFont('Karla-Medium', 60)
        self.pdf_canvas.drawString(10, 50, str(type_label).upper())

        self.pdf_canvas.setFillColor('white')
        self.pdf_canvas.setFont('Karla-Medium', 10)

        # Issue Date / Revision Date
        date_type = f"{['ISSUED', 'REVISION'][int(self.is_revision)]}"

        if self.is_revision:
            revision_number = f' | REV: {self.revision_number}'
        else:
            revision_number = ''

        date_text = f'{date_type}: {self.date}{revision_number}'

        self.pdf_canvas.drawString(15, 15, date_text)

        # Page Number
        if self.show_page_number:
            self.pdf_canvas.drawString(500, 15, f"PAGE {page_num:02} OF {page_total:02}")

        self.pdf_canvas.showPage()

    def save_pdf(self):
        self.pdf_canvas.save()
        pdf_bytes = self.buffer.getvalue()
        self.buffer.close()
        return pdf_bytes
