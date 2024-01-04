from flask import Flask, send_from_directory, request, redirect, Response
from box_module import eosBox
from cutsheet_module import Stamp
from datetime import datetime
import logging
logging.basicConfig(level=logging.DEBUG)

app = Flask(__name__, static_folder='frontend-dist', static_url_path='')
CLIENT_ID = 'ek7onbev0qocf7rtfuov0h8xo17picca'
CLIENT_SECRET = 'IXlVDtc03kOdwskeVfXkbz2Urj6jLnR3'
CALLBACK_URL = 'http://localhost:8000/'

box = eosBox(CLIENT_ID, CLIENT_SECRET, CALLBACK_URL)


@app.route("/", methods=['GET', 'POST'])
def index():
    code = request.args.get('code')
    if not code:
        return redirect(box.auth_url)

    try:
        box.authenticate_client(code)
    except Exception as e:
        print(e)
        # If authentication fails, redirect back to the Box authentication URL
        return redirect(box.auth_url)
    return send_from_directory(app.static_folder, 'index.html')


@app.route('/api/folder-info/<folderID>', methods=["GET"])
def check_folder_contents(folderID):
    files = box.get_files_in_folder(folderID)

    return files, HTTP_STATUS_SUCCESS


@app.route('/api/stamp', methods=['POST'])
def post_stamp():
    try:
        logging.info('Stamping...')
        data = request.get_json()
        logging.debug(f'json data: {data}')
        stamp = Stamp(data)
        pdfs, page_count = box.get_pdfs_in_folder(stamp.folder_id)
        logging.info(f'{len(pdfs)} PDFs, and {page_count} pages')
        page_number = 0

        for i in range(len(pdfs)):
            pdf = pdfs[i]
            for j in range(len(pdf['images'])):
                page_number += 1
                image = pdf['images'][j]
                logging.debug(f"Applying page {page_number}, with {pdf['name']}")
                stamp.apply_stamp_to_img(image, pdf['name'], page_number, page_count)

        current_time = datetime.now().strftime('%y-%m-%d-%H-%M-%S')
        pdf_data = stamp.save_pdf()
        box.save_file_to_box(pdf_data, f"cutsheet_{current_time}.pdf", stamp.folder_id)
    except Exception as e:
        return Response("Error", status=HTTP_STATUS_SUCCESS)

    return Response("Success", status=HTTP_STATUS_SUCCESS)



if __name__ == "__main__":
    HTTP_STATUS_SUCCESS = 200
    app.run(port=8000, debug=False)
