from typing import Any, List

from src.greedy.author import Author
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


def count_author_rate(author):
    points = author.get_sum_of_publications_to_considerate()
    num = author.get_number_of_publications_to_considerate()
    return points / num


def prepare_authors(
    authors: List[str],
    employees: List[int],
    phd_students: List[int],
    contribution: List[float],
    is_in_n: List[int],
) -> List[Author]:
    result = []
    for author, is_emp, is_phd, cont, in_n in zip(
        authors, employees, phd_students, contribution, is_in_n
    ):
        is_emp = False if is_emp == 0 else True
        is_phd = False if is_phd == 0 else True
        author = Author(author, is_emp, is_phd, cont, in_n)
        result.append(author)

    return result


def prepare_publications(
    authors: List[Author],
    publications: List[Any],
    monographs: List[int],
    publications_points: List[float],
    publications_contributions: List[Any],
) -> None:
    for author, points, contrib in zip(
        authors, publications_points, publications_contributions
    ):
        author.load_publications(publications, monographs, points, contrib)
        author.create_publications_ranking()


def prepare_authors_and_their_publications(data):
    authors = prepare_authors(
        data[AUTHOR_ID],
        data[IS_EMPLOYEE],
        data[IS_PHD_STUDENT],
        data[CONTRIBUTION],
        data[IS_IN_N],
    )
    prepare_publications(
        authors,
        data[PUBLICATION_ID],
        data[IS_MONOGRAPH],
        data[PUBLICATION_POINTS_FOR_AUTHOR],
        data[PUBLICATION_CONTRIB_FOR_AUTHOR],
    )

    return authors


def set_rate_for_authors(authors):
    for auth in authors:
        auth.set_rate(count_author_rate(auth))


def sort_authors(authors: List[Author]):
    set_rate_for_authors(authors)
    return sorted(authors, key=lambda author: author.get_rate(), reverse=True)
