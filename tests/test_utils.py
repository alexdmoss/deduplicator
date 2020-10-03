from deduplicator.utils import hash_file


def test_hash_file(mocker, caplog):
    test_input_file = "./mocks/barca_dupe_level_0.jpg"

    digest = hash_file(test_input_file)
    assert digest == "e8114e843bc16f5e895d6aa752bf3584"


def test_hash_file_missing(mocker, caplog):
    test_missing_file = "./mocks/not-there.jpg"
    hash_file(test_missing_file)
    assert 'File not found' in caplog.text
