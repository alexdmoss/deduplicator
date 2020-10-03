
import logging
import os

from deduplicator.utils import hash_file


logging.basicConfig(level=logging.INFO,
                    format='-> [%(levelname)s] [%(asctime)s] %(message)s',
                    datefmt='%Y-%m-%d %H:%M')

logger = logging.getLogger(__name__)


def build_hash_file_list(folder: str) -> dict:
    all_files = {}
    for dir_name, subdirs, list_of_files in os.walk(folder, True, False, True):
        logger.debug("Scanning %s" % dir_name)
        for filename in list_of_files:
            path = os.path.join(dir_name, filename)
            file_hash = hash_file(path)
            logger.debug(f"Hash of file {path} was {file_hash}")
            if file_hash in all_files:
                all_files[file_hash].append(path)
            else:
                all_files[file_hash] = [path]
    return all_files


def delete_duplicates(results: dict):
    for x in results:
        if (len(results[x]) > 1):
            logger.info("Deleting " + results[x][-1])
            # os.remove(results[x][-1])
    return results
