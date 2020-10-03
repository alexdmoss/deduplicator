import click
import logging
import sys
from pathlib import Path

from deduplicator.results import print_results, save_results
from deduplicator.files import list_all_files, hash_files, delete_duplicates
from deduplicator.parse import remove_files_with_no_duplicates
from deduplicator.images import find_duplicate_images


@click.command()
@click.option("--dir", "-d", help="Starting directory for search", type=str, required=True)
@click.option("--output", "-o", help="Output file for duplicates found", type=str)
@click.option("--images", "-i", flag_value="images", help="Compare images for visual similarities too", default=False)
@click.option("--delete", "-D", flag_value="delete", help="Remove duplicates or not")
@click.option("--debug", "-v", flag_value="debug", help="Turn on debugging", default=False)
@click.option("--quiet", "-q", flag_value="quiet", help="Quiet mode - only prints files to be deleted", default=False)
def start(dir, output, images, delete, debug, quiet):
    logging.basicConfig(stream=sys.stdout, level=logging.INFO,
                        format='-> [%(levelname)s] [%(asctime)s] %(message)s', datefmt='%Y-%m-%d %H:%M')
    logger = logging.getLogger(__name__)

    if quiet:
        logging.getLogger().setLevel(logging.ERROR)

    if debug:
        logging.getLogger().setLevel(logging.DEBUG)
        logger.debug("Debug logging is enabled")

    logger.info("Script started. Starting directory: " + dir)

    if images:
        logger.info("Visual image comparison is enabled")

    if delete:
        logger.info("DELETE mode is enabled - duplicates files will be removed")

    if not Path(dir).exists():
        logger.fatal(f"{dir} is not a valid path, please verify")
        sys.exit(1)

    if images:
        duplicates = find_duplicate_images(dir)
    else:
        all_files = list_all_files(dir)

        hash_of_all_files = hash_files(all_files)

        duplicates = remove_files_with_no_duplicates(hash_of_all_files)

    print_results(duplicates)

    if output:
        save_results(duplicates, output)

    if delete:
        files = delete_duplicates(duplicates)
        if len(files) == 0:
            logger.info("All duplicate files deleted")
        else:
            logger.warning(f"Some duplicate files remain: {len(files)}")

    logger.info("Script completed")
