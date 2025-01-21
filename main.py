#! /.venv/bin/python
import logging
import os
from datetime import datetime
from io import BytesIO

import dotenv
import fitz
import flask
from PIL import Image
from flask import Response

import eos_box
from eos_box import EosBox
from brand_stamp import BrandStamp
from cutsheet import CutSheet

logging.basicConfig(
        level=logging.CRITICAL,
        format="%(asctime)s [%(module)s:%(levelname)s] [%(funcName)s] %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S",
)

logging.getLogger("urllib3").setLevel(logging.WARNING)
logging.getLogger("werkzeug").setLevel(logging.WARNING)
logging.getLogger("eos_box").setLevel(logging.INFO)

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

dotenv.load_dotenv()

class CutSheetStamper:
    CALLBACK_URL = 'https://pdfstamper.eoslightmedia.com'
    def __init__(self):
        self.client_id, self.client_secret = os.getenv("CLIENT_ID"), os.getenv("CLIENT_SECRET"); assert self.client_id and self.client_secret, "Missing client_id or secret, check your environment variables"
        self.callback_url = self.CALLBACK_URL if __name__ != '__main__' else 'http://localhost:8000'
        self.eos_box = EosBox(self.client_id, self.client_secret, self.callback_url)

        self.webapp = flask.Flask(__name__, static_folder='frontend', static_url_path='')
        self.webapp.route('/')(self.login)
        self.webapp.route('/api/folder/', methods=["GET"])(self.query_folder_contents)
        self.webapp.route('/api/stamp/', methods=['POST'])(self.do_stamp)
        self.webapp.route('/api/brand/', methods=['POST'])(self.do_brand)

        logger.info(f'Cutsheet Stamper initialized with callback url: {self.callback_url}')

    def login(self) -> Response:
        session_code = flask.request.args.get('code')
        try:
            access_token, refresh_token = self.eos_box.request_tokens(session_code)
            logger.info('Login successful')
            logger.info('Setting cookies...')
            static_render = flask.make_response(flask.send_from_directory(self.webapp.static_folder, 'index.html'))
            static_render.set_cookie('access', access_token)
            static_render.set_cookie('refresh', refresh_token)
            return static_render

        except Exception as e:
            logger.warning(f'Login failed: {type(e).__name__}')
            logger.info(f'Redirecting to authentication url: {self.eos_box.auth_url}')
            return flask.redirect(self.eos_box.auth_url)

    def query_folder_contents(self) -> Response:
        logger.info('Querying folder contents...')
        try:
            folder_id = flask.request.args['folderID']
        except KeyError:
            folder_id = flask.request.args['folder_id']
            logger.warning('Please use folderID instead of folder_id')

        access_token, refresh_token = flask.request.cookies.get('access'), flask.request.cookies.get('refresh')
        session = self.eos_box.log_into_session(access_token, refresh_token)
        files: dict = eos_box.get_files_in_folder(folder_id, session)
        logger.info(f'Found {len(files)} files: {str(files.values())}')
        return flask.make_response(files)

    def do_brand(self) -> Response:
        data = flask.request.get_json()
        session = self.eos_box.log_into_session(flask.request.cookies.get('access'), flask.request.cookies.get('refresh'))

        pdfs = eos_box.get_pdfs_in_folder(data['folderID'], session)
        current_time = datetime.now().strftime('%y.%m.%d - %H:%M')

        for name, pdf in pdfs.items():
            logging.info(f"Brand stamping: {name}")
            brand_stamp = BrandStamp(pdf)
            branded_pdf = brand_stamp.lay_branding(data.get('preparedBy'))
            file_name = f"{name}"
            folder_name = f"{name} - Branded - {current_time}"

            folder_id = eos_box.save_file_to_box(branded_pdf, folder_name, file_name, data['folderID'], session)
            return flask.make_response(folder_id, 200)

    def do_stamp(self) -> Response:
        folder_id = None
        data = flask.request.get_json()

        session = self.eos_box.log_into_session(flask.request.cookies.get('access'), flask.request.cookies.get('refresh'))

        if data.get('isBrandStamp'):
            logger.warning('Use api/brand/ endpoint instead of api/stamp/ endpoint for brand stamping.')
            return self.do_brand()

        is_package = data.get('packageSet')
        job_code = data.get('projectNumber')
        pdf_type = 'Packaged' if is_package else 'Stamped'
        current_time = datetime.now().strftime('%y.%m.%d - %H:%M')
        folder_name = f'{job_code.upper()} - {pdf_type} Cut Sheets - {current_time}'

        logger.info('Loading pdfs from folder...')
        pdfs = eos_box.get_pdfs_in_folder(data.get('folderID'), session)
        logger.info('Flattening pdfs...')
        flattened_pdfs = {}
        page_count = 0
        for pdf_name, pdf in pdfs.items():
            images = convert_pdf_to_png(pdf)
            flattened_pdfs[pdf_name] = images
            logging.info(f'Flattened: {pdf_name}')
            page_count += len(images)

        if data.get('coverSheet') and is_package == True:
            logging.warning('Cannot select coversheet and package. Forcing package to false')
            is_package = False

        logger.info('Rendering stamps...')
        if is_package:
            logger.info(f'Saving cut sheet package to folder: {folder_name}...')
            cut_sheet = CutSheet(data)
            coversheet_offset = int(data['coverSheet'])
            page_number = coversheet_offset
            page_count += coversheet_offset

            if data['coverSheet']:
                raise SyntaxError('Cannot select coversheet and package')

            for name, images in flattened_pdfs.items():
                type_name, description, part_number = express_name_details(name)
                logger.info(f"Rendering cut sheet: {name}")
                for image in images:
                    page_number += 1
                    cut_sheet.render_page(image, type_name, page_number, page_count)

            pdf_data = cut_sheet.save_pdf()
            folder_id = eos_box.save_file_to_box(pdf_data, folder_name, f"{job_code.upper()} - Cut Sheet Package.pdf", data['folderID'], session)
            logger.info(f'Packaged cut sheet saved to folder: {folder_id}')

        else:   # Not package
            logger.info(f'Saving cut sheets to folder: {folder_name}...')
            for name, images in flattened_pdfs.items():
                logging.info(f"Processing cut sheet: {name}")
                cut_sheet = CutSheet(data)
                coversheet_offset = int(data['coverSheet'])
                page_number = coversheet_offset
                page_count = len(images) + coversheet_offset

                type_name, description, part_number = express_name_details(name)
                if data['coverSheet']:
                    cut_sheet.render_cover_sheet([type_name, description, part_number])

                logger.info(f"Rendering cut sheet: {name}")
                for image in images:
                    page_number += 1
                    cut_sheet.render_page(image, type_name, page_number, page_count)

                pdf_data = cut_sheet.save_pdf()

                logger.info(f"Saving {name}")
                folder_id = eos_box.save_file_to_box(pdf_data, folder_name, name + '.pdf', data['folderID'], session)

            logger.info(f'Cut sheets saved to folder: {folder_id}')

        return flask.make_response(folder_id, 200)

def convert_pdf_to_png(pdf_file: bytes) -> list:
    doc = fitz.Document(stream=pdf_file, filetype='pdf')
    images = []
    for i in range(len(doc)):
        page = doc.load_page(i)
        zoom_factor = 2.0
        mat = fitz.Matrix(zoom_factor, zoom_factor)
        render = page.get_pixmap(matrix=mat)

        pil_img = Image.frombytes("RGB", (render.width, render.height), render.samples)
        output = BytesIO()
        pil_img.save(output, 'png')
        images.append(output)
    return images

def express_name_details(elements: str):
    """
    :param elements: 
    :return: A tuple containing the type name, description (if present, otherwise
             an empty string), and the part number.
    :rtype: tuple[str, str, str]
    
    Example:
        'L01_LiteLab a01.pdf' -> ('L01', 'LiteLab a01', 'LiteLaba01')
        'L05_DLC LumiSheet.pdf' -> ('L05', 'DLC LumiSheet', 'DLCLumiSheet')
        'T01.pdf' -> ('T01', '', 'T01')
        'T02_LiteLabbus_13.pdf' -> ('T02', 'LiteLabbus', '13')
    """
    elements: list[str] = elements.split('.')[0].split('_')
    type_name = elements[0].replace(' ', '')

    if len(elements) > 1:
        description = elements[1]
    else:
        description = ''

    part_number = elements[-1].replace(' ', '')
    return type_name, description, part_number

class StampRequest:
    def __init__(self, data: dict):
        ...

cutsheet_stamper = CutSheetStamper()
        
if __name__ == "__main__":
    cutsheet_stamper.webapp.run(port=8000)


