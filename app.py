import time

from flask import Flask, send_from_directory, request, session, redirect, url_for
from box_module import eosBox
from cutsheet_module import Stamp

app = Flask(__name__, static_folder='frontend-dist', static_url_path='')

CLIENT_ID = 'ek7onbev0qocf7rtfuov0h8xo17picca'
CLIENT_SECRET = 'IXlVDtc03kOdwskeVfXkbz2Urj6jLnR3'

box = eosBox(CLIENT_ID, CLIENT_SECRET, 'http://localhost:8000/')
print(f'url: {box.auth_url}')


@app.route("/", methods=['GET', 'POST'])
def index():
    code = request.args.get('code')
    # If 'code' is None, redirect client to the Box authentication URL
    if code is None:
        return redirect(box.auth_url)
    # Once 'code' is provided, authenticate the client
    try:
        box.authenticate_client(code)
    except Exception as e:
        print(e)
        # If authentication fails, redirect back to the Box authentication URL
        return redirect(box.auth_url)
    return send_from_directory(app.static_folder, 'index.html')


@app.route('/api/folder_check', methods=["GET", "POST"])
def folder_check():
    folder = request.args.get('folderId')
    files = box.get_files_in_folder(folder)
    return files, 200


@app.route('/api/stamp', methods=['POST'])
def post_stamp():
    data = request.get_json()
    print(data)
    Stamp.apply_stamp_to_img(data)
    return 'Success!', 200


# This route is needed for the default path for all other routes not defined above
# @app.route('/<path:path>')
# def serve(path):
#     return send_from_directory(app.static_folder, 'index.html')


if __name__ == "__main__":
    app.run(port=8000, debug=False)
