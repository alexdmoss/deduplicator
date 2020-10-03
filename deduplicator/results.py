import logging
from pathlib import Path

logging.basicConfig(level=logging.INFO,
                    format='-> [%(levelname)s] [%(asctime)s] %(message)s',
                    datefmt='%Y-%m-%d %H:%M')

logger = logging.getLogger(__name__)


def print_results(results: dict):
    for x in results:
        if (len(results[x]) > 1):
            for result in results[x]:
                logger.info(f"Found duplicate: {result}")


def save_results(results: dict, filename: str):
    logger.info(f"Saving output to {filename}")
    output = Path(filename)
    with output.open(mode="w+") as out:
        for x in results:
            if (len(results[x]) > 1):
                for result in results[x]:
                    out.write(result + "\n")
                # newline to distinguish next group of files
                out.write("\n")
