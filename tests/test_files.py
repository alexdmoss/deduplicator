from deduplicator.files import find_duplicate_hashes, list_all_files, hash_files, delete_duplicates, hash_file


def test_hash_file():
    test_input_file = "./mocks/files/image-with-dupe-L0.jpg"
    digest = hash_file(test_input_file)
    assert digest.hash == "e8114e843bc16f5e895d6aa752bf3584"
    assert digest.file == "./mocks/files/image-with-dupe-L0.jpg"


def test_hash_file_missing(caplog):
    test_missing_file = "./mocks/not-there.jpg"
    hash_file(test_missing_file)
    assert 'File not found' in caplog.text


def test_list_all_files():
    test_data = "./mocks/files"
    all_files = list_all_files(test_data)
    assert './mocks/files/image-no-dupe-L0.jpg' in all_files
    assert './mocks/files/image-with-dupe-L0.jpg' in all_files
    assert './mocks/files/level1/image-with-dupe-L1.jpg' in all_files
    assert './mocks/files/level1/level2/image-with-dupe-L2.jpg' in all_files
    assert './mocks' not in all_files
    assert 'random-file' not in all_files
    assert len(all_files) == 4


def test_hash_files():
    test_data = ['./mocks/files/image-with-dupe-L0.jpg',
                 './mocks/files/level1/image-with-dupe-L1.jpg',
                 './mocks/files/level1/level2/image-with-dupe-L2.jpg']
    hashed_files = hash_files(test_data)

    keys = hashed_files.keys()
    assert 'd6301cd22dff266fede98ef879a68ab5' not in keys
    assert 'e8114e843bc16f5e895d6aa752bf3584' in keys


def test_delete_matched_duplicates(caplog, mocker):
    test_data = {}
    test_data['e8114e843bc16f5e895d6aa752bf3584'] = ['./test/image1.jpg',
                                                     './test/level_1/image1.jpg',
                                                     './test/level_1/level_2/image1.jpg']
    test_data['1d626efa9c786692344142cd7ef982c1'] = ['./test/lol_dupe_level_0.jpg',
                                                     './test/level_1/lol_dupe_level_1.jpg']
    test_data['3300d0cec39386604c5e387404660a05'] = ['./test/what_dupe_level_0.jpg',
                                                     './test/level_1/level_2/what_dupe_level_2.jpg']

    mocker.patch('deduplicator.files.os.remove')

    files = delete_duplicates(test_data)

    assert './test/barca_dupe_level_0.jpg' not in caplog.text
    assert './test/lol_dupe_level_0.jpg' not in caplog.text
    assert './test/what_dupe_level_0.jpg' not in caplog.text
    assert './test/level_1/barca_dupe_level_1.jpg' not in caplog.text

    assert './test/level_1/lol_dupe_level_1.jpg' in caplog.text
    assert './test/level_1/level_2/what_dupe_level_2.jpg' in caplog.text

    assert len(files) == 3


def test_empty_results_to_delete(caplog):
    test_data = {}
    test_data['e8114e843bc16f5e895d6aa752bf3584'] = ['./test/barca_dupe_level_0.jpg']

    files = delete_duplicates(test_data)

    assert 'Deleting' not in caplog.text
    assert len(files) == 1


def test_find_duplicate_hashes():
    expected_output = {}
    mock_hashed_files = {}

    mock_hashed_files["somehash"] = ['file1', 'file2']
    mock_hashed_files["anotherhash"] = ['file3']

    expected_output["somehash"] = ['file1', 'file2'] 

    duplicates = find_duplicate_hashes(mock_hashed_files)

    assert duplicates == expected_output
