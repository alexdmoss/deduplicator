import os
import concurrent.futures
from dataclasses import dataclass
from time import time
import hashlib
import random

from deduplicator.logger import log


@dataclass
class FileResult:
    file: str
    hash: str


def list_all_files(folder: str) -> dict:
    all_files = []
    for dir_name, subdirs, list_of_files in os.walk(folder, True, False, True):
        log.info("Scanning %s" % dir_name)
        for filename in list_of_files:
            path = os.path.join(dir_name, filename)
            all_files.append(path)
    return all_files


def hash_files_parallel(files, num_processes=None):
    with concurrent.futures.ProcessPoolExecutor(max_workers=os.cpu_count() if num_processes is None else num_processes) as executor:
        for result in executor.map(hash_file, files):
            if result is not None:
                yield result


def hash_files(list_of_files):
    hashed_files = {}
    log.info("Hashing list of files")

    for result in hash_files_parallel(list_of_files):
        if result is not None:

            if result.hash not in hashed_files:
                hashed_files[result.hash] = [result.file]
            else:
                hashed_files[result.hash].append(result.file)

    return hashed_files
    # for file in list_of_files:
    #     file_hash = hash_file(file)
    #     log.debug(f"Hash of file {file} was {file_hash}")
    #     if file_hash in hashed_files:
    #         hashed_files[file_hash].append(file)
    #     else:
    #         hashed_files[file_hash] = [file]
    # return hashed_files


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


def hash_file(path, blocksize=2**22):
    m = hashlib.sha256()
    try:
        with open(path, "rb") as f:
            while True:
                buf = f.read(blocksize)
                if not buf:
                    break
                m.update(buf)
        log.debug(f"Hashed {path}")
        return FileResult(file=path, hash=m.hexdigest())
    except FileNotFoundError:
        log.error("File not found: " + path)
        return FileResult(file=path, hash= time() + random.randint(1, 1000000000))
    except OSError:  # pragma: no cover (@TODO: mocking doesn't seem to work)
        log.error("File could not be opened: " + path)
        return FileResult(file=path, hash= time() + random.randint(1, 1000000000))
