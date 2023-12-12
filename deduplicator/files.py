import os

from deduplicator.logger import log
from deduplicator.utils import hash_file


def list_all_files(folder: str) -> dict:
    all_files = []
    for dir_name, subdirs, list_of_files in os.walk(folder, True, False, True):
        log.info("Scanning %s" % dir_name)
        for filename in list_of_files:
            path = os.path.join(dir_name, filename)
            all_files.append(path)
    return all_files


def hash_files(list_of_files):
    hashed_files = {}
    log.info("Hashing list of files")
    for file in list_of_files:
        file_hash = hash_file(file)
        log.debug(f"Hash of file {file} was {file_hash}")
        if file_hash in hashed_files:
            hashed_files[file_hash].append(file)
        else:
            hashed_files[file_hash] = [file]
    return hashed_files


def delete_duplicates(results: dict):
    for result in results.values():
        result.remove(result[0])
        for file in result:
            log.info(f"Deleting {file}")
            os.remove(file)
    return results


def find_duplicate_hashes(all_files: dict) -> dict:
    duplicates = {}
    for md, files in all_files.items():
        if len(files) > 1:
            duplicates[md] = files
    return duplicates
