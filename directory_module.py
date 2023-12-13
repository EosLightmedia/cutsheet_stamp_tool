from typing import Optional

import gdocs_module
import box_module

BOX = 0
GOOGLE = 1


def list_items_in_folder(url: str) -> list:
    url_type = get_url_type(url)

    if url_type == BOX:
        return box_module.list_items(url)
    elif url_type == GOOGLE:
        return gdocs_module.list_items(url)
    else:
        return []



def get_url_type(url: str) -> int:
    global BOX, GOOGLE
    if 'box.com' in url:
        return BOX
    elif 'drive.google.com' in url:
        return GOOGLE
    else:
        return -1
