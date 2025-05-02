from boxsdk import OAuth2, Client
import logging
from io import BytesIO

PACKAGE_FOLDER = 'Stamp Exports'
STAMP_FOLDER = '03-Stamped Cut Sheets'

class EosBox:
    def __init__(self, client_id, client_secret, callback_url):
        self.oauth = OAuth2(
            client_id=client_id,
            client_secret=client_secret
        )
        self.auth_url, _ = self.oauth.get_authorization_url(callback_url)
        self.client_id = client_id
        self.client_secret = client_secret

    def request_tokens(self, authentication_code):
        access_token, refresh_token = self.oauth.authenticate(authentication_code)
        return access_token, refresh_token

    def log_into_session(self, access_token, refresh_token):
        return Client(OAuth2(
                client_id=self.client_id,
                client_secret=self.client_secret,
                access_token=access_token,
                refresh_token=refresh_token
        ))


def get_shared_folder_id(shared_folder: str, session: Client, password=None):
    return session.get_shared_item(shared_folder, password=password)

def get_files_in_folder(folder_id, session: Client):
    folder = session.folder(folder_id).get()

    full_folder_path = "/".join([entry['name'] for entry in folder.path_collection['entries'][1:]])
    full_folder_path = f"{full_folder_path}/{folder.name}"

    items = []
    for item in folder.get_items():
        item_type = item.type
        if item.name.endswith('.pdf'):
            item_type = 'pdf'

        item_dict = {
            'type': item_type,
            'name': item.name,
        }

        items.append(item_dict)

    folder_dict = {
        'path': full_folder_path,
        'items': items
    }

    return folder_dict


def get_pdfs_in_folder(folder_id, session: Client) -> dict[str, bytes]:
    folder = session.folder(folder_id).get()
    pdfs = {}

    for item in folder.get_items(sort='name'):
        if item.type == 'file' and item.name.lower().endswith('.pdf'):
            pdf_file = session.file(item.id).content()
            pdfs[item.name] = pdf_file        
    
    return pdfs


def save_file_to_box(file: bytes, folder_name: str, file_name: str, folder_id: str, session: Client):
    logging.info(f'Saving file: {file_name} to Box folder: {folder_name} in folder_id: {folder_id}')
    items = session.folder(folder_id).get_items()
    
    # Try to find the folder with matching name
    exported_pdfs_folder = None
    for item in items:
        if item.type == 'folder' and item.name == STAMP_FOLDER:
            exported_pdfs_folder = session.folder(item.object_id)
            logging.info(f'Found existing folder "{STAMP_FOLDER}"')
            break

    # If the folder was not found, create it
    if exported_pdfs_folder is None:
        logging.info(f'Creating folder "{STAMP_FOLDER}"')
        exported_pdfs_folder = session.folder(folder_id).create_subfolder(STAMP_FOLDER)

    # Create a sub-folder
    sub_folder = None
    items = session.folder(exported_pdfs_folder.object_id).get_items()
    for item in items:
        if item.type == 'folder' and item.name == folder_name:
            logging.info(f'Found existing sub-folder "{folder_name}"')
            sub_folder = session.folder(item.object_id)
            break

    if sub_folder is None:
        logging.info(f'Creating sub-folder "{folder_name}"')
        sub_folder = session.folder(exported_pdfs_folder.object_id).create_subfolder(folder_name)

    # Create a file-like object from the bytes
    file_object = BytesIO(file)

    # Upload file object to new folder
    logging.info(f'Uploading file "{file_name}" to Box...')
    sub_folder.upload_stream(file_object, file_name)
    return sub_folder.object_id
