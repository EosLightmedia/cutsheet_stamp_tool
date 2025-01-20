#! /.venv/bin/python
import logging
import os
from datetime import datetime

import dotenv
import flask
from flask import Response

from box_module import EosBox
from brand_stamp import BrandStamp
from cutsheet import CutSheet

logging.basicConfig(
        level=logging.DEBUG,
        format="%(asctime)s [%(module)s:%(levelname)s] [%(funcName)s] %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S",
)

logging.getLogger("urllib3").setLevel(logging.WARNING)
logging.getLogger("werkzeug").setLevel(logging.WARNING)

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
            access_token, refresh_token = self.eos_box.login(session_code)
            logger.info('Login successful')
            logger.info('Setting cookies...')
            static_render = flask.make_response(flask.send_from_directory(self.webapp.static_folder, 'index.html'))
            static_render.set_cookie('access', access_token)
            static_render.set_cookie('refresh', refresh_token)
            return static_render

        except Exception as e:
            logger.warning(f'Login error:\n{e}')
            logger.info('Redirecting to authentication url:')
            return flask.redirect(self.eos_box.auth_url)

    def query_folder_contents(self) -> Response:
        try:
            folder_id = flask.request.args['folderID']
        except KeyError:
            folder_id = flask.request.args['folder_id']
            logger.warning('Please use folderID instead of folder_id')
            
        access_token, refresh_token = flask.request.cookies.get('access'), flask.request.cookies.get('refresh')
        self.eos_box.authenticate_client(access_token, refresh_token)
        files: dict = self.eos_box.get_files_in_folder(folder_id)
        return flask.make_response(files)

    def do_brand(self) -> Response:
        data = flask.request.get_json()
        self.eos_box.authenticate_client(flask.request.cookies.get('access'), flask.request.cookies.get('refresh'))
        
        pdfs = self.eos_box.get_pdfs_in_folder(data['folderID'])
        current_time = datetime.now().strftime('%y.%m.%d - %H:%M')
        
        for pdf in pdfs:
            logging.info(f"Brand stamping: {pdf.get('name')}")
            brand_stamp = BrandStamp(pdf.get('data'))
            branded_pdf = brand_stamp.lay_branding(data.get('preparedBy'))
            file_name = f"{pdf.get('name')}"
            folder_name = f"{pdf.get('name')} - Branded - {current_time}"

            folder_id = self.eos_box.save_file_to_box(branded_pdf, folder_name, file_name, data['folderID'])
            return flask.make_response(folder_id, 200)

    def do_stamp(self) -> Response:
        folder_id = None
        data = flask.request.get_json()        

        self.eos_box.authenticate_client(flask.request.cookies.get('access'), flask.request.cookies.get('refresh'))

        if data.get('isBrandStamp'):
            logging.warning('Use api/brand/ endpoint instead of api/stamp/ endpoint for brand stamping.')
            return self.do_brand()
        
        is_package = data.get('packageSet')
        job_code = data.get('projectNumber')
        pdf_type = 'Packaged' if is_package else 'Stamped'
        current_time = datetime.now().strftime('%y.%m.%d - %H:%M')
        folder_name = f'{job_code.upper()} - {pdf_type} Cut Sheets - {current_time}'
        
        logger.info('Flattening pdfs...')
        flattened_pdfs = self.eos_box.get_flattened_pdfs_in_folder(data.get('folderID'))

        if data.get('coverSheet'): 
            is_package = False

        if is_package:
            logging.info('Processing cut sheet package...')
            cut_sheet = CutSheet(data)
            coversheet_offset = int(data['coverSheet'])
            page_count = len(flattened_pdfs) + coversheet_offset
            page_number = coversheet_offset
            
            if data['coverSheet']:
                raise SyntaxError('Cannot select coversheet and package')
            
            for flattened_pdf in flattened_pdfs:
                type_name, description, part_number = express_name_details(flattened_pdf['name'])
                for image in flattened_pdf['images']:
                    page_number += 1
                    cut_sheet.render_page(image, type_name, page_number, page_count)
            
            pdf_data = cut_sheet.save_pdf()
            
            logging.info('Cut sheet package processed')
            logging.info(f'Saving cut sheet package to folder: {folder_name}...')
            folder_id = self.eos_box.save_file_to_box(pdf_data, folder_name, f"{job_code.upper()} - Cut Sheet Package.pdf", data['folderID'])
            logging.info(f'Packaged cut sheet saved to folder: {folder_id}')
        
        else:
            for flattened_pdf in flattened_pdfs:
                logging.info(f"Processing cut sheet: {flattened_pdf.get('name')}")
                cut_sheet = CutSheet(data)
                pdf_page_count = len(flattened_pdf['images'])
                coversheet_offset = int(data['coverSheet'])
                page_number = coversheet_offset
                
                if data['coverSheet']:
                    type_name, description, part_number = express_name_details(flattened_pdf['name'])
                    cut_sheet.render_cover_sheet([type_name, description, part_number])
                
                for image in flattened_pdf['images']:
                    page_number += 1
                    type_name, description, part_number = express_name_details(flattened_pdf['name'])
                    cut_sheet.render_page(image, type_name, page_number, pdf_page_count + coversheet_offset)
                
                pdf_data = cut_sheet.save_pdf()

                logging.info(f"Cut sheet processed")
                logging.info(f'Saving cut sheet to folder: {folder_name}...')
                folder_id = self.eos_box.save_file_to_box(pdf_data, folder_name, flattened_pdf.get('name') + '.pdf', data['folderID'])
                logging.info(f'Cut sheet saved to folder: {folder_id}')
                    
        return flask.make_response(folder_id, 200)

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

cutsheet_stamper = CutSheetStamper()
        
if __name__ == "__main__":
    cutsheet_stamper.webapp.run(port=8000, debug=True)