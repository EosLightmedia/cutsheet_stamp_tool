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
        self.pdf_canvas.drawImage(logo_img, self.page_width - 100, 10, 80, 80)

    def apply_stamp_to_img(self, page_image_bytes, pdf_name: str, page_num: int, page_total: int):
        # Place image
        scale = 0.85
        pdf_image = ImageReader(page_image_bytes)
        self.pdf_canvas.drawImage(pdf_image, self.page_width * 0.075, self.page_height * 0.15, self.page_width * scale,
                                  self.page_height * scale)

        # Draw footer
        self._draw_box((0, 0), (self.page_width, self.page_height * 0.15), 'black')

        # if self.gradient == 0:
        self._draw_box((5, 30), (self.page_width - 10, (self.page_height * 0.15) - 35), 'white')
        # else:
        #     image_path = [
        #         'frontend-dist/static/media/purple-gradient.d4158913ea60c14f19aa.png',
        #         'frontend-dist/static/media/orange-gradient.1174bcef997a2d5e694d.png'
        #     ][self.gradient - 1]
        #     self.pdf_canvas.drawImage(image_path, 5, 30, self.page_width - 10, (self.page_height * 0.15) - 35)
        #
        # logo_path = [
        #     'frontend-dist/static/media/eos-logo.41995ff3f203db68e72f.png',
        #     'frontend-dist/static/media/abernathy-logo.c0d4809a4631d4f433e5.png'
        #     ][self.prepared_by]

        # self.pdf_canvas.drawImage(logo_path, self.page_width - 100, 100, 80, 80)

        # Details
        self.pdf_canvas.setFont('Karla-Medium', 12)
        self.pdf_canvas.setFillColor('grey')

        self.pdf_canvas.drawString(10, 105, 'TYPE')
        self.pdf_canvas.drawString(200, 100, 'PROJECT NAME')
        self.pdf_canvas.drawString(200, 80, 'JOB CODE')
        self.pdf_canvas.drawString(200, 60, 'PREPARED FOR')
        self.pdf_canvas.drawString(200, 40, 'PROJECT PHASE')

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
        type_label = pdf_name.split('_')[0]
        type_size = interp(len(type_label), [4, 8], [60, 20])

        self.pdf_canvas.setFont('Karla-Medium', int(type_size))
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
        if self.is_page_number:
            self.pdf_canvas.drawString(500, 15, f"PAGE {page_num:02} OF {page_total:02}")

        self.pdf_canvas.showPage()

    def save_pdf(self):
        self.pdf_canvas.save()
        pdf_bytes = self.buffer.getvalue()
        self.buffer.close()
        return pdf_bytes