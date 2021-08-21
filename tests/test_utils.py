from deduplicator.utils import hash_file


def test_hash_file():
    test_input_file = "./mocks/files/image-with-dupe-L0.jpg"
    digest = hash_file(test_input_file)
    assert digest == "e8114e843bc16f5e895d6aa752bf3584"


def test_hash_file_missing(caplog):
    test_missing_file = "./mocks/not-there.jpg"
    hash_file(test_missing_file)
    assert 'File not found' in caplog.text
