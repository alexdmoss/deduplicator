import logging
from pathlib import Path


def print_results(results: dict):
    for x in results:
        if (len(results[x]) > 1):
            for result in results[x]:
                if len(result) == 3:
                    logging.info(f"Found potential duplicate image: {result[0]}, size: {result[1]}, dimensions: {result[2]}")
                else:
                    logging.info(f"Found duplicate file: {result}")


def save_results(results: dict, filename: str):
    logging.info(f"Saving output to {filename}")
    output = Path(filename)
    with output.open(mode="w+") as out:
        for x in results:
            if (len(results[x]) > 1):
                for result in results[x]:
                    if len(result) == 3:
                        out.write(f"{result[0]}, {result[1]}, {result[2]}\n")
                    else:
                        out.write(result + "\n")
                # newline to distinguish next group of files
                out.write("\n")
