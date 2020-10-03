from freezegun import freeze_time

from deduplicator.utils import get_timestamp, hash_file


@freeze_time("2020-10-02 13:37:42")
def test_get_timestamp():
    ts = get_timestamp()
    assert ts == "2020-10-02 13:37:42"


def test_hash_file(mocker, caplog):
    test_input_file = "./mocks/barca_dupe_level_0.jpg"

    digest = hash_file(test_input_file)
    assert digest == "e8114e843bc16f5e895d6aa752bf3584"


def test_hash_file_missing(mocker, caplog):
    test_missing_file = "./mocks/not-there.jpg"
    hash_file(test_missing_file)
    assert 'File not found' in caplog.text


def test_hash_file_cannot_open(mocker, caplog):
    test_readonly_file = "/etc/shadow"          # @TODO: figure out how to mock OSError as this is dumb
    open_file = mocker.patch('os.read')
    open_file.side_effect = OSError
    hash_file(test_readonly_file)
    assert 'File could not be opened' in caplog.text
