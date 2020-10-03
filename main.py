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

import sys
from deduplicator.start import start


if __name__ == "__main__":  # pragma: nocover
    sys.exit(start())
