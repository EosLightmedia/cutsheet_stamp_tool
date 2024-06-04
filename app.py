#! /.venv/bin/python
from io import StringIO
from flask import Flask, make_response, send_from_directory, request, redirect, Response
from box_module import eosBox
from cutsheet import CutSheet
from datetime import datetime
import logging
from logging.handlers import MemoryHandler
import os
from dotenv import load_dotenv


class ByteIOHandler(logging.StreamHandler):
    def __init__(self):
        super().__init__(StringIO())

    def read(self):
        self.flush()
        self.stream.seek(0)
        return self.stream.getvalue().encode()


logging.basicConfig(
    level=logging.DEBUG,
    format="%(asctime)s [%(module)s:%(levelname)s] [%(funcName)s] %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
)
logging.getLogger("urllib3").setLevel(logging.INFO)
logging.getLogger("werkzeug").setLevel(logging.ERROR)
logger = logging.getLogger(__name__)
handler = ByteIOHandler()
logger.setLevel(logging.DEBUG)
log_memory = MemoryHandler(capacity=1024 * 16, target=handler)
logger.addHandler(log_memory)

# Load environment variables from .env file
load_dotenv()

HTTP_STATUS_SUCCESS = 200
logging.basicConfig(level=logging.WARNING)
app = Flask(__name__, static_folder='frontend', static_url_path='')


def get_callback_url():
    if __name__ == "__main__":
        callback_url = 'http://localhost:8000'

    else:
        callback_url = 'https://pdfstamper.eoslightmedia.com'

    return callback_url


def get_box():
    client_id = os.getenv("CLIENT_ID")
    client_secret = os.getenv("CLIENT_SECRET")
    return eosBox(client_id, client_secret, get_callback_url())


@app.route("/", methods=['GET', 'POST'])
def index():
    logger.info('Welcome')
    response = make_response(send_from_directory(app.static_folder, 'index.html'))
    box = get_box()
    code = request.args.get('code')
    logger.info(f'Session Code: {code}')

    if code:
        logger.info('Logging in with code...')

        try:
            access_token, refresh_token = box.login(code)
            logger.info('Login successful')
            logger.debug(f'Access token: {access_token}')
            logger.debug(f'Refresh token: {refresh_token}')

            logger.info('Setting cookies...')
            response.set_cookie('access', access_token)
            response.set_cookie('refresh', refresh_token)

            logger.info('Rendering AJAX web page')
            return response

        except Exception as e:
            logger.warning(f'Login error:\n{e}')

    logger.warning('Invalid Code')
    logger.info('Redirecting to authentication url:')
    return redirect(box.auth_url)


@app.route('/api/folder/', methods=["GET"])
def check_folder_contents():
    print(f'Request received: {request}')
    folder_id = request.args.get('folder_id')
    access_token = request.cookies.get('access')
    refresh_token = request.cookies.get('refresh')

    box = get_box()
    box.authenticate_client(access_token, refresh_token)

    files = box.get_files_in_folder(folder_id)

    return files, HTTP_STATUS_SUCCESS


@app.route('/api/stamp/', methods=['POST'])
def post_stamp():
    data: dict = request.get_json()

    logger.info(f'Stamping cut sheet with data:\n{request.data}')

    def get_pdf_name(pdf):
        pdf_name: list[str] = pdf['name'].split('.')[0].split('_')
        type_name = pdf_name[0].replace(' ', '')

        if len(pdf_name) > 1:
            description = pdf_name[1]
        else:
            description = ''

        part_number = pdf_name[-1].replace(' ', '')
        return [type_name, description, part_number]

    def get_folder_name(job_code, is_package, time):
        pdf_type = ['Stamped', 'Packaged'][int(is_package)]
        return f'{job_code.upper()} - {pdf_type} Cut Sheets - {time}'

    def process_single_pdf(pdf, folder_name, job_code):
        cut_sheet = CutSheet(data)
        pdf_page_count = len(pdf['images'])
        coversheet_offset = int(data['coverSheet'])
        page_number = coversheet_offset
        if data['coverSheet']:
            cut_sheet_item_document_details = get_pdf_name(pdf)
            cut_sheet.render_cover_sheet(cut_sheet_item_document_details)

        for j in range(len(pdf['images'])):
            page_number += 1
            image = pdf['images'][j]
            pdf_name = get_pdf_name(pdf)[0]
            cut_sheet.render_page(image, pdf_name, page_number, pdf_page_count)

        pdf_data = cut_sheet.save_pdf()
        type_label = get_pdf_name(pdf)[0]
        file_name = f"{type_label}.pdf"

        folder_id = box.save_file_to_box(pdf_data, folder_name, file_name, data['folderID'])
        return folder_id

    def process_pdf_package(pdfs, folder_name, job_code):
        cut_sheet = CutSheet(data)
        coversheet_offset = int(data['coverSheet'])
        page_number = coversheet_offset
        page_count = total_page_count + page_number
        if data['coverSheet']:
            cut_sheet.render_cover_sheet()

        for i in range(len(pdfs)):
            pdf = pdfs[i]
            pdf_name = get_pdf_name(pdf)[0]
            for j in range(len(pdf['images'])):
                page_number += 1
                image = pdf['images'][j]
                cut_sheet.render_page(image, pdf_name, page_number, page_count)

        pdf_data = cut_sheet.save_pdf()
        file_name = f"{job_code.upper()} - Cut Sheet Package.pdf"

        folder_id = box.save_file_to_box(pdf_data, folder_name, file_name, data['folderID'])
        return folder_id

    access_token = request.cookies.get('access')
    refresh_token = request.cookies.get('refresh')

    logging.debug(f'Submitted data: {data}')

    box = get_box()
    box.authenticate_client(access_token, refresh_token)

    is_package = data.get('packageSet')
    pdfs, total_page_count = box.get_pdfs_in_folder(data.get('folderID'))

    job_code = data.get('projectNumber')
    current_time = datetime.now().strftime('%y-%m-%d-%H-%M')
    folder_name = get_folder_name(job_code, is_package, current_time)

    saved_folder_id = None

    if is_package:
        saved_folder_id = process_pdf_package(pdfs, folder_name, job_code)
    else:
        for i in range(len(pdfs)):
            saved_folder_id = process_single_pdf(pdfs[i], folder_name, job_code)

    if data.get('note') == 'DEBUG':
        log_memory.flush()
        log_bytes = handler.read()
        box.save_file_to_box(log_bytes, folder_name, 'debug.txt', data['folderID'])

    return Response(saved_folder_id, status=HTTP_STATUS_SUCCESS)


logger.info(f"Callback URL: {get_callback_url()}")

if __name__ == "__main__":
    app.run(port=8000, debug=True)
