from reportlab.lib.utils import ImageReader
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from io import BytesIO


class Stamp:
    DISCLAIMERS = [
        'For Coordination Only',
        'Issued for Tender',
        'Submitted for Review, Comment & Approval'
    ]
    def __init__(self, stamp_data: dict):
        self._register_fonts()
        self.stamp_data: dict = stamp_data
        self.memory_allocation: BytesIO = BytesIO()
        self.pdf_canvas = canvas.Canvas(self.memory_allocation)
        self.cursor: tuple[int, int] = (0, 0)

    @staticmethod
    def _register_fonts():
        pdfmetrics.registerFont(TTFont('Karla-Medium', 'stamp-assets/Karla-Medium.ttf'))
        pdfmetrics.registerFont(TTFont('Karla-Light', 'stamp-assets/Karla-Light.ttf'))

    def render_page(self, document_image: BytesIO, type_name: str, page_number: int, page_total: int):
        self.cursor = (A4[0] * 0.06, 0)

        if self.stamp_data['isHeader'] is True:
            self._draw_disclaimer()
            self._draw_document(document_image)
            self._draw_stamp(type_name, page_number, page_total)
        else:
            self._draw_disclaimer()
            self._draw_stamp(type_name, page_number, page_total)
            self._draw_document(document_image)

        self.pdf_canvas.showPage()

    def render_cover_sheet(self):

        self._put_image(ImageReader("stamp-assets/letterhead-bg.png"),(0, 0), A4)
        self.pdf_canvas.showPage()

    def save_pdf(self):
        self.pdf_canvas.save()
        pdf_memory = self.memory_allocation.getvalue()
        self.memory_allocation.close()
        return pdf_memory

    def _draw_stamp(self, type_name, page_number: int, page_total: int):
        at_cursor = self.cursor
        stamp_size = (A4[0] * 0.88, A4[1] * 0.12)
        self._put_rect(at_cursor, stamp_size)

        gradient_size = (stamp_size[0] - 4, stamp_size[1] - 15)
        at_gradient = (at_cursor[0] + 2, at_cursor[1] + 13)
        self._put_image(self._get_gradiant(), at_gradient, gradient_size)

        at_date = (at_cursor[0] + 7, at_cursor[1] + 4)
        self._put_text(self._get_date_text(), at_date, 'white', 8, False)

        at_text = (at_cursor[0] + 7, at_cursor[1] + 83)
        self._put_text('type', at_text, bold=False)

        at_text = (at_text[0], at_text[1] - 30)
        self._put_text(type_name, at_text, size=40)

        at_text = (at_text[0], at_text[1] - 15)
        self._put_text('Job Name', at_text, bold=False)

        at_text = (at_text[0] + 80, at_text[1])
        self._put_text(self.stamp_data['projectName'], at_text)

        at_text = (at_text[0] - 80, at_text[1] - 15)
        self._put_text('Prepared For', at_text, bold=False)

        at_text = (at_text[0] + 80, at_text[1])
        self._put_text(self.stamp_data['preparedFor'], at_text)

        at_text = (at_text[0] + 200, at_text[1] + 15)
        self._put_text('Job Code', at_text, bold=False)

        at_text = (at_text[0] + 50, at_text[1])
        self._put_text(self.stamp_data['projectNumber'], at_text)

        if self.stamp_data['note'] != '':
            at_text = (at_text[0] - 50, at_text[1] - 15)
            self._put_text('note', at_text, bold=False)

            at_text = (at_text[0] + 50, at_text[1])
            self._put_text(self.stamp_data['note'], at_text)

        if self.stamp_data['showPageNumbers']:
            at_page = (at_cursor[0] + 450, at_cursor[1] + 4)
            self._put_text(self._get_page_text(page_number, page_total), at_page, 'white', 8, False)

        self.cursor = (self.cursor[0], self.cursor[1] + stamp_size[1])

    def _draw_document(self, document_image):
        at_cursor = self.cursor
        document_size = (A4[0] * 0.88, A4[1] * 0.88)

        self._put_image(document_image, at_cursor, document_size)
        self.cursor = (self.cursor[0], self.cursor[1] + document_size[1])

    def _draw_disclaimer(self):
        at_cursor = self.cursor
        at_disclaimer = (at_cursor[0] + 7, at_cursor[1] + 2)
        self._put_text(self._get_disclaimer_text(), at_disclaimer, size=7)
        self.cursor = (self.cursor[0], self.cursor[1] + (A4[1] * 0.01))

    def _put_text(self, text: str, at: tuple[int, int], color: str = 'Black', size: int = 10, bold: bool = True):
        if bold:
            self.pdf_canvas.setFont('Karla-Medium', size)
        else:
            self.pdf_canvas.setFont('Karla-Light', size)
        self.pdf_canvas.setFillColor(color)
        self.pdf_canvas.drawString(at[0],at[1], text.upper())

    def _put_rect(self, at: tuple[int, int], size: tuple[int, int], color: str = 'Black'):
        self.pdf_canvas.setFillColor(color)
        self.pdf_canvas.rect(at[0], at[1], size[0], size[1], fill=True, stroke=0)

    def _put_image(self, image_obj, at: tuple[int, int], size: tuple[int, int]):
        self.pdf_canvas.drawImage(ImageReader(image_obj), at[0], at[1], size[0], size[1])

    def _get_gradiant(self):
        prep_by = ['eos', 'ald'][self.stamp_data['preparedBy']]
        gradient = ['white', 'gradient'][int(self.stamp_data['isGradient'])]
        file_path = f'stamp-assets/{prep_by}-{gradient}.png'
        return ImageReader(file_path)

    def _get_date_text(self):
        date_type = f"{['ISSUED', 'REVISION'][int(self.stamp_data['isRevision'])]}"
        if self.stamp_data['isRevision']:
            revision_number = f" | REV: {self.stamp_data['revisionNumber']}"
        else:
            revision_number = ''
        date_text = f"{date_type}: {self.stamp_data['date']}{revision_number}"
        return date_text

    def _get_page_text(self, page_number: int, page_total):
        page_number += self.stamp_data['pageStart'] - 1
        page_total += self.stamp_data['pageStart'] - 1
        return f"PAGE {page_number:02} OF {page_total:02}"

    def _get_disclaimer_text(self):
        active_disclaimers = []

        for i in range(len(self.stamp_data["disclaimer"])):
            if self.stamp_data["disclaimer"][i] is True:
                active_disclaimers.append(self.DISCLAIMERS[i].upper())

        disclaimer_text = ', '.join(active_disclaimers)
        return disclaimer_text

if __name__ == '__main__':
    _stamp_data = {
        "isGradient": 1,
        "folderID": 123,
        "projectName": "Project",
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
        "isHeader": False
    }

    stamp = Stamp(stamp_data=_stamp_data)
    image_file = open("stamp-assets/letterhead-bg.png", 'rb')
    image = BytesIO(image_file.read())
    image_file.close()

    stamp.render_cover_sheet()
    stamp.render_page(image, 'longexample', 69, 420)

    pdf_bytes = stamp.save_pdf()
    pdf_file = open("output.pdf", 'wb')
    pdf_file.write(pdf_bytes)
    pdf_file.close()