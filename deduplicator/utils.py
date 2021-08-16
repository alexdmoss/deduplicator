from time import time
import hashlib
import random
import logging

log = logging.getLogger(__name__)


def hash_file(path, blocksize=2**20):
    m = hashlib.md5()
    try:
        with open(path, "rb") as f:
            while True:
                buf = f.read(blocksize)
                if not buf:
                    break
                m.update(buf)
        log.debug(f"Hashed {path}")
        return m.hexdigest()
    except FileNotFoundError:
        log.error("File not found: " + path)
        return time() + random.randint(1, 1000)
    except OSError:  # pragma: no cover (@TODO: mocking doesn't seem to work)
        log.error("File could not be opened: " + path)
        return time() + random.randint(1, 1000)
