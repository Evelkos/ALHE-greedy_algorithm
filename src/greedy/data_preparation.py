from typing import Any, List

from src.greedy.author import Author
from src.greedy.publication import Publication
from src.greedy.settings import (
    AUTHOR_ID,
    CONTRIBUTION,
    IS_EMPLOYEE,
    IS_IN_N,
    IS_MONOGRAPH,
    IS_PHD_STUDENT,
    PUBLICATION_CONTRIB_FOR_AUTHOR,
    PUBLICATION_ID,
    PUBLICATION_POINTS_FOR_AUTHOR,
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


def count_author_rate(author: Author) -> float:
    """
    Counts single author rate.

    Args:
        author: single author

    Returns:
        Author's rate

    """
    points = author.get_sum_of_publications_to_considerate()
    num = author.get_number_of_publications_to_considerate()

    if num == 0:
        return 0

    return points / num


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
    pubs: List[str], mons: List[int], points: List[float], contribs: List[float]
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
    assert len(pubs) == len(mons)
    assert len(points) == len(contribs)
    assert len(pubs) == len(contribs)

    result = []
    for pub_id, is_mon, pts, contrib in zip(pubs, mons, points, contribs):
        if pts > 0 and contrib > 0:
            is_mon = False if is_mon == 0 else True
            result.append(Publication(pub_id, is_mon, pts, contrib))

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
            All keys are defined in settings.py

    """
    pubs_ids = data[PUBLICATION_ID]
    mons = data[IS_MONOGRAPH]

    for idx, author in enumerate(authors, 0):
        auth_pubs = data[PUBLICATION_POINTS_FOR_AUTHOR][idx]
        auth_contribs = data[PUBLICATION_CONTRIB_FOR_AUTHOR][idx]
        pubs = create_publications_list(pubs_ids, mons, auth_pubs, auth_contribs)
        author.load_publications(pubs)
        author.create_publications_ranking()
    return authors


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
            All keys are defined in settings.py

    Returns:
        List of authors (for tests)

    """
    data = normalize_data(data)
    authors = prepare_authors(data)
    prepare_publications(authors, data)
    return authors


def set_rate_for_authors(authors: List[Author]) -> None:
    """
    Counts and sets rates for authors.

    Args:
        autors: list of authors

    """
    for auth in authors:
        auth.set_rate(count_author_rate(auth))


def sort_authors(authors: List[Author]):
    """
    Sorts authors by rate
    """
    return sorted(authors, key=lambda author: author.get_rate(), reverse=True)
