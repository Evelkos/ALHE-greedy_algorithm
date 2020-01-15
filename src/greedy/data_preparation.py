from typing import List

import numpy as np

from src.greedy.author import Author
from src.greedy.output_converter import get_empty_vector, get_idx_map
from src.greedy.publication import Publication
from src.greedy.settings import (
    AUTHOR_ID,
    CONTRIBUTION,
    EMPLOYEES_NUM,
    INITIAL_PUBS,
    IS_EMPLOYEE,
    IS_IN_N,
    IS_MONOGRAPH,
    IS_PHD_STUDENT,
    PUBLICATION_CONTRIB_FOR_AUTHOR,
    PUBLICATION_ID,
    PUBLICATION_POINTS_FOR_AUTHOR,
    PUBLICATIONS_NUM,
)


def normalize_data(data: dict):
    """
    Normalizes data from given dictionary (changes all zeros to False values and
    all ones to True values) for functions that load authors.

    Args:
        data: dictionary that contains data needed to load authors and their
            publications. It contains keys IS_EMPLOYEE and IS_PHD_STUDENT, specified
            in settings.py file

    Returns:
        Normalized dictionary

    """
    data[IS_EMPLOYEE] = [False if emp == 0 else True for emp in data[IS_EMPLOYEE]]
    data[IS_PHD_STUDENT] = [False if ps == 0 else True for ps in data[IS_PHD_STUDENT]]
    return data


def prepare_authors(data: dict) -> List[Author]:
    """
    Prepares list of authors without their publications list

    Args:
        data: dictionary with keyes:
            AUTHOR_ID: list of authors' ids
            IS_EMPLOYEE: list that defines which authors are employees
            IS_PHD_STUDENT: list that defines which authors are phd students
            CONTRIBUTION: list of authors' contributions
            IS_IN_N: list that defines which authors are in N
            All keys are defined in settings.py

    Returns:
        List of authors

    """
    result = []
    for idx in range(len(data[AUTHOR_ID])):
        author_id = data[AUTHOR_ID][idx]
        is_emp = data[IS_EMPLOYEE][idx]
        is_phd = data[IS_PHD_STUDENT][idx]
        cont = data[CONTRIBUTION][idx]
        in_n = data[IS_IN_N][idx]
        result.append(Author(author_id, is_emp, is_phd, cont, in_n))
    return result


def create_publications_list(
    pubs: List[str],
    mons: List[int],
    points: List[float],
    contribs: List[float],
    init: List[int] = None,
):
    """
    Creates publications list for single author.

    Args:
        pubs: list of publications' ids
        mons: list that defines which publications are monographs
        points: lists that contains points from publications for single author
        contribs: list that contains contributions from publications for single
            author

    Returns:
        List of publications. Publications with 0 points or 0.0 contribution are
        not contained
    """
    if init is None:
        init = [0 for _ in range(len(pubs))]

    assert len(pubs) == len(mons)
    assert len(points) == len(contribs)
    assert len(pubs) == len(contribs)
    assert len(init) == len(pubs)

    result = []

    for pub_id, is_mon, pts, contrib, ini in zip(pubs, mons, points, contribs, init):
        if pts > 0 and contrib > 0:
            is_mon = False if is_mon == 0 else True
            ini = False if ini == 0 else True
            result.append(Publication(pub_id, is_mon, pts, contrib, None, ini))

    return result


def prepare_publications(authors: List[Author], data: dict) -> None:
    """
    Prepares lists of publications, attaches them to authors and creates ranking of
    publications for each author.

    Args:
        authors: list of authors
        data: dictionary with keys:
            PUBLICATION_ID: list of publications' ids
            IS_MONOGRAPH: list that defines which publications are monographs
            PUBLICATION_POINTS_FOR_AUTHOR: list of lists. Each list contains
                publications' points for single author
            PUBLICATION_CONTRIB_FOR_AUTHOR: list of lists. Each list contains
                publications' contributions for single author
            INITIAL_PUBS: list of lists. Each list defines author's publications
                included in initial result
            All keys are defined in settings.py

    """
    pubs_ids = data[PUBLICATION_ID]
    mons = data[IS_MONOGRAPH]

    for idx, author in enumerate(authors, 0):
        auth_pubs = data[PUBLICATION_POINTS_FOR_AUTHOR][idx]
        auth_contrs = data[PUBLICATION_CONTRIB_FOR_AUTHOR][idx]
        init = data[INITIAL_PUBS][idx]
        pubs = create_publications_list(pubs_ids, mons, auth_pubs, auth_contrs, init)
        author.load_publications(pubs)

    return authors


def get_temporary_pub_rate(pub: Publication):
    return pub.get_points() / pub.get_contribution()


def get_empty_choosen_pubs_list(data) -> List[List[int]]:
    """
    Returns empty vector.

    Returns:
        List of lists that contains publications that need to be included in
        greedy algorithm result.

    """
    return get_empty_vector(data[EMPLOYEES_NUM], data[PUBLICATIONS_NUM])


def get_full_choosen_pubs_list(data: dict) -> List[List[int]]:
    """
    Chooses all publications for every author.

    Args:
        data: contains normalized data from input file

    Returns:
        List of lists that contains publications that need to be included in
        greedy algorithm result.

    """
    publications = get_empty_vector(data[EMPLOYEES_NUM], data[PUBLICATIONS_NUM])

    rows = len(data[PUBLICATION_POINTS_FOR_AUTHOR])
    columns = len(data[PUBLICATION_POINTS_FOR_AUTHOR][0])
    for row in range(rows):
        for column in range(columns):
            points = data[PUBLICATION_POINTS_FOR_AUTHOR][row][column]
            contrib = data[PUBLICATION_CONTRIB_FOR_AUTHOR][row][column]
            if points != 0 and contrib != 0:
                publications[row][column] += 1

    return publications


def get_choosen_pubs(data: dict, auth_pubs_num: int, shuffle) -> List[List[int]]:
    """
    Chooses number of publications for every author. Publications are shuffled by
    shuffle function (ex. sort_pubs(), shuffle_pubs()) then first auth_pubs_num
    publications are selected

    Args:
        data: contains normalized data from input file
        auth_pubs_num: number of publications choosen for author

    Returns:
        List of lists that contains publications that need to be included in
        greedy algorithm result.

    """
    publications = get_empty_vector(data[EMPLOYEES_NUM], data[PUBLICATIONS_NUM])
    publications_idx_map = get_idx_map(data, PUBLICATION_ID)
    pubs_ids = data[PUBLICATION_ID]
    mons = data[IS_MONOGRAPH]

    for auth in range(len(data[PUBLICATION_POINTS_FOR_AUTHOR])):
        auth_pubs = data[PUBLICATION_POINTS_FOR_AUTHOR][auth]
        auth_contribs = data[PUBLICATION_CONTRIB_FOR_AUTHOR][auth]
        pubs = create_publications_list(pubs_ids, mons, auth_pubs, auth_contribs)
        pubs = shuffle(pubs)

        contrib_sum = 0
        choosen_pubs = 0
        for pub in pubs:
            if choosen_pubs >= auth_pubs_num:
                break
            if pub.get_contribution() + contrib_sum <= 4:
                pub_idx = publications_idx_map[pub.get_id()]
                contrib_sum += pub.get_contribution()
                publications[auth][pub_idx] += 1
                choosen_pubs += 1
    return publications


def sort_pubs(pubs: List[Publication]) -> List[Publication]:
    result = sorted(pubs, key=lambda pub: get_temporary_pub_rate(pub), reverse=True)
    return result


def shuffle_pubs(pubs: List[Publication]) -> List[Publication]:
    np.random.shuffle(pubs)
    return pubs


def get_initial_publications(
    mode: int, data: dict, auth_pubs_num: int = None
) -> List[List[int]]:
    """
    Prepares initial publications list according to choosen mode.

    Args:
        mode:
            0 - empty publications list
            1 - full publications list
            2 - first auth_pubs_num publications from sorted publications list
            3 - first auth_pubs_num publications from sorted shuffled list
        data: contains normalized data from input file
        auth_pubs_num: initial number of publications choosen for each author

    Returns:
        List of initial, accepted publications (List of lists with zeros or ones)

    Raises:
        AttributeError if given mode does not exist

    """
    if mode == 0:
        return get_empty_choosen_pubs_list(data)
    elif mode == 1:
        return get_full_choosen_pubs_list(data)
    elif mode == 2:
        return get_choosen_pubs(data, auth_pubs_num, sort_pubs)
    elif mode == 3:
        return get_choosen_pubs(data, auth_pubs_num, shuffle_pubs)
    raise AttributeError("Wrong mode choosen. Supported modes: 0, 1, 2, 3")


def prepare_authors_and_their_publications(data: dict) -> None:
    """
    Main function for data preparation.
    Normalizes data and then creates authors and lists of publications. Attaches
    publications to authors

    Args:
        data: dictionary with keys:
            PUBLICATION_ID: list of publications' ids
            IS_MONOGRAPH: list that defines which publications are monographs
            PUBLICATION_POINTS_FOR_AUTHOR: list of lists. Each list contains
                publications' points for single author
            PUBLICATION_CONTRIB_FOR_AUTHOR: list of lists. Each list contains
                publications' contributions for single author
            AUTHOR_ID: list of authors' ids
            IS_EMPLOYEE: list that defines which authors are employees
            IS_PHD_STUDENT: list that defines which authors are phd students
            CONTRIBUTION: list of authors' contributions
            IS_IN_N: list that defines which authors are in N
            INITIAL_PUBS: list of lists. Each list defines author's publications
                included in initial result
            All keys are defined in settings.py

    Returns:
        List of authors (for tests)

    """
    authors = prepare_authors(data)
    prepare_publications(authors, data)

    return authors
