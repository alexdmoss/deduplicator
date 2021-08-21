import logging
from pathlib import Path

from deduplicator.results import print_duplicate_results, save_duplicate_results, print_image_results

def test_print_results(caplog):

    test_data = {}
    test_data['e8114e843bc16f5e895d6aa752bf3584'] = ['./test/barca_dupe_level_0.jpg',
                                                     './test/level_1/barca_dupe_level_1.jpg',
                                                     './test/level_1/level_2/barca_dupe_level_2.jpg']
    test_data['1d626efa9c786692344142cd7ef982c1'] = ['./test/lol_dupe_level_0.jpg',
                                                     './test/level_1/lol_dupe_level_1.jpg']
    test_data['3300d0cec39386604c5e387404660a05'] = ['./test/what_dupe_level_0.jpg',
                                                     './test/level_1/level_2/what_dupe_level_2.jpg']
    print_duplicate_results(test_data)
    assert "Duplicate Files: ['./test/barca_dupe_level_0.jpg', './test/level_1/barca_dupe_level_1.jpg', './test/level_1/level_2/barca_dupe_level_2.jpg']" in caplog.text
    assert "Duplicate Files: ['./test/lol_dupe_level_0.jpg', './test/level_1/lol_dupe_level_1.jpg']" in caplog.text
    assert "Duplicate Files: ['./test/what_dupe_level_0.jpg', './test/level_1/level_2/what_dupe_level_2.jpg']" in caplog.text


def test_print_empty_results(caplog):

    test_data = {}
    test_data['e8114e843bc16f5e895d6aa752bf3584'] = ['./test/barca_dupe_level_0.jpg']

    print_duplicate_results(test_data)

    assert 'Found duplicate' not in caplog.text


def test_save_results(caplog, tmpdir):

    test_output_file = Path(f'{tmpdir}/test.txt')

    test_data = {}
    test_data['e8114e843bc16f5e895d6aa752bf3584'] = ['./test/barca_dupe_level_0.jpg',
                                                     './test/level_1/barca_dupe_level_1.jpg',
                                                     './test/level_1/level_2/barca_dupe_level_2.jpg']
    test_data['1d626efa9c786692344142cd7ef982c1'] = ['./test/lol_dupe_level_0.jpg',
                                                     './test/level_1/lol_dupe_level_1.jpg']
    test_data['3300d0cec39386604c5e387404660a05'] = ['./test/what_dupe_level_0.jpg',
                                                     './test/level_1/level_2/what_dupe_level_2.jpg']

    save_duplicate_results(test_output_file, test_data)

    with open(test_output_file) as f:
        num_lines = sum(1 for _ in f)

    assert num_lines == 3
    assert f'Saving output to {tmpdir}/test.txt' in caplog.text
    assert test_output_file.exists() is True


def test_save_empty_results(caplog, tmpdir):

    test_output_file = Path(f'{tmpdir}/test.txt')

    test_data = {}

    save_duplicate_results(test_output_file, test_data)

    with open(test_output_file) as f:
        num_lines = sum(1 for _ in f)

    assert num_lines == 0


def test_print_image_result(caplog):

    mocked_identical_images = {}
    mocked_similar_images = {}
    similar_result_1 = {}
    similar_result_2 = {}

    mocked_identical_images = {
        'some_hash_1': [
            {'file': '/some/original/image1.jpg', 'size': 2389171, 'resolution': '3264 x 2448', 'taken': '2015:09:27 13:59:55'},
            {'file': '/some/other/image1.jpg', 'size': 23148, 'resolution': '360 x 270', 'taken': 'Time unknown'}
        ],
        'some_hash_2': [
            {'file': '/some/original/image2.jpg', 'size': 1081866, 'resolution': '4032 x 3024', 'taken': '2019:05:20 15:09:11'},
            {'file': '/some/other/image2.jpg', 'size': 1081866, 'resolution': '4032 x 3024', 'taken': '2019:05:20 15:09:11'},
            {'file': '/some/another/image2.jpg', 'size': 1081866, 'resolution': '4032 x 3024', 'taken': '2019:05:20 15:09:11'}
        ]
    }
    mocked_similar_images = [
        {
            'confidence': '97%',
            'origin_file': '/some/original/image3.jpg',
            'target_file': '/some/other/image3.jpg',
            'origin_result': {
                'file': '/some/original/image3.jpg', 
                'size': 18384, 'resolution': '398 x 398', 'taken': 'Time unknown', 'confidence': 97
            }, 
            'target_result': {
                'file': '/some/other/image3.jpg', 
                'size': 17984, 'resolution': '398 x 398', 'taken': 'Time unknown', 'confidence': 97
            }
        },
        {
            'confidence': '17%',
            'origin_file': '/some/original/image4.jpg',
            'target_file': '/some/other/image4.jpg',
            'origin_result': {
                'file': '/some/original/image4.jpg', 
                'size': 17984, 'resolution': '398 x 398', 'taken': 'Time unknown', 'confidence': 97}, 
            'target_result': {
                'file': '/some/other/image4.jpg', 
                'size': 18384, 'resolution': '398 x 398', 'taken': 'Time unknown', 'confidence': 97
            }
        }
    ]

    print_image_results(mocked_identical_images, mocked_similar_images)

    assert "Displaying image results" in caplog.text
    assert "Duplicate Images: /some/original/image1.jpg;/some/other/image1.jpg;" in caplog.text
    assert "Duplicate Images: /some/original/image2.jpg;/some/other/image2.jpg;/some/another/image2.jpg;" in caplog.text
    assert "Similar Images: {'confidence': '97%', 'origin_file': '/some/original/image3.jpg', 'target_file': '/some/other/image3.jpg'" in caplog.text
    assert "Similar Images: {'confidence': '17%', 'origin_file': '/some/original/image4.jpg', 'target_file': '/some/other/image4.jpg'" in caplog.text
