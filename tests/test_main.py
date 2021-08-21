import deduplicator.main


def test_main(mocker):
    mocker.patch('deduplicator.main.start')
    deduplicator.main.start()
