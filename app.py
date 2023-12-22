from flask import Flask, send_from_directory, request, redirect
from box_module import eosBox
from cutsheet_module import Stamp

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


@app.route('/api/folder-info', methods=["POST"])
def check_folder_contents():
    folder = request.args.get('folderId')
    files = box.get_files_in_folder(folder)
    return files, HTTP_STATUS_SUCCESS


@app.route('/api/stamp', methods=['POST'])
def post_stamp():
    data = request.get_json()
    stamp = Stamp(data)
    pdfs = box.get_pdfs_in_folder(stamp.folder_id)
    print(f'pdfs: {pdfs}')
    for pdf in pdfs:
        stamp.apply_stamp_to_img(pdf['image'], pdf['name'], 0, 1)
    return 'Success!', HTTP_STATUS_SUCCESS


if __name__ == "__main__":
    HTTP_STATUS_SUCCESS = 200
    app.run(port=8000, debug=False)
