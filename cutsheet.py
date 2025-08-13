import random
from reportlab.lib.utils import ImageReader
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import LETTER
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from io import BytesIO

DISCLAIMERS = [
    'For Coordination Only',
    'Issued for Tender',
    'Submitted for Review, Comment & Approval',
    'Refer to LX Equipment Schedule for Specifications'
]


def register_fonts():
    pdfmetrics.registerFont(TTFont('Karla-Medium', 'stamp-assets/Karla-Medium.ttf'))
    pdfmetrics.registerFont(TTFont('Karla-Light', 'stamp-assets/Karla-Light.ttf'))


class CutSheet:
    def __init__(self, stamp_data: dict):
        register_fonts()
        self.stamp_data: dict = stamp_data
        self.memory_allocation: BytesIO = BytesIO()
        self.pdf_canvas = canvas.Canvas(self.memory_allocation, pagesize=LETTER)
        self.cursor: tuple[int, int] = (0, 0)

    def _draw_cover_title(self):
        company_name, company = self._get_company()
        horizontal_offset = [0.23, 0.15][company]
        stamp_cursor = LETTER[0] * horizontal_offset, LETTER[1] * 0.92
        title_text = f"{company_name} Submittal Cover Sheet"

        self._draw_text(title_text, stamp_cursor, size=18, cap=False)

    def _draw_cover_status(self):
        stamp_cursor = LETTER[0] * 0.125, LETTER[1] * 0.8
        stamp_size = (LETTER[0] * 0.75, LETTER[1] * 0.1)
        self._draw_rectangle(stamp_cursor, stamp_size)

        stamp_cursor = stamp_cursor[0] + 2, stamp_cursor[1] + 2
        stamp_size = stamp_size[0] - 4, stamp_size[1] - 4 - 20
        self._draw_rectangle(stamp_cursor, stamp_size, color='white')

        company_name, company = self._get_company()
        stamp_cursor = stamp_cursor[0] + 100, stamp_cursor[1] + 67
        title_text = f"{company_name} Status"
        self._draw_text(title_text, stamp_cursor, cap=False, color='white', bold=False)

        box_cursor = stamp_cursor[0] - 65, stamp_cursor[1] - 26
        box_size = 30, 15

        x_cursor = box_cursor[0] + 8, box_cursor[1] + 2 + 18
        x_offset = int(self.stamp_data["coverStatus"]) * -18
        x_cursor = x_cursor[0], x_cursor[1] + x_offset

        stamp_cursor = stamp_cursor[0], stamp_cursor[1] - 22
        self._draw_text('For Information', stamp_cursor, cap=False, bold=False)
        stamp_cursor = stamp_cursor[0], stamp_cursor[1] - 18
        self._draw_text('For Approval', stamp_cursor, cap=False, bold=False)
        stamp_cursor = stamp_cursor[0], stamp_cursor[1] - 18
        self._draw_text('For Review & Comments', stamp_cursor, cap=False, bold=False)

        self._draw_rectangle(box_cursor, box_size, color='whitesmoke')
        box_cursor = box_cursor[0], box_cursor[1] - 18
        self._draw_rectangle(box_cursor, box_size, color='whitesmoke')
        box_cursor = box_cursor[0], box_cursor[1] - 18
        self._draw_rectangle(box_cursor, box_size, color='whitesmoke')

        self._draw_text('x', x_cursor, size=18)

    def _get_company(self):
        company: int = self.stamp_data["preparedBy"]
        company_name = ["Eos Lightmedia", "Abernathy Lighting Design"][company]
        return company_name, company

    def _draw_cover_items(self, item_details):
        stamp_cursor = LETTER[0] * 0.125, LETTER[1] * 0.65
        stamp_size = (LETTER[0] * 0.75, LETTER[1] * 0.13)
        self._draw_rectangle(stamp_cursor, stamp_size)

        stamp_cursor = stamp_cursor[0] + 2, stamp_cursor[1] + 2
        stamp_size = stamp_size[0] - 4, stamp_size[1] - 4 - 20
        self._draw_rectangle(stamp_cursor, stamp_size, color='white')

        stamp_cursor = stamp_cursor[0] + 35, stamp_cursor[1] + 93
        self._draw_text('Item', stamp_cursor, cap=False, bold=False, color='white')

        stamp_cursor = stamp_cursor[0] + 63, stamp_cursor[1]
        self._draw_text('Document Submitted', stamp_cursor, cap=False, bold=False, color='white')

        stamp_cursor = stamp_cursor[0] - 55, stamp_cursor[1] - 25
        self._draw_text('1', stamp_cursor, cap=False)

        stamp_cursor = stamp_cursor[0] + 55, stamp_cursor[1]
        item_details_text = ' - '.join(item_details)
        self._draw_text(item_details_text, stamp_cursor, cap=False)

    def _draw_cover_details(self):
        stamp_cursor = LETTER[0] * 0.125, LETTER[1] * 0.1
        stamp_size = (LETTER[0] * 0.75, LETTER[1] * 0.1)
        self._draw_rectangle(stamp_cursor, stamp_size)

        stamp_cursor = stamp_cursor[0] + 2, stamp_cursor[1] + 2
        stamp_size = stamp_size[0] - 4, stamp_size[1] - 4
        self._draw_rectangle(stamp_cursor, stamp_size, color='white')

        stamp_cursor = stamp_cursor[0] + 10, stamp_cursor[1] + 20
        self._draw_text('Reference #', stamp_cursor, cap=False)

        stamp_cursor = stamp_cursor[0] + 0, stamp_cursor[1] + 20
        self._draw_text('Date', stamp_cursor, cap=False)

        stamp_cursor = stamp_cursor[0] + 0, stamp_cursor[1] + 20
        self._draw_text('Issued By', stamp_cursor, cap=False)

        stamp_cursor = stamp_cursor[0] + 80, stamp_cursor[1]
        self._draw_text(self.stamp_data['coverIssueBy'], stamp_cursor, size=12, cap=False, bold=False)

        stamp_cursor = stamp_cursor[0], stamp_cursor[1] - 20
        self._draw_text(self.stamp_data['date'], stamp_cursor, size=12, bold=False)

        stamp_cursor = stamp_cursor[0], stamp_cursor[1] - 20
        self._draw_text(self.stamp_data['coverRefNum'], stamp_cursor, size=12, bold=False)

    def _draw_stamp(self, type_name: str, page_number: int, page_total: int):

        stamp_cursor = self.cursor
        stamp_size = (LETTER[0] * 0.88, LETTER[1] * 0.12)
        self._draw_rectangle(stamp_cursor, stamp_size)

        gradient_size = (stamp_size[0] - 4, stamp_size[1] - 15)
        gradient_cursor = (stamp_cursor[0] + 2, stamp_cursor[1] + 13)
        self._draw_image(self._get_stamp_image(), gradient_cursor, gradient_size)

        at_date = (stamp_cursor[0] + 7, stamp_cursor[1] + 4)
        self._draw_text(self._get_date_text(), at_date, 'white', 8, False)

        at_text = (stamp_cursor[0] + 7, stamp_cursor[1] + 83)
        self._draw_text('type', at_text, bold=False)

        at_text = (at_text[0], at_text[1] - 30)
        self._draw_text(type_name, at_text, size=40, cap=False)

        at_text = (at_text[0], at_text[1] - 15)
        self._draw_text('Job Name', at_text, bold=False)

        at_text = (at_text[0] + 80, at_text[1])
        self._draw_text(self.stamp_data['projectName'], at_text)

        if self.stamp_data['preparedFor'] != '':    # if there's an entry in preparedFor
            at_text = (at_text[0] - 80, at_text[1] - 15)
            self._draw_text('Prepared For', at_text, bold=False)

            at_text = (at_text[0] + 80, at_text[1])
            self._draw_text(self.stamp_data['preparedFor'], at_text)
        else:   # no entry
            # Mimic the cursor movements either-way
            at_text = (at_text[0] + 80, at_text[1])
            at_text = (at_text[0] - 80, at_text[1] - 15)


        at_text = (at_text[0] + 225, at_text[1] + 15)
        self._draw_text('Job Code', at_text, bold=False)

        at_text = (at_text[0] + 50, at_text[1])
        self._draw_text(self.stamp_data['projectNumber'], at_text)

        if self.stamp_data['note'] != '':
            at_text = (at_text[0] - 50, at_text[1] - 15)
            self._draw_text('note', at_text, bold=False)

            at_text = (at_text[0] + 50, at_text[1])
            self._draw_text(self.stamp_data['note'], at_text)

        if self.stamp_data['showPageNumbers']:
            at_page = (stamp_cursor[0] + 450, stamp_cursor[1] + 4)
            self._draw_text(self._get_page_number_text(page_number, page_total), at_page, 'white', 8, False)

        self.cursor = (self.cursor[0], self.cursor[1] + stamp_size[1])

    def _draw_document_image(self, document_image):
        at_cursor = self.cursor
        scale = 0.88
        document_size = (LETTER[0] * scale, LETTER[1] * scale)

        self._draw_image(document_image, at_cursor, document_size)
        self.cursor = (self.cursor[0], self.cursor[1] + document_size[1])

    def _draw_disclaimer(self):
        at_cursor = self.cursor
        at_disclaimer = (at_cursor[0] + 7, at_cursor[1] + 2)
        self._draw_text(self._get_disclaimer_text(), at_disclaimer, size=7)
        self.cursor = (self.cursor[0], self.cursor[1] + (LETTER[1] * 0.01))

    def _draw_text(self, text: str, location: tuple[int, int], color: str = 'Black', size: int = 10, bold: bool = True,
                   cap: bool = True):
        if bold:
            self.pdf_canvas.setFont('Karla-Medium', size)
        else:
            self.pdf_canvas.setFont('Karla-Light', size)
        if cap: text = text.upper()

        self.pdf_canvas.setFillColor(color)
        self.pdf_canvas.drawString(*location, text)

    def _draw_rectangle(self, location: tuple[int, int], size: tuple[int, int], color: str = 'Black'):
        self.pdf_canvas.setFillColor(color)
        self.pdf_canvas.rect(*location, *size, fill=True, stroke=0)

    def _draw_image(self, image_obj, location: tuple[int, int], size: tuple[int, int]):
        self.pdf_canvas.drawImage(ImageReader(image_obj), *location, *size)

    def _get_stamp_image(self):
        theme_choice_int = self.stamp_data['preparedBy']
        is_gradient_int = int(self.stamp_data['isGradient'])

        theme_choice = ['eos', 'ald', 'blank'][theme_choice_int]
        gradient_choice = ['white', 'gradient'][is_gradient_int]

        file_path = f'stamp-assets/{theme_choice}-{gradient_choice}.png'
        return ImageReader(file_path)

    def _get_coversheet_image(self):
        theme_choice_int = self.stamp_data['preparedBy']
        theme_choice = ['eos', 'ald'][theme_choice_int]
        file_path = f'stamp-assets/{theme_choice}-coversheet.png'

        return ImageReader(file_path)

    def _get_date_text(self) -> str:
        date_type = f"{['ISSUED', 'REVISION'][int(self.stamp_data['isRevision'])]}"
        if self.stamp_data['isRevision']:
            revision_number = f" | REV: {self.stamp_data['revisionNumber']}"
        else:
            revision_number = ''

        date_text = f"{date_type}: {self.stamp_data['date']}{revision_number}"

        return date_text

    def _get_page_number_text(self, page_number: int, page_total) -> str:
        page_number += self.stamp_data['pageStart'] - 1
        page_total += self.stamp_data['pageStart'] - 1
        return f"PAGE {page_number:02} OF {page_total:02}"

    def _get_disclaimer_text(self) -> str:
        active_disclaimers: list[str] = []

        for i in range(len(self.stamp_data["disclaimer"])):
            if self.stamp_data["disclaimer"][i] is True:
                active_disclaimers.append(DISCLAIMERS[i].upper())

        disclaimer_text = ', '.join(active_disclaimers)
        return disclaimer_text

    def end_page(self):
        self.pdf_canvas.showPage()

    def render_page(self, document_image: BytesIO, type_name: str, page_number: int, page_total: int):
        cursor_start = LETTER[0] * 0.06, 0
        self.cursor = cursor_start

        if self.stamp_data['isHeader']:
            self._draw_disclaimer()
            self._draw_document_image(document_image)
            self._draw_stamp(type_name, page_number, page_total)
        else:
            self._draw_disclaimer()
            self._draw_stamp(type_name, page_number, page_total)
            self._draw_document_image(document_image)

        self.end_page()

    def render_cover_sheet(self, item_details):
        self._draw_image(self._get_coversheet_image(), (0, 0), LETTER)
        self._draw_cover_details()
        self._draw_cover_items(item_details)
        self._draw_cover_status()
        self._draw_cover_title()

        self.end_page()

    def save_pdf(self) -> bytes:
        self.pdf_canvas.save()
        pdf_memory = self.memory_allocation.getvalue()
        self.memory_allocation.close()

        return pdf_memory


if __name__ == '__main__':
    _stamp_data = {
        "isGradient": 1,
        "folderID": 123,
        "projectName": "ProjectName",
        "projectNumber": "12345",
        "preparedBy": 0,
        "preparedFor": "Client",
        "isRevision": True,
        "showPageNumbers": True,
        "revisionNumber": 99,
        "date": "2049/01/01",
        "note": "he he",
        "disclaimer": [True, True, True],
        "pageStart": 1,
        "isHeader": False,
        "coverStatus": 0,
        "coverIssueBy": "Jaylin",
        "coverRefNum": "0092999",
        "coverSheet": True
    }

    cut_sheet = CutSheet(stamp_data=_stamp_data)
    with open("stamp-assets/eos-coversheet.png", 'rb') as image_file:
        image = BytesIO(image_file.read())

    if _stamp_data['coverSheet']: cut_sheet.render_cover_sheet(['LX02A', 'Sound Bar Cut Sheet', 'FN44HT7900D'])

    cut_sheet.render_page(image, 'long_example', 69, 420)

    pdf_bytes = cut_sheet.save_pdf()
    pdf_file = open("output_LETTER.pdf", 'wb')
    pdf_file.write(pdf_bytes)
    pdf_file.close()