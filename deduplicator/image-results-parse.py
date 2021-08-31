#!/usr/bin/env python
#
# For manipulating the output of the image scan - as re-running it is expensive

import sys
import ast
from typing import List
import click
from pathlib import Path


THRESHOLD = 70   # filters out results with confidence matching or higher than this
EQUAL_TO = False # if set, ONLY lines matching THRESHOLD are saved

@click.command()
@click.option("--input", help="Input File of image results", type=str, required=True)
@click.option("--output", help="Output File to save to", type=str, required=True)
@click.option("--threshold", help="Confidence Threshold to match against", type=int, required=False)
@click.option("--exact_match", help="If set to True, only returns results that have the exact threshold of confidence", type=bool, required=False)
def main(input, output, threshold, exact_match):
    if threshold == "":
        threshold = THRESHOLD
    if exact_match:
        exact_match = True
    results = files_with_resolution_above_threshold(input, threshold, exact_match)
    save_duplicate_results(output, results)


def files_with_resolution_above_threshold(input: str, threshold: int, exact_match: bool):
    matches = []
    input_file = Path(input)
    with input_file.open("r") as f:
        results = f.readlines()

    for result in results:
        result = ast.literal_eval(result)
        confidence = int(result['confidence'].replace('%', ''))
        if exact_match:
            if confidence == threshold:
                if _is_second_image_bigger(result['origin_result']['resolution'], result['target_result']['resolution']):
                    # we use | as separator here as lazy way to deal with probable things like comma in filename
                    entry = f"{result['target_file']}|({result['target_result']['resolution']})|"
                    entry += f"{result['origin_file']}|({result['origin_result']['resolution']})"
                else:
                    entry = f"{result['origin_file']}|({result['origin_result']['resolution']})|"
                    entry += f"{result['target_file']}|({result['target_result']['resolution']})"
                matches.append(entry)
        else:
            if confidence >= threshold:
                if _is_second_image_bigger(result['origin_result']['resolution'], result['target_result']['resolution']):
                    # we use | as separator here as lazy way to deal with probable things like comma in filename
                    entry = f"{result['target_file']}|({result['target_result']['resolution']})|"
                    entry += f"{result['origin_file']}|({result['origin_result']['resolution']})"
                else:
                    entry = f"{result['origin_file']}|({result['origin_result']['resolution']})|"
                    entry += f"{result['target_file']}|({result['target_result']['resolution']})"
                matches.append(entry)

    return matches


def save_duplicate_results(filename: str, results: dict):
    output = Path(filename)
    with output.open(mode="w+") as out:
        for result in results:
            out.write(f"{result}\n")


def _is_second_image_bigger(file1, file2):
    first = int(file1.split()[0])
    second = int(file2.split()[0])
    if second > first:
        return True


if __name__ == "__main__":  # pragma: nocover
    sys.exit(main())
