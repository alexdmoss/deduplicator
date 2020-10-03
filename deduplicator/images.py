import logging
# from cv2 import imread
import magic
import concurrent.futures
import os
from PIL import Image, ExifTags
import imagehash
from fuzzywuzzy import fuzz

logging.basicConfig(level=logging.INFO,
                    format='-> [%(levelname)s] [%(asctime)s] %(message)s',
                    datefmt='%Y-%m-%d %H:%M')

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)          # @TODO: sort this out properly


def find_duplicate_images(path):
    hashed_files = {}
    files = get_image_files(path)
    for result in hash_files_parallel(files, num_processes=None):
        # result[1] is the hash, result[0] is the file
        # result[2] is size, result[3] is dimensions, result[4] may be timestamp
        output_data = [result[0], result[1], result[2]]

        # first entry, initialise return dict
        if not hashed_files:
            hashed_files[result[1]] = [output_data]
        else:
            for key in hashed_files.keys():
                match = fuzz.ratio(result[1], key)
                if match > 90:      # label dupe if 90% confidence in similarity of image hashes
                    hashed_files[key].append(output_data)
                    logger.debug(f"Ratio was {match} for {result[0]}")
                    break

    return hashed_files


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

        logger.debug(f"Hashed {file}")
        return file, hashes, file_size, image_size, capture_time
    except OSError:
        logger.warning(f"Unable to open {file}")
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
