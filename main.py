#!/usr/bin/env python
#
# ----------------------------------------------------------------------------------------
#
# usage: find-duplicates.py [-h] [-d DIR] [-o OUTPUT] [-r] [-v] [-q]
#
#           (-h for full description of args)
#
# ----------------------------------------------------------------------------------------
#
# Reads from a single directory supplied through command line arguments - if you want to
# search across multiple directories you will need to either move or symlink to them.
#
# Option (--remove) to DELETE the last found duplicate (so order of folders matters).
#
# Option (--output) to write out duplicate files to a file to then do something else with.

from time import time, gmtime, strftime
import os
import hashlib
import argparse
import random
import sys
import logging

logging.basicConfig(level=logging.INFO,
                    format='-> [%(levelname)s] [%(asctime)s] %(message)s',
                    datefmt='%Y-%m-%d %H:%M')

logger = logging.getLogger(__name__)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("-d", "--dir", help="Starting directory for search", required=True)
    parser.add_argument("-o", "--output", help="Output file for duplicates found")
    parser.add_argument("-r", "--remove", help="Remove duplicates or not", action="store_true")
    parser.add_argument("-v", "--debug", help="Turn on debugging", action="store_true")
    parser.add_argument("-q", "--quiet", help="Quiet mode - only prints files to be deleted", action="store_true")

    if len(sys.argv) == 1:
        parser.print_help(sys.stderr)
        sys.exit(1)

    args = parser.parse_args()

    if args.quiet:
        logging.getLogger().setLevel(logging.ERROR)

    if args.debug:
        logging.getLogger().setLevel(logging.DEBUG)

    folder = args.dir
    is_deleting = args.remove

    logger.info("Script started at " + get_timestamp() + ". Starting directory: " + folder)

    if is_deleting:
        logger.info("Script will automatically **DELETE** the duplicates it finds")

    if not os.path.exists(folder):
        logger.fatal("%s is not a valid path, please verify" % folder)
        sys.exit(1)

    hash_of_all_files = build_hash_file_list(folder)

    duplicates = remove_files_with_no_duplicates(hash_of_all_files)

    print_results(duplicates)

    if args.output:
        save_results(duplicates, args.output)

    if is_deleting:
        delete_duplicates(duplicates)

    logger.info("Script completed at " + get_timestamp())


def build_hash_file_list(folder: str) -> dict:
    all_files = {}
    for dir_name, subdirs, list_of_files in os.walk(folder, True, False, True):
        logger.debug("Scanning %s" % dir_name)
        for filename in list_of_files:
            path = os.path.join(dir_name, filename)
            file_hash = hash_file(path)
            if file_hash in all_files:
                all_files[file_hash].append(path)
            else:
                all_files[file_hash] = [path]
    return all_files


def remove_files_with_no_duplicates(all_files: dict) -> dict:
    duplicates = {}
    for md, files in all_files.items():
        if len(files) > 1:
            duplicates[md] = files
    return duplicates


def print_results(results: dict):
    for x in results:
        if (len(results[x]) > 1):
            for result in results[x]:
                logger.info("Found duplicate: " + result)


def save_results(results: dict, output: str):
    logger.info("Saving output to " + output)
    with open(output, 'w+') as out:
        for x in results:
            if (len(results[x]) > 1):
                for result in results[x]:
                    out.write(result + "\n")
                # newline to distinguish next group of files
                out.write("\n")


def delete_duplicates(results: dict):
    for x in results:
        if (len(results[x]) > 1):
            logger.info("Deleting " + results[x][-1])
            # os.remove(results[x][-1])


def get_timestamp() -> str:
    return strftime("%Y-%m-%d %H:%M:%S", gmtime())


def hash_file(path, blocksize=65536):
    try:
        afile = open(path, 'rb')
        hasher = hashlib.md5()
        buf = afile.read(blocksize)
        while len(buf) > 0:
            hasher.update(buf)
            buf = afile.read(blocksize)
        afile.close()
        return hasher.hexdigest()
    except FileNotFoundError:
        logger.error("File not found: " + path)
        return time.time() + random.randint(1, 1000)
    except OSError:
        logger.error("File could not be opened: " + path)
        return time.time() + random.randint(1, 1000)


def init():
    if __name__ == "__main__":
        sys.exit(main())


init()
