import os
from typing import Any, List


def compare_lists(list1: List[Any], list2: List[Any]):
    if (list1 is None) ^ (list2 is None):
        return False
    if list1 is not None:
        if not len(list1) == len(list2):
            return False
        for pub in list1:
            if pub not in list2:
                return False
    return True


def get_list_of_files_from_dir(dirpath: str, suffix: str):
    files = []
    for file in os.listdir(dirpath):
        if file.endswith(suffix):
            files.append(os.path.join(dirpath, file))
    return files
