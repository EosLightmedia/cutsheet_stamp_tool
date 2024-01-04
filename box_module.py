from boxsdk import OAuth2, Client
import logging
import fitz
import datetime
from io import BytesIO
from PIL import Image

logging.basicConfig(level=logging.DEBUG, )


def _convert_pdf_to_png(pdf_file: object) -> list:
    doc = fitz.Document(stream=pdf_file, filetype='pdf')
    logging.debug(f'\tFound {len(doc)} pages')
    images = []

    for i in range(len(doc)):
        page = doc.load_page(i)
        # zoom factor is 2.0 here
        zoom_factor = 2.0
        # create a matrix for transformation
        mat = fitz.Matrix(zoom_factor, zoom_factor)
        # get pixmap with the transformation matrix
        render = page.get_pixmap(matrix=mat)

        # convert fitz.Pixmap/render to a PIL.Image object
        pil_img = Image.frombytes("RGB", (render.width, render.height), render.samples)
        output = BytesIO()
        pil_img.save(output, 'png')
        images.append(output)
        print(images)
    return images


class eosBox:
    def __init__(self, client_id, client_secret, callback_url):
        self.refresh_token = None
        self.access_token = None
        self.auth_url = None
        self.client = None

        self.authorized = OAuth2(
            client_id=client_id,
            client_secret=client_secret,
            store_tokens=self._store_tokens
        )

        self.auth_url, _ = self.authorized.get_authorization_url(callback_url)

    def _store_tokens(self, refresh_token, access_token):
        logging.debug('Storing tokens')
        self.refresh_token = refresh_token
        self.access_token = access_token

    def authenticate_client(self, auth_code):
        logging.info('Authenticating...', )
        access_token, refresh_token = self.authorized.authenticate(auth_code)
        self.access_token = access_token
        self.refresh_token = refresh_token
        self.client = Client(self.authorized)
        logging.info('...Authentication complete')

    def get_files_in_folder(self, folder_id):
        folder = self.client.folder(folder_id).get()

        # construct the folder's full path
        full_folder_path = "/".join([entry['name'] for entry in folder.path_collection['entries'][1:]])
        full_folder_path = f"{full_folder_path}/{folder.name}"

        items = []
        for item in folder.get_items():
            print(item)
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

    def get_pdfs_in_folder(self, folder_id):
        if self.client is None:
            logging.warning('Client not authenticated yet')
            return None
        folder = self.client.folder(folder_id).get()
        pdfs = []
        page_count = 0
        for item in folder.get_items():
            if item.type == 'file' and item.name.endswith('.pdf'):
                logging.debug(f'Processing {item.name}:')
                pdf_file = self.client.file(item.id).content()
                png_files = _convert_pdf_to_png(pdf_file)
                page_count += len(png_files)

                pdfs.append({
                    'name': item.name,
                    'images': png_files
                })

        return pdfs, page_count

    def save_file_to_box(self, file: bytes, file_name: str, folder_id: str):
        # Set folder name to be used
        folder_name = 'Stamp Exports'

        # Get the list of items (folders and files) in the parent folder
        items = self.client.folder(folder_id).get_items()

        # Try to find the folder with matching name
        exported_pdfs_folder = None
        for item in items:
            if item.type == 'folder' and item.name == folder_name:
                exported_pdfs_folder = self.client.folder(item.object_id)
                break

        # If the folder was not found, create it
        if exported_pdfs_folder is None:
            exported_pdfs_folder = self.client.folder(folder_id).create_subfolder(folder_name)

        # Create a file-like object from the bytes
        file_object = BytesIO(file)

        # Upload file object to new folder
        exported_pdfs_folder.upload_stream(file_object, file_name)
        return exported_pdfs_folder.object_id
