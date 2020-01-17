from typing import List
import os
from src.greedy.publication import Publication
from src.greedy.settings import (
    AUTHOR_ID,
    EMPLOYEES_NUM,
    PUBLICATION_ID,
    PUBLICATIONS_NUM,
    THRESHOLDS_SUFFIX,
)


def get_empty_vector(rows: int, columns: int) -> List[List[int]]:
    """
    Prepares vector to store algorithm result: authors and their publications

    Args:
        rows: number of rows
        columns: number of columns

    Returns:
        list of lists to store information about authors and their publications
    """
    return [[0 for _ in range(columns)] for _ in range(rows)]


def get_idx_map(data: dict, key: str) -> dict:
    """
    Prepares dictionary that mapes objects from list in data[key] to list indices

    Args:
        data: stores list of objects to map
        key: dictionary key

    Returns:
        dictionary that mapes list objects to indices in this list

    """
    result = {}
    for idx, single_id in enumerate(data[key], 0):
        result.update({single_id: idx})
    return result


def convert_dictionary_to_vector(pubs_auths: dict, data: dict) -> List[List[int]]:
    """
    Converts dictionary returned

    Args:
        pubs_auths: contains information about accepted publications and authors
        data: contains information about authors and publications from input file

    Returns:
        vector in which each row is a single author and columns are his publications.
        Every '1' in vector means that specific publication was choosen to be
        published

    """

    result = get_empty_vector(data[EMPLOYEES_NUM], data[PUBLICATIONS_NUM])
    authors_idx_map = get_idx_map(data, AUTHOR_ID)
    publications_idx_map = get_idx_map(data, PUBLICATION_ID)

    for publication_id in pubs_auths.keys():
        for author_id in pubs_auths[publication_id]:
            row = authors_idx_map[author_id]
            column = publications_idx_map[publication_id]
            result[row][column] += 1

    return result


def convert_publications_to_dictionary(publications: List[Publication]) -> dir:
    """
    Converts list of publications to dictionary

    Args:
        publications: list of publications

    Returns:
        doctionary with publications' ids as keys and lists of authors as values
        Ex.
        {
            "pub1": ["auth1", "auth2"],
            "pub2": ["auth3", "auth4"],
            "pub9": ["auth3"],
        }
    """
    result_publications = {}
    for pub in publications:
        if not pub.get_id() in result_publications:
            result_publications.update({pub.get_id(): [pub.get_author().get_id()]})
        else:
            result_publications[pub.get_id()].append(pub.get_author().get_id())
    return result_publications


def get_result_path(
    input_path: str, mode: int, idx: int, test_try: int, results_dir: str
) -> str:
    path = input_path.split("/")
    filename = path[len(path) - 1].split(("-"))[0]
    single_test_dir = os.path.join(results_dir, filename)

    if not os.path.exists(single_test_dir):
        os.mkdir(single_test_dir)

    return os.path.join(single_test_dir, f"{filename}_{mode}_{idx}_{test_try}.txt")


def save_results(path: str, data: dir, goal: float, vec: List[List[int]]) -> None:
    with open(path, "w") as f:
        tmp_goals = data["threshold_goal_values"]
        for threshold in tmp_goals:
            f.write(f"{THRESHOLDS_SUFFIX}{threshold} = {tmp_goals[threshold]};")
            f.write("\n")
        f.write("\n")
        f.write(f"final_goal_function = {goal};")
        f.write("\n")
        f.write("\n")
        f.write(f"vector = {vec};")