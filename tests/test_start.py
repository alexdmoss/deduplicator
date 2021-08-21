import logging
from click.testing import CliRunner
from deduplicator.start import start


def test_image_mode(mocker, caplog):
    caplog.set_level(logging.DEBUG)

    mocker.patch('deduplicator.start.find_and_hash_images')
    mocker.patch('deduplicator.start.find_identical_images')
    mocker.patch('deduplicator.start.find_similar_images')
    mocker.patch('deduplicator.start.print_image_results')

    runner = CliRunner()
    result = runner.invoke(start, ['--dir=./mocks/images', '--images'])

    assert "Script started" in caplog.text
    assert "Visual image comparison is enabled" in caplog.text
    assert result.exception is None
    assert result.exit_code == 0


def test_delete_mode(mocker, caplog):

    mocker.patch('deduplicator.start.list_all_files')
    mocker.patch('deduplicator.start.hash_files')
    mocker.patch('deduplicator.start.find_duplicate_hashes')
    mocker.patch('deduplicator.start.print_duplicate_results')
    mocker.patch("deduplicator.start.delete_duplicates", return_value=[])

    runner = CliRunner()
    result = runner.invoke(start, ['--dir=./mocks', '--delete'])
    assert "DELETE mode is enabled - duplicates files will be removed" in caplog.text
    assert "Deleting" not in caplog.text      # testing mock ok!
    assert result.exception is None
    assert result.exit_code == 0


def test_delete_files_remain(mocker, caplog):

    mocker.patch('deduplicator.start.list_all_files')
    mocker.patch('deduplicator.start.hash_files')
    mocker.patch('deduplicator.start.find_duplicate_hashes')
    mocker.patch('deduplicator.start.print_duplicate_results')
    mocker.patch("deduplicator.start.delete_duplicates", return_value=['a', 'b'])

    runner = CliRunner()
    result = runner.invoke(start, ['--dir=./mocks', '--delete'])
    assert "DELETE mode is enabled - duplicates files will be removed" in caplog.text
    assert "Deleting" not in caplog.text      # testing mock ok!
    assert result.exception is None
    assert result.exit_code == 0


def test_non_existent_path(mocker, caplog):

    mocker.patch('deduplicator.start.list_all_files')
    mocker.patch('deduplicator.start.hash_files')
    mocker.patch('deduplicator.start.find_duplicate_hashes')
    mocker.patch('deduplicator.start.print_duplicate_results')

    runner = CliRunner()
    result = runner.invoke(start, ['--dir=/wibble'])

    assert "/wibble is not a valid path, please verify" in caplog.text
    assert result.exception is not None
    assert result.exit_code == 1


def test_saving_output(mocker, tmpdir):

    mocker.patch('deduplicator.start.list_all_files')
    mocker.patch('deduplicator.start.hash_files')
    mocker.patch('deduplicator.start.find_duplicate_hashes')
    mocker.patch('deduplicator.start.print_duplicate_results')
    mocker.patch('deduplicator.start.save_duplicate_results')

    runner = CliRunner()
    result = runner.invoke(start, ['--dir=./mocks', f'--output={tmpdir}/test.txt'])

    assert result.exception is None
    assert result.exit_code == 0


def test_image_mode_with_save(mocker, tmpdir, caplog):
    caplog.set_level(logging.DEBUG)

    mocker.patch('deduplicator.start.find_and_hash_images')
    mocker.patch('deduplicator.start.find_identical_images')
    mocker.patch('deduplicator.start.find_similar_images')
    mocker.patch('deduplicator.start.print_image_results')
    mocker.patch('deduplicator.start.save_image_results')

    runner = CliRunner()
    result = runner.invoke(start, ['--dir=./mocks/images', '--images', f'--output={tmpdir}/test.txt'])

    assert "Script started" in caplog.text
    assert "Visual image comparison is enabled" in caplog.text
    assert result.exception is None
    assert result.exit_code == 0