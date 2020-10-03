def remove_files_with_no_duplicates(all_files: dict) -> dict:
    duplicates = {}
    for md, files in all_files.items():
        if len(files) > 1:
            duplicates[md] = files
    return duplicates
