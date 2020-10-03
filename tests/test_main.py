import main


def test_main(mocker):
    mocker.patch('main.start')
    main.start()
