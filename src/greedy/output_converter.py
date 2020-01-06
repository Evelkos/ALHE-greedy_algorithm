from src.greedy.settings import EMPLOYEES_NUM, PUBLICATIONS_NUM, AUTHOR_ID, PUBLICATION_ID
from typing import List


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