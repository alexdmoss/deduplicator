from deduplicator.parse import remove_files_with_no_duplicates


def test_remove_files_with_no_duplicates():
    test_data = {}
    test_data['e8114e843bc16f5e895d6aa752bf3584'] = ['./test/barca_dupe_level_0.jpg',
                                                     './test/level_1/barca_dupe_level_1.jpg',
                                                     './test/level_1/level_2/barca_dupe_level_2.jpg']
    test_data['1d626efa9c786692344142cd7ef982c1'] = ['./test/lol_dupe_level_0.jpg',
                                                     './test/level_1/lol_dupe_level_1.jpg']
    test_data['7df4590c7de2a654dbd0de8a4ecb680d'] = ['./test/queen_no_dupe_level_0.jpg']
    test_data['3300d0cec39386604c5e387404660a05'] = ['./test/what_dupe_level_0.jpg',
                                                     './test/level_1/level_2/what_dupe_level_2.jpg']
    test_data['d6301cd22dff266fede98ef879a68ab5'] = ['./test/level_1/beans_no_dupe_level_1.jpeg']

    dupes = remove_files_with_no_duplicates(test_data)

    all_dupes = []
    for files in dupes.values():
        all_dupes = all_dupes + files

    assert './test/barca_dupe_level_0.jpg' in all_dupes
    assert './test/level_1/barca_dupe_level_1.jpg' in all_dupes
    assert './test/lol_dupe_level_0.jpg' in all_dupes
    assert './test/level_1/lol_dupe_level_1.jpg' in all_dupes
    assert './test/what_dupe_level_0.jpg' in all_dupes
    assert './test/level_1/level_2/what_dupe_level_2.jpg' in all_dupes
    assert './test/queen_no_dupe_level_0.jpg' not in all_dupes
    assert './test/level_1/beans_no_dupe_level_1.jpg' not in all_dupes
    assert len(all_dupes) == 7
