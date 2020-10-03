#!/usr/bin/env python
#
# main.py --dir=DIR
#        [--output=OUTPUT]
#        [--delete]         # removes last found duplicate only - order of folders matters
#        [--debug]
#        [--quiet]

import sys
from deduplicator.start import start


if __name__ == "__main__":  # pragma: nocover
    sys.exit(start())
