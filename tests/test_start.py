import logging
from click.testing import CliRunner
from deduplicator.start import start


def test_debug(mocker):
    logging.getLogger("").handlers = []

    mocker.patch('deduplicator.start.print_results')
    mocker.patch('deduplicator.start.save_results')
    mocker.patch('deduplicator.start.list_all_files')
    mocker.patch('deduplicator.start.hash_files')
    mocker.patch('deduplicator.start.delete_duplicates')
    mocker.patch('deduplicator.start.remove_files_with_no_duplicates')

    runner = CliRunner()
    result = runner.invoke(start, ['--dir=./mocks', '-v'])
    assert "Script started" in result.output
    assert "Debug logging is enabled" in result.output
    assert result.exception is None
    assert result.exit_code == 0


def test_quiet(mocker):
    logging.getLogger("").handlers = []

    mocker.patch('deduplicator.start.print_results')
    mocker.patch('deduplicator.start.save_results')
    mocker.patch('deduplicator.start.list_all_files')
    mocker.patch('deduplicator.start.hash_files')
    mocker.patch('deduplicator.start.delete_duplicates')
    mocker.patch('deduplicator.start.remove_files_with_no_duplicates')

    runner = CliRunner()
    result = runner.invoke(start, ['--dir=./mocks', '-q'])
    assert "Script started" not in result.output
    assert result.exception is None
    assert result.exit_code == 0


def test_image_mode(mocker):
    logging.getLogger("").handlers = []

    mocker.patch('deduplicator.start.print_results')
    mocker.patch('deduplicator.start.save_results')
    mocker.patch('deduplicator.start.list_all_files')
    mocker.patch('deduplicator.start.hash_files')
    mocker.patch('deduplicator.start.delete_duplicates')
    mocker.patch('deduplicator.start.remove_files_with_no_duplicates')
    mocker.patch('deduplicator.start.find_duplicate_images')

    runner = CliRunner()
    result = runner.invoke(start, ['--dir=./mocks/image_compare', '--images'])
    assert "Script started" in result.output
    assert "Visual image comparison is enabled" in result.output
    assert result.exception is None
    assert result.exit_code == 0


def test_delete_mode(mocker):
    logging.getLogger("").handlers = []

    mocker.patch('deduplicator.start.print_results')
    mocker.patch('deduplicator.start.save_results')
    mocker.patch('deduplicator.start.list_all_files')
    mocker.patch('deduplicator.start.hash_files')
    mocker.patch('deduplicator.start.remove_files_with_no_duplicates')

    mocker.patch("deduplicator.start.delete_duplicates", return_value=[])

    runner = CliRunner()
    result = runner.invoke(start, ['--dir=./mocks', '-D'])
    assert "DELETE mode is enabled - duplicates files will be removed" in result.output
    assert "Deleting" not in result.output      # testing mock ok!
    assert "All duplicate files deleted" in result.output
    assert result.exception is None
    assert result.exit_code == 0


def test_delete_files_remain(mocker):
    logging.getLogger("").handlers = []

    mocker.patch('deduplicator.start.print_results')
    mocker.patch('deduplicator.start.save_results')
    mocker.patch('deduplicator.start.list_all_files')
    mocker.patch('deduplicator.start.hash_files')
    mocker.patch('deduplicator.start.remove_files_with_no_duplicates')

    mocker.patch("deduplicator.start.delete_duplicates", return_value=['a', 'b'])
    runner = CliRunner()
    result = runner.invoke(start, ['--dir=./mocks', '-D'])
    assert "DELETE mode is enabled - duplicates files will be removed" in result.output
    assert "Deleting" not in result.output      # testing mock ok!
    assert "Some duplicate files remain: 2" in result.output
    assert result.exception is None
    assert result.exit_code == 0


def test_non_existent_path(mocker):
    logging.getLogger("").handlers = []

    mocker.patch('deduplicator.start.print_results')
    mocker.patch('deduplicator.start.save_results')
    mocker.patch('deduplicator.start.list_all_files')
    mocker.patch('deduplicator.start.hash_files')
    mocker.patch('deduplicator.start.delete_duplicates')
    mocker.patch('deduplicator.start.remove_files_with_no_duplicates')

    runner = CliRunner()
    result = runner.invoke(start, ['--dir=/wibble'])
    assert "/wibble is not a valid path, please verify" in result.output
    assert result.exception is not None
    assert result.exit_code == 1


def test_saving_output(mocker, tmpdir):
    logging.getLogger("").handlers = []

    mocker.patch('deduplicator.start.print_results')
    mocker.patch('deduplicator.start.list_all_files')
    mocker.patch('deduplicator.start.hash_files')
    mocker.patch('deduplicator.start.delete_duplicates')
    mocker.patch('deduplicator.start.remove_files_with_no_duplicates')

    runner = CliRunner()
    result = runner.invoke(start, ['--dir=./mocks', f'--output={tmpdir}/test.txt'])
    assert f"Saving output to {tmpdir}/test.txt" in result.output
    assert result.exception is None
    assert result.exit_code == 0
