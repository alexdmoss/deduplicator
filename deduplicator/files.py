
import logging
import os

from deduplicator.utils import hash_file


logging.basicConfig(level=logging.INFO,
                    format='-> [%(levelname)s] [%(asctime)s] %(message)s',
                    datefmt='%Y-%m-%d %H:%M')

logger = logging.getLogger(__name__)


def list_all_files(folder: str) -> dict:
    all_files = []
    for dir_name, subdirs, list_of_files in os.walk(folder, True, False, True):
        logger.debug("Scanning %s" % dir_name)
        for filename in list_of_files:
            path = os.path.join(dir_name, filename)
            all_files.append(path)
    return all_files


def hash_files(list_of_files):
    hashed_files = {}
    logger.debug("Hashing list of files")
    for file in list_of_files:
        file_hash = hash_file(file)
        logger.debug(f"Hash of file {file} was {file_hash}")
        if file_hash in hashed_files:
            hashed_files[file_hash].append(file)
        else:
            hashed_files[file_hash] = [file]
    return hashed_files


def delete_duplicates(results: dict):
    for x in results:
        if (len(results[x]) > 1):
            logger.info("Deleting " + results[x][-1])
            # os.remove(results[x][-1])
    return results
