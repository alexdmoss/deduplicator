import logging
from pathlib import Path

from deduplicator.results import print_results, save_results

logging.basicConfig(level=logging.INFO,
                    format='-> [%(levelname)s] [%(asctime)s] %(message)s',
                    datefmt='%Y-%m-%d %H:%M')

logger = logging.getLogger(__name__)


def test_print_results(caplog):
    caplog.set_level(logging.INFO)

    test_data = {}
    test_data['e8114e843bc16f5e895d6aa752bf3584'] = ['./test/barca_dupe_level_0.jpg',
                                                     './test/level_1/barca_dupe_level_1.jpg',
                                                     './test/level_1/level_2/barca_dupe_level_2.jpg']
    test_data['1d626efa9c786692344142cd7ef982c1'] = ['./test/lol_dupe_level_0.jpg',
                                                     './test/level_1/lol_dupe_level_1.jpg']
    test_data['3300d0cec39386604c5e387404660a05'] = ['./test/what_dupe_level_0.jpg',
                                                     './test/level_1/level_2/what_dupe_level_2.jpg']

    print_results(test_data)

    assert 'Found duplicate: ./test/barca_dupe_level_0.jpg' in caplog.text
    assert 'Found duplicate: ./test/barca_dupe_level_0.jpg' in caplog.text
    assert 'Found duplicate: ./test/level_1/barca_dupe_level_1.jpg' in caplog.text
    assert 'Found duplicate: ./test/level_1/level_2/barca_dupe_level_2.jpg' in caplog.text
    assert 'Found duplicate: ./test/lol_dupe_level_0.jpg' in caplog.text
    assert 'Found duplicate: ./test/level_1/lol_dupe_level_1.jpg' in caplog.text
    assert 'Found duplicate: ./test/what_dupe_level_0.jpg' in caplog.text
    assert 'Found duplicate: ./test/level_1/level_2/what_dupe_level_2.jpg' in caplog.text


def test_print_empty_results(caplog):
    caplog.set_level(logging.INFO)

    test_data = {}
    test_data['e8114e843bc16f5e895d6aa752bf3584'] = ['./test/barca_dupe_level_0.jpg']

    print_results(test_data)

    assert 'Found duplicate' not in caplog.text


def test_save_results(caplog, tmpdir):
    caplog.set_level(logging.INFO)

    test_output_file = Path(f'{tmpdir}/test.txt')

    test_data = {}
    test_data['e8114e843bc16f5e895d6aa752bf3584'] = ['./test/barca_dupe_level_0.jpg',
                                                     './test/level_1/barca_dupe_level_1.jpg',
                                                     './test/level_1/level_2/barca_dupe_level_2.jpg']
    test_data['1d626efa9c786692344142cd7ef982c1'] = ['./test/lol_dupe_level_0.jpg',
                                                     './test/level_1/lol_dupe_level_1.jpg']
    test_data['3300d0cec39386604c5e387404660a05'] = ['./test/what_dupe_level_0.jpg',
                                                     './test/level_1/level_2/what_dupe_level_2.jpg']

    save_results(test_data, test_output_file)

    with open(test_output_file) as f:
        num_lines = sum(1 for _ in f)

    assert num_lines == 10
    assert f'Saving output to {tmpdir}/test.txt' in caplog.text
    assert test_output_file.exists() is True


def test_save_empty_results(caplog, tmpdir):
    caplog.set_level(logging.INFO)

    test_output_file = Path(f'{tmpdir}/test.txt')

    test_data = {}
    test_data['e8114e843bc16f5e895d6aa752bf3584'] = ['./test/barca_dupe_level_0.jpg']

    save_results(test_data, test_output_file)

    with open(test_output_file) as f:
        num_lines = sum(1 for _ in f)

    assert num_lines == 0
