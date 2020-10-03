import logging
from deduplicator.files import list_all_files, hash_files, delete_duplicates


def test_list_all_files():
    test_data = "./mocks"
    all_files = list_all_files(test_data)
    assert './mocks/barca_dupe_level_0.jpg' in all_files
    assert './mocks/level_1/barca_dupe_level_1.jpg' in all_files
    assert './mocks/lol_dupe_level_0.jpg' in all_files
    assert './mocks/level_1/lol_dupe_level_1.jpg' in all_files
    assert './mocks/what_dupe_level_0.jpg' in all_files
    assert './mocks/level_1/level_2/what_dupe_level_2.jpg' in all_files
    assert './mocks/queen_no_dupe_level_0.jpg' in all_files
    assert './mocks/level_1/beans_no_dupe_level_1.jpeg' in all_files
    assert './mocks' not in all_files
    assert 'random-file' not in all_files
    assert len(all_files) == 15


def test_hash_files():
    test_data = ['./mocks/barca_dupe_level_0.jpg',
                 './mocks/level_1/barca_dupe_level_1.jpg',
                 './mocks/level_1/level_2/barca_dupe_level_2.jpg',
                 './mocks/lol_dupe_level_0.jpg',
                 './mocks/level_1/lol_dupe_level_1.jpg',
                 './mocks/what_dupe_level_0.jpg',
                 './mocks/level_1/level_2/what_dupe_level_2.jpg']
    hashed_files = hash_files(test_data)

    keys = hashed_files.keys()
    assert 'e8114e843bc16f5e895d6aa752bf3584' in keys
    assert '1d626efa9c786692344142cd7ef982c1' in keys
    assert '3300d0cec39386604c5e387404660a05' in keys


def test_delete_matched_duplicates(caplog):
    caplog.set_level(logging.INFO)
    test_data = {}
    test_data['e8114e843bc16f5e895d6aa752bf3584'] = ['./test/barca_dupe_level_0.jpg',
                                                     './test/level_1/barca_dupe_level_1.jpg',
                                                     './test/level_1/level_2/barca_dupe_level_2.jpg']
    test_data['1d626efa9c786692344142cd7ef982c1'] = ['./test/lol_dupe_level_0.jpg',
                                                     './test/level_1/lol_dupe_level_1.jpg']
    test_data['3300d0cec39386604c5e387404660a05'] = ['./test/what_dupe_level_0.jpg',
                                                     './test/level_1/level_2/what_dupe_level_2.jpg']

    files = delete_duplicates(test_data)

    assert './test/barca_dupe_level_0.jpg' not in caplog.text
    assert './test/lol_dupe_level_0.jpg' not in caplog.text
    assert './test/what_dupe_level_0.jpg' not in caplog.text
    assert './test/level_1/barca_dupe_level_1.jpg' not in caplog.text

    assert './test/level_1/lol_dupe_level_1.jpg' in caplog.text
    assert './test/level_1/level_2/what_dupe_level_2.jpg' in caplog.text

    assert len(files) == 3


def test_empty_results_to_delete(caplog):
    caplog.set_level(logging.INFO)
    test_data = {}
    test_data['e8114e843bc16f5e895d6aa752bf3584'] = ['./test/barca_dupe_level_0.jpg']

    files = delete_duplicates(test_data)

    assert 'Deleting' not in caplog.text
    assert len(files) == 1
