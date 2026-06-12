import os
import shutil
import zipfile

import requests

DATA_URL = "https://bit.ly/LuPNT_data"
DATA_FILENAME = "LuPNT_data.zip"
DATA_FOLDERNAME = "LuPNT_data"


def _data_root():
    """Directory the data bundle is downloaded into / looked for.

    Honours ``LUPNT_DATA_PATH`` so the bundle can be pinned to a stable,
    shared location instead of always landing in the current working directory.
    ``LUPNT_DATA_PATH`` points directly at the ``LuPNT_data`` folder (the dir that
    contains ``ephemeris/``); we download into its parent so the extracted
    ``LuPNT_data/`` lands exactly there. Falls back to the current directory when
    the variable is unset, preserving the previous default behaviour.
    """
    pinned = os.environ.get("LUPNT_DATA_PATH")
    if pinned:
        return os.path.dirname(os.path.abspath(pinned))
    return os.getcwd()


def _is_populated(path):
    """True if ``path`` already holds an extracted bundle (has ``ephemeris/``)."""
    return os.path.isdir(os.path.join(path, "ephemeris"))


_data_path = os.environ.get(
    "LUPNT_DATA_PATH", os.path.join(os.getcwd(), DATA_FOLDERNAME)
)

if not _is_populated(_data_path):
    root = _data_root()
    os.makedirs(root, exist_ok=True)
    zip_path = os.path.join(root, DATA_FILENAME)
    print("Downloading required data from", DATA_URL)
    response = requests.get(DATA_URL, stream=True)
    with open(zip_path, "wb") as f:
        shutil.copyfileobj(response.raw, f)
    with zipfile.ZipFile(zip_path, "r") as zip_ref:
        zip_ref.extractall(root)
    os.remove(zip_path)
    os.environ["LUPNT_DATA_PATH"] = os.path.join(root, DATA_FOLDERNAME)
    print("Downloaded data to", os.path.relpath(os.environ["LUPNT_DATA_PATH"]))
else:
    os.environ["LUPNT_DATA_PATH"] = _data_path
    print("Found required data at", os.path.relpath(_data_path))
