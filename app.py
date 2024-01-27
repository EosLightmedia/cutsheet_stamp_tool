#! /.venv/bin/python

from flask import Flask, make_response, send_from_directory, request, redirect, Response
from box_module import eosBox
from cutsheet_module import Stamp
from datetime import datetime
import logging
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

HTTP_STATUS_SUCCESS = 200
logging.basicConfig(level=logging.WARNING)
app = Flask(__name__, static_folder='frontend-dist', static_url_path='')


def get_box():
    client_id = 'ek7onbev0qocf7rtfuov0h8xo17picca'
    client_secret = 'IXlVDtc03kOdwskeVfXkbz2Urj6jLnR33'

    if __name__ == "__main__":
        callback_url = 'http://localhost:8000/'

    else:
        callback_url = 'https://pdfstamper.eoslightmedia.com'

    return eosBox(client_id, client_secret, callback_url)


@app.route("/", methods=['GET', 'POST'])
def index():
    print(f'Request received: {request}')
    response = make_response(send_from_directory(app.static_folder, 'index.html'))
    box = get_box()
    code = request.args.get('code')

    if code:
        print(f'Code: {code}')
        print('Logging in with code...')

        try:
            access_token, refresh_token = box.login(code)
            print(f'Login successful')
            print(f'Access token: {access_token}')
            print(f'Refresh token: {refresh_token}')

            print(f'Setting cookies...')
            response.set_cookie('access', access_token)
            response.set_cookie('refresh', refresh_token)

            print(f'Rendering...')
            return response

        except Exception as e:
            print(f'Login error:\n{e}')

    print('Invalid Code')
    print('Redirecting:')
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
    print(f'Request received: {request}')
    access_token = request.cookies.get('access')
    refresh_token = request.cookies.get('refresh')
    print(f'Access token: {access_token}')
    print(f'Refresh token: {refresh_token}')

    data = request.get_json()
    box = get_box()
    box.authenticate_client(access_token, refresh_token)

    print(f'Stamp data: {data}')

    is_package = data.get('packageSet')
    print(f'is_package: {is_package}')

    pdfs, total_page_count = box.get_pdfs_in_folder(data.get('folderID'))
    print(f'{len(pdfs)} PDFs, and {total_page_count} total pages')

    page_number = 0
    saved_folder_id = 0

    current_time = datetime.now().strftime('%y-%m-%d-%H-%M-%S')
    print(f'Saving time as: {current_time}')

    stamp = Stamp(data)

    for i in range(len(pdfs)):
        pdf = pdfs[i]
        pdf_page_count = len(pdf['images'])

        if is_package:
            page_count = total_page_count
        else:
            page_count = pdf_page_count

        for j in range(len(pdf['images'])):
            page_number += 1
            image = pdf['images'][j]
            stamp.apply_stamp_to_img(image, pdf['name'], page_number, page_count)

        if not is_package:
            page_number = 0
            pdf_data = stamp.save_pdf()
            type_label = pdf['name'].split('_')[0]
            folder_name = f"cut-sheet_{current_time}"
            file_name = f"{type_label}.pdf"
            saved_folder_id = box.save_file_to_box(pdf_data, folder_name, file_name, stamp.folder_id)
            stamp = Stamp(data)

    if is_package:
        pdf_data = stamp.save_pdf()
        file_name = f"cut-sheet_{current_time}.pdf"
        saved_folder_id = box.save_package_to_box(pdf_data, file_name, stamp.folder_id)

    return Response(saved_folder_id, status=HTTP_STATUS_SUCCESS)


if __name__ == "__main__":
    app.run(port=8000, debug=True)