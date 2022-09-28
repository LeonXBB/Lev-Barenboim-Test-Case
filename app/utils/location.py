
import os

from .hash import get_hash

def get_file_location(file_id: int, new_file: bool=False) -> str:

    hashed_file_id = get_hash(str(file_id))

    if new_file: sha256_broken = os.path.isfile(f"storage/{hashed_file_id}")
    else: sha256_broken = False

    #dirname = os.path.abspath(os.path.join(os.path.dirname(os.path.realpath(__file__)))) # copied from https://github.com/encode/starlette/issues/646

    return f"storage/{hashed_file_id}" if not sha256_broken else "storage/IT_HAPPENED!"