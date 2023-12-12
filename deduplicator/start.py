import click
import sys
from pathlib import Path

from deduplicator.logger import log
from deduplicator.results import print_duplicate_results, print_image_results, save_duplicate_results, save_image_results
from deduplicator.files import list_all_files, hash_files, delete_duplicates, find_duplicate_hashes
from deduplicator.images import find_and_hash_images, find_identical_images, find_similar_images



@click.command()
@click.option("--dir", "-d", help="Starting directory for search", type=str, required=True)
@click.option("--output", "-o", help="Output file for duplicates found", type=str)
@click.option("--images", "-i", flag_value="images", help="Compare images for visual similarities too", default=False)
@click.option("--delete", "-D", flag_value="delete", help="Remove duplicates or not")
def start(dir, output, images, delete):

    log.info("Script started. Starting directory: " + dir)

    if images:
        log.info("Visual image comparison is enabled")

    if delete:
        log.info("DELETE mode is enabled - duplicates files will be removed")

    if not Path(dir).exists():
        log.fatal(f"{dir} is not a valid path, please verify")
        sys.exit(1)

    if images:
        images = find_and_hash_images(dir)
        identical_images = find_identical_images(images)
        similar_images = find_similar_images(images)
        print_image_results(identical_images, similar_images)
        if output:
            save_image_results(output, identical_images, similar_images)

    else:
        all_files = list_all_files(dir)
        hash_of_all_files = hash_files(all_files)
        duplicates = find_duplicate_hashes(hash_of_all_files)
        print_duplicate_results(duplicates)
        if output:
            save_duplicate_results(output, duplicates)
        if delete:
            delete_duplicates(duplicates)

    log.info("Script completed")
