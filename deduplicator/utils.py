from time import time, gmtime, strftime
import hashlib
import random

import logging

logging.basicConfig(level=logging.INFO,
                    format='-> [%(levelname)s] [%(asctime)s] %(message)s',
                    datefmt='%Y-%m-%d %H:%M')

logger = logging.getLogger(__name__)


def get_timestamp() -> str:
    return strftime("%Y-%m-%d %H:%M:%S", gmtime())


def hash_file(path, blocksize=2**20):
    m = hashlib.md5()
    try:
        with open(path, "rb") as f:
            while True:
                buf = f.read(blocksize)
                if not buf:
                    break
                m.update(buf)
        return m.hexdigest()
    except FileNotFoundError:
        logger.error("File not found: " + path)
        return time() + random.randint(1, 1000)
    except OSError:  # pragma: no cover (@TODO: mocking doesn't seem to work)
        logger.error("File could not be opened: " + path)
        return time() + random.randint(1, 1000)
