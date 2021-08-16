import click
import logging
import json
import sys
from pathlib import Path
from logging.config import dictConfig


from deduplicator.results import print_duplicate_results, print_image_results, save_duplicate_results, save_image_results
from deduplicator.files import list_all_files, hash_files, delete_duplicates, find_duplicate_hashes
from deduplicator.images import find_duplicate_images

with open('./logging.json') as file:
    config_dict = json.load(file)
    dictConfig(config_dict)


log = logging.getLogger(__name__)

@click.command()
@click.option("--dir", "-d", help="Starting directory for search", type=str, required=True)
@click.option("--output", "-o", help="Output file for duplicates found", type=str)
@click.option("--images", "-i", flag_value="images", help="Compare images for visual similarities too", default=False)
@click.option("--delete", "-D", flag_value="delete", help="Remove duplicates or not")
@click.option("--quiet", "-q", flag_value="quiet", help="Quiet mode - only prints files to be deleted", default=False)
def start(dir, output, images, delete, quiet):

    log.info("Script started. Starting directory: " + dir)

    if images:
        log.debug("Visual image comparison is enabled")

    if delete:
        log.info("DELETE mode is enabled - duplicates files will be removed")

    if not Path(dir).exists():
        log.fatal(f"{dir} is not a valid path, please verify")
        sys.exit(1)

    if images:
        duplicates = find_duplicate_images(dir)
        print_image_results(duplicates)
        if output:
            save_image_results(output, duplicates)

    else:
        all_files = list_all_files(dir)
        hash_of_all_files = hash_files(all_files)
        duplicates = find_duplicate_hashes(hash_of_all_files)
        print_duplicate_results(duplicates)
        if output:
            save_duplicate_results(output, duplicates)

    if delete:
        files = delete_duplicates(duplicates)
        if len(files) == 0:
            log.info("All duplicate files deleted")
        else:
            log.warning(f"Some duplicate files remain: {len(files)}")

    log.info("Script completed")
