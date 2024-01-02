from boxsdk import OAuth2, Client
import logging
import fitz
from io import BytesIO
from PIL import Image

logging.basicConfig(level=logging.DEBUG, )



def _convert_pdf_to_png(pdf_file: object) -> list:
    doc = fitz.Document(stream=pdf_file, filetype='pdf')
    logging.debug(f'\tFound {len(doc)} pages')
    images = []

    for i in range(len(doc)):
        page = doc.load_page(i)
        render = page.get_pixmap()

        # convert fitz.Pixmap/render to a PIL.Image object
        pil_img = Image.frombytes("RGB", [render.width, render.height], render.samples)
        output = BytesIO()
        pil_img.save(output, 'png')
        images.append(output)

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
        items = []
        for item in folder.get_items():
            items.append(item)
        return items

    def get_pdfs_in_folder(self, folder_id):
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
