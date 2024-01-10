from flask import Flask, make_response, send_from_directory, request, redirect, Response
from box_module import eosBox
from cutsheet_module import Stamp
from datetime import datetime
import logging

HTTP_STATUS_SUCCESS = 200
logging.basicConfig(level=logging.DEBUG)
app = Flask(__name__, static_folder='frontend-dist', static_url_path='')


def get_box():
    client_id = 'ek7onbev0qocf7rtfuov0h8xo17picca'
    client_secret = 'IXlVDtc03kOdwskeVfXkbz2Urj6jLnR3'

    if __name__ == "__main__":
        callback_url = 'http://localhost:8000/'

    else:
        callback_url = 'https://cutsheet-stamp-tool-at2sy.ondigitalocean.app'

    return eosBox(client_id, client_secret, callback_url)


@app.route("/", methods=['GET', 'POST'])
def index():
    print(f'Request received: {request}')
    code = request.args.get('code')

    if not code:
        print('No code provided')
        box = get_box()
        print('Redirecting')
        return redirect(box.auth_url)

    else:
        print(f'Code: {code}')

        try:
            print('Logging in with code...')
            box = get_box()
            access_token, refresh_token = box.login(code)
            print(f'Login successful')

        except Exception as e:
            print(f'Login error: {e}')
            box = get_box()
            print('Redirecting')
            return redirect(box.auth_url)

        response = make_response(send_from_directory(app.static_folder, 'index.html'))
        response.set_cookie('auth_code', access_token)

        return response


@app.route('/api/folder/', methods=["GET"])
def check_folder_contents():
    print(f'Request received: {request}')
    folder_id = request.args.get('folder_id')
    token = request.args.get('auth_code')
    print(token, folder_id)

    box = get_box()
    box.authenticate_client(token, '')

    files = box.get_files_in_folder(folder_id)

    return files, HTTP_STATUS_SUCCESS


@app.route('/api/stamp/', methods=['POST'])
def post_stamp():
    print(f'Request received: {request}')
    access = request.args.get('auth_code')
    print(f'Token: {access}')
    # refresh = request.args.get('refresh')
    box = get_box()
    box.authenticate_client(access, '')

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
        saved_folder_id = box.save_file_to_box(pdf_data, f"cutsheet_{current_time}.pdf", stamp.folder_id)

    except Exception as e:
        return Response(f"\nPython Error: {e}", status=HTTP_STATUS_SUCCESS)

    return Response(saved_folder_id, status=HTTP_STATUS_SUCCESS)


if __name__ == "__main__":
    app.run(port=8000, debug=True)
