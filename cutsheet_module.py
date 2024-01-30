from reportlab.lib.utils import ImageReader
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from numpy import interp
from io import BytesIO


class Stamp:
    FORMATS = ["%Y/%m/%d", "%m/%d/%Y", "%d/%m/%Y"]

    def __init__(self, stamp_data: dict):

        self.buffer = BytesIO()
        self.is_gradient = stamp_data["isGradient"]
        self.folder_id = stamp_data["folderID"]
        self.project_name = stamp_data["projectName"]
        self.project_number = stamp_data["projectNumber"]
        self.prepared_by: int = stamp_data["preparedBy"]
        self.prepared_for: str = stamp_data["preparedFor"]
        self.is_revision = stamp_data["isRevision"]
        self.is_page_number = stamp_data["showPageNumbers"]
        self.revision_number = stamp_data["revisionNumber"]
        self.date = stamp_data["date"]
        self.note = stamp_data["note"]
        self.disclaimer = stamp_data["disclaimer"]

        self.page_width, self.page_height = A4
        self.pdf_canvas = canvas.Canvas(self.buffer)

        pdfmetrics.registerFont(TTFont('Karla-Medium', 'stamp-assets/Karla-Medium.ttf'))
        pdfmetrics.registerFont(TTFont('Karla-Light', 'stamp-assets/Karla-Light.ttf'))
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
        self.pdf_canvas.drawImage(logo_img, self.page_width - 100, 10, 80, 80)

    def apply_stamp_to_img(self, page_image_bytes, pdf_name: str, page_num: int, page_total: int):
        # Place image
        scale = 0.85
        pdf_image = ImageReader(page_image_bytes)
        self.pdf_canvas.drawImage(pdf_image, self.page_width * 0.075, self.page_height * 0.15, self.page_width * scale,
                                  self.page_height * scale)

        # Draw footer
        prep_by = ['eos', 'ald'][self.prepared_by]
        gradient = ['white', 'gradient'][int(self.is_gradient)]
        file_path = f'stamp-assets/{prep_by}-{gradient}.png'

        gradient_file = open(file_path, 'rb')
        gradient_bytes = BytesIO(gradient_file.read())
        gradient_image = ImageReader(gradient_bytes)
        gradient_file.close()

        self._draw_box((0, 13), (self.page_width, self.page_height * 0.14), 'black')
        self.pdf_canvas.drawImage(gradient_image, 5, 30, self.page_width - 10, self.page_height * 0.155 - 35)

        # Details
        self.pdf_canvas.setFont('Karla-Light', 10)
        self.pdf_canvas.setFillColor('black')

        self.pdf_canvas.drawString(15, 110, 'TYPE')
        self.pdf_canvas.drawString(15, 55, 'JOB NAME')
        self.pdf_canvas.drawString(235, 55, 'JOB CODE')
        self.pdf_canvas.drawString(15, 40, 'PREPARED FOR')
        if self.note != '':
            self.pdf_canvas.drawString(235, 40, 'NOTE')

        self.pdf_canvas.setFont('Karla-Medium', 10)

        self.pdf_canvas.drawString(90, 55, str(self.project_name).upper())
        self.pdf_canvas.drawString(290, 55, str(self.project_number).upper())
        self.pdf_canvas.drawString(90, 40, str(self.prepared_for).upper())
        self.pdf_canvas.drawString(290, 40, str(self.note).upper())



        # Type
        type_label = pdf_name.split('.')[0]
        type_label = type_label.split('_')[0]
        self.pdf_canvas.setFont('Karla-Medium', 45)

        self.pdf_canvas.drawString(13, 75, str(type_label).upper())

        # Issue Date / Revision Date
        date_type = f"{['ISSUED', 'REVISION'][int(self.is_revision)]}"

        if self.is_revision:
            revision_number = f' | REV: {self.revision_number}'
        else:
            revision_number = ''

        date_text = f'{date_type}: {self.date}{revision_number}'

        self.pdf_canvas.setFillColor('white')
        self.pdf_canvas.setFont('Karla-Medium', 8)

        self.pdf_canvas.drawString(15, 18, date_text)

        # Page Number
        if self.is_page_number:
            self.pdf_canvas.drawString(520, 18, f"PAGE {page_num:02} OF {page_total:02}")



        # Disclaimer
        disclaimers = [
            'For Coordination Only',
            'Issued for Tender',
            'Submitted for Review, Comment & Approval'
        ]

        active_disclaimers = []
        for i in range(len(self.disclaimer)):
            if self.disclaimer[i] is True:
                active_disclaimers.append(disclaimers[i].upper())
        disclaimer_text = ', '.join(active_disclaimers)

        self.pdf_canvas.setFont('Karla-Medium', 8)
        self.pdf_canvas.setFillColor('black')
        self.pdf_canvas.drawString(15, 4, disclaimer_text)

        self.pdf_canvas.showPage()

    def save_pdf(self):
        self.pdf_canvas.save()
        pdf_bytes = self.buffer.getvalue()
        self.buffer.close()
        return pdf_bytes

if __name__ == '__main__':
    stamp_data = {
        "isGradient": 0,
        "folderID": 123,
        "projectName": "Project",
        "projectNumber": "12345",
        "preparedBy": 0,
        "preparedFor": "Client",
        "isRevision": True,
        "showPageNumbers": False,
        "revisionNumber": 99,
        "date": "2049/01/01",
        "note": "",
        "disclaimer": [True, False, True]
    }

    stamp = Stamp(stamp_data)
    image_file = open("stamp-assets/eos-gradient.png", 'rb')
    image = BytesIO(image_file.read())
    image_file.close()

    stamp.apply_stamp_to_img(image, 'longexample_01.pdf', 69, 420)

    pdf_bytes = stamp.save_pdf()
    pdf_file = open("output.pdf", 'wb')
    pdf_file.write(pdf_bytes)
    pdf_file.close()
