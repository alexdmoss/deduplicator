#!/usr/bin/env python
#
# For manipulating the output of the image scan - as re-running it is expensive

import sys
import click
from pathlib import Path

@click.command()
@click.option("--input", help="Input File of Image Results", type=str, required=True)
def main(input):

    input_file = Path(input)
    with input_file.open("r") as results:
        data = results.readlines()

    print (data)

    # if confidence is 100%, extract origin and target file to compare
    # if confidence is 100%, extract origin and target file + their resolutions/size to compare
    
if __name__ == "__main__":  # pragma: nocover
    sys.exit(main())
