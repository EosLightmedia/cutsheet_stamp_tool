from reportlab.lib.utils import ImageReader
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from datetime import datetime


class Stamp:
    FORMATS = ["%Y/%m/%d", "%m/%d/%Y", "%d/%m/%Y"]

    def __init__(self, packet, stamp_data: dict):
        self.box_url = stamp_data["URL"]
        self.project_name = stamp_data["projectName"]
        self.project_number = stamp_data["projectNumber"]
        self.prepared_by = stamp_data["preparedBy"]
        self.prepared_for = stamp_data["preparedFor"]
        self.client = stamp_data["client"]
        self.is_revision = stamp_data["isRevision"]
        self.revision_number = stamp_data["revisionNumber"]
        self.date_format = stamp_data["dateFormat"]
        self.job_phase = stamp_data["jobPhase"]
        self.issued_date = self._date_to_string(stamp_data["issuedDate"])

        self.page_width, self.page_height = A4
        self.pdf_canvas = canvas.Canvas(packet)
        pdfmetrics.registerFont(TTFont('Karla-Medium', 'static/karla-medium.ttf'))
        self.pdf_canvas.setFont('Karla-Medium', 12)

    def _date_to_string(self, date_dict: dict):
        year = int(date_dict['year'])
        month = int(date_dict['month'])
        day = int(date_dict['day'])
        date = datetime(year, month, day)
        return date.strftime(self.FORMATS[self.date_format])

    def _draw_box(self, origin: tuple, size: tuple, color):
        self.pdf_canvas.setFillColor(color)
        self.pdf_canvas.rect(origin[0], origin[1], size[0], size[1], fill=True)
    def _get_logo(self):
        if self.client == 0:
            return "eos-logo.png"
        elif self.client == 1:
            return "abn-logo.png"

    def _place_logo(self):
        logo = self._get_logo()
        logo_img = ImageReader(logo)
        self.pdf_canvas.drawImage(logo_img, self.page_width - 100, 10, 80, 80)

    def apply_stamp_to_img(self, device_img, device_type: str, page_num: int, page_total: int):
        self._draw_box((0, 0), (self.page_width, self.page_height * 0.15), 'black')
        self._draw_box((5, 30), (self.page_width - 10, (self.page_height * 0.15) - 35), 'white')

        self.pdf_canvas.setFillColor('grey')

        self.pdf_canvas.drawString(15, 110, 'TYPE')
        self.pdf_canvas.drawString(200, 100, 'PROJECT NAME')
        self.pdf_canvas.drawString(200, 80, 'JOB CODE')
        self.pdf_canvas.drawString(200, 60, 'PREPARED FOR')
        self.pdf_canvas.drawString(200, 40, 'PROJECT PHASE')

        self.pdf_canvas.setFillColor('black')

        self.pdf_canvas.drawString(300, 100, str(self.project_name).upper())
        self.pdf_canvas.drawString(300, 80, str(self.project_number).upper())
        self.pdf_canvas.drawString(300, 60, str(self.prepared_for).upper())
        self.pdf_canvas.drawString(300, 40, str(self.job_phase).upper())

        self.pdf_canvas.setFillColor('white')
        self.pdf_canvas.setFont('Karla-Medium', 10)

        self.pdf_canvas.drawString(
            15,
            15,
            f"{['ISSUED DATE: ', 'REVISED DATE: '][int(self.is_revision)]}{self.issued_date}")

        self.pdf_canvas.drawString(500, 15, f"PAGE {page_num:02} OF {page_total:02}")



if __name__ == '__main__':
    packet = "output.pdf"
    stamp_data = {
        "URL": "https://example.com/box",
        "projectName": "Project X",
        "projectNumber": "12345",
        "preparedBy": "John Doe",
        "preparedFor": "Jane Smith",
        "client": "ACME Corp",
        "isRevision": True,
        "revisionNumber": "2",
        "dateFormat": 0,
        "jobPhase": "Phase 1",
        "issuedDate": {"year": 2022, "month": 1, "day": 15},
    }

    stamp = Stamp(packet, stamp_data)
    img = "image.jpg"
    stamp.apply_stamp_to_img(img, 'EG01', 1, 2)
    stamp.pdf_canvas.save()
