import os
import re
from typing import Optional, Union
from werkzeug.datastructures import FileStorage

from flask_uploads import UploadSet, IMAGES

# "images" must be same as the center of UPLOADED_IMAGES_DEST in config
IMAGE_SET = UploadSet("images", IMAGES) # set name and allowed extensions

def save_image(image: FileStorage, folder: Optional[str]  = None, name: Optional[str] = None) -> str:
    """Takes FileStorage and saves it to a folder
    """
    return IMAGE_SET.save(image, folder, name)

def get_path(filename: str, folder: str) -> str:
    """Take image name and folder and return full path
    """
    return IMAGE_SET.path(filename, folder)

def find_image_any_format(filename: str, folder: str) -> Union[str, None]:
    """Takes a filename and returns an iamge on any of the accepted formats.
    """
    for _format in IMAGES:
        image = f"{filename}.{_format}"
        image_path = IMAGE_SET.path(filename=image, folder=folder)
        if os.path.isfile(image_path):
            return image_path

def _retrieve_filename(file: Union[str, FileStorage]) -> Union[str, None]:
    """Take FileStorage and return the file name
    Allows our function to call with both file names and FileStorages and always get back a file name.
    """
    if isinstance(file, FileStorage):
        return file.filename 
    
    return file

def is_filename_safe(file: Union[str, FileStorage]) -> bool:
    """Check our regex and return whether the string matches or not
    """
    filename = _retrieve_filename(file)
    if not filename:
        return False
    
    allowed_format = "|".join(IMAGES) # png|svg|jpg
    regex = f"^[a-zA-Z0-9][a-zA-Z0-9_()-\\.]*\\.({allowed_format})$"
    return re.match(regex, filename) is not None

def get_basename(file: Union[str, FileStorage]) -> str:
    """Return full name of image in the path
    get basename('some/folder/image.jpg') returns 'image.jpg'
    """
    filename = _retrieve_filename(file)
    return os.path.split(filename)[1] # type: ignore

def get_extension(file: Union[str, FileStorage]) -> str:
    """Return file extension
    """
    filename = _retrieve_filename(file)
    return os.path.splitext(filename)[1] # type: ignore
