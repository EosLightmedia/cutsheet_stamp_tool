from boxsdk import OAuth2, Client
import logging
import fitz
logging.basicConfig(level=logging.DEBUG)



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
        self.refresh_token = refresh_token
        self.access_token = access_token

    def _convert_pdf_to_png(self, pdf_file):
        # Create a fitz document object
        doc = fitz.open(stream=pdf_file, filetype='pdf')
        images = []

        for i in range(len(doc)):
            # Render page to an image
            pix = doc[i].get_pixmap()

            # Save the image as a PNG
            output = BytesIO()
            pix.writePNG(output)
            images.append(output)

        return images

    def authenticate_client(self, auth_code):
        access_token, refresh_token = self.authorized.authenticate(auth_code)
        self.access_token = access_token
        self.refresh_token = refresh_token
        self.client = Client(self.authorized)

    def get_files_in_folder(self, folder_id):
        folder = self.client.folder(folder_id).get()
        items = []
        for item in folder.get_items():
            items.append(item)
        return items

    def get_pdfs_in_folder(self, folder_id):
        folder = self.client.folder(folder_id).get()
        pdfs = []
        for item in folder.get_items():
            if item.type == 'file' and item.name.endswith('.pdf'):
                pdf_file = self.client.file(item.id).content()
                png_files = self.convert_pdf_to_png(pdf_file)
                pdfs.append({
                    'name': item.name,
                    'data': pdf_file,
                    'images': png_files
                })
        return pdfs

