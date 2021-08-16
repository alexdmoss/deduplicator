import logging
import magic
import concurrent.futures
import os
from PIL import Image, ExifTags
import imagehash
from fuzzywuzzy import fuzz
from dataclasses import dataclass


log = logging.getLogger(__name__)

FUZZINESS = 80

@dataclass
class ImageResult:
    file: str
    hash: str
    image_size: str
    file_size: str
    capture_time: str


def find_duplicate_images(path):
    hashed_files = {}
    matches = []
    
    files = get_image_files(path)

    for result in hash_files_parallel(files, num_processes=None):
        output_data = {
            "file": result.file,
            "size": result.file_size,
            "resolution": result.image_size,
            "taken": result.capture_time,
        }

        if result.hash not in hashed_files:
            hashed_files[result.hash] = output_data
        else:
            log.info(f"{output_data['file']} is a DUPLICATE of {hashed_files[result.hash]['file']}, and should be picked up by the hash-based matching")

    all_hashes = list(hashed_files.keys())

    for hash_to_test in all_hashes:
        for hash, data in hashed_files.items():
            file_to_test = hashed_files[hash_to_test]['file']
            this_file = data['file']
            if file_to_test != this_file:
                confidence = fuzz.ratio(hash_to_test, hash)
                if confidence > FUZZINESS:
                    data["confidence"] = confidence
                    matches.append([str(confidence)+'%', file_to_test, this_file])

    return matches


def hash_files_parallel(files, num_processes=None):
    with concurrent.futures.ProcessPoolExecutor(max_workers=num_processes) as executor:
        for result in executor.map(hash_file, files):
            if result is not None:
                yield result


def is_image(file_name):
    full_supported_formats = ['gif', 'jp2', 'jpeg', 'pcx', 'png', 'tiff', 'x-ms-bmp',
                              'x-portable-pixmap', 'x-xbitmap']
    try:
        mime = magic.from_file(file_name, mime=True)
        return mime.rsplit('/', 1)[1] in full_supported_formats
    except IndexError:
        return False


# TODO: could use existing list of files rather than re-walk
def get_image_files(path):
    path = os.path.abspath(path)
    for root, dirs, files in os.walk(path):
        for file in files:
            file = os.path.join(root, file)
            if is_image(file):
                yield file


def hash_file(file):
    try:
        hashes = []
        img = Image.open(file)

        file_size = get_file_size(file)
        image_size = get_image_size(img)
        capture_time = get_capture_time(img)

        # hash the image 4 times and rotate it by 90 degrees each time
        for angle in [0, 90, 180, 270]:
            if angle > 0:
                turned_img = img.rotate(angle, expand=True)
            else:
                turned_img = img
            hashes.append(str(imagehash.phash(turned_img)))

        hashes = ''.join(sorted(hashes))

        return ImageResult(file=file, hash=hashes, file_size=file_size, image_size=image_size, capture_time=capture_time)
    except OSError:
        log.warning(f"Unable to open {file}")
        return None


def get_file_size(file_name):
    try:
        return os.path.getsize(file_name)
    except FileNotFoundError:
        return 0


def get_image_size(img):
    return "{} x {}".format(*img.size)


def get_capture_time(img):
    try:
        exif = {
            ExifTags.TAGS[k]: v
            for k, v in img._getexif().items()
            if k in ExifTags.TAGS
        }
        return exif["DateTimeOriginal"]
    except Exception:
        return "Time unknown"
