import logging
from pathlib import Path

log = logging.getLogger(__name__)


def print_duplicate_results(results: dict):
    for x in results:
        log.info(f"Duplicate Files: {results[x]}")


def save_duplicate_results(filename: str, results: dict):
    log.info(f"Saving output to {filename}. This contains the Original PLUS its duplicates listed on each line")
    output = Path(filename)
    with output.open(mode="w+") as out:
        for x in results:
            out.write(f"{(', '.join(results[x]))}\n")


def print_image_results(identical_images: dict, similar_images: dict):
    log.info("Displaying image results")

    print(identical_images)

    for match in identical_images:
        entry = "Duplicate Images: "
        for result in identical_images[match]:
            entry += f"{result['file']};"
        log.info(entry)

    for match in similar_images:
        log.info(f"Similar Images: {match}")


def save_image_results(filename: str, identical_images: dict, similar_images: dict):

    log.info(f"Saving duplicate images output to {filename}")
    output = Path(filename)

    with output.open(mode="w") as out:
        for result in identical_images:
            entry = {
                "confidence": "100%",
                "origin_file": identical_images[result][0]['file'],
                "target_file": identical_images[result][1]['file'],
                "origin_result": identical_images[result][0],
                "target_result": identical_images[result][1],
            }
            out.write(str(entry) + "\n")

    log.info(f"Saving similar images output to {filename}")
    output = Path(filename)

    with output.open(mode="a") as out:
        for result in similar_images:
            out.write(str(result) + "\n")
