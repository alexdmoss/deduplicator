import logging
from pathlib import Path

log = logging.getLogger(__name__)


def print_duplicate_results(results: dict):
    for x in results:
        for result in results[x]:
            log.info(f"{result}")


def print_image_results(results: dict):
    for result in results:
        log.info(f"{result[1]} is a {result[0]} match for {result[2]}")


def save_duplicate_results(filename: str, results: dict):
    log.debug(f"Saving output to {filename}")
    output = Path(filename)
    with output.open(mode="w+") as out:
        for x in results:
            for result in results[x]:
                out.write(str(result) + "\n")
            out.write("\n")     # newline to distinguish next group of files


def save_image_results(filename: str, results: dict):
    log.debug(f"Saving output to {filename}")
    output = Path(filename)
    with output.open(mode="w+") as out:
        for result in results:
            out.write(str(result) + "\n")
