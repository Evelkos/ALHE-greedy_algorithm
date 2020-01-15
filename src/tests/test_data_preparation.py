from typing import List

from src.greedy.author import Author
from src.greedy.data_preparation import (
    create_publications_list,
    normalize_data,
    prepare_authors,
    prepare_authors_and_their_publications,
    prepare_publications,
)
from src.greedy.publication import Publication
from src.greedy.settings import (
    AUTHOR_ID,
    CONTRIBUTION,
    INITIAL_PUBS,
    IS_EMPLOYEE,
    IS_IN_N,
    IS_MONOGRAPH,
    IS_PHD_STUDENT,
    PUBLICATION_CONTRIB_FOR_AUTHOR,
    PUBLICATION_ID,
    PUBLICATION_POINTS_FOR_AUTHOR,
)
from src.greedy.tools import compare_lists


def prepare_test_authors(data: dict):
    authors = []
    for idx in range(len(data[AUTHOR_ID])):
        a_id = data[AUTHOR_ID][idx]
        is_emp = data[IS_EMPLOYEE][idx]
        is_phd = data[IS_PHD_STUDENT][idx]
        contrib = data[CONTRIBUTION][idx]
        in_n = data[IS_IN_N][idx]
        authors.append(Author(a_id, is_emp, is_phd, contrib, in_n))
    return authors


def prepare_test_authors_data():
    return {
        AUTHOR_ID: ["0", "1", "2", "3"],
        IS_EMPLOYEE: [False, False, True, True],
        IS_PHD_STUDENT: [False, True, True, False],
        CONTRIBUTION: [1.0, 0.5, 1.0, 0.5],
        IS_IN_N: [1, 1, 0, 1],
    }


def prepare_test_publications(
    ids: List[str], mons: List[bool], points: List[float], ctbs: List[float]
):
    pubs = []
    for p_id, mon, pts, cbs in zip(ids, mons, points, ctbs):
        if pts > 0 and cbs > 0:
            pubs.append(Publication(p_id, mon, pts, cbs))
    return pubs


def prepare_test_publications_data():
    ids = ["0", "1", "2", "3", "4"]
    mons = [True, False, True, False, True]
    points = [0, 0, 1, 1, 2]
    ctbs = [0.0, 1.0, 0.5, 0.0, 1.0]
    return ids, mons, points, ctbs


def test_normalize_data():
    data = {IS_EMPLOYEE: [0, 0, 1, 1], IS_PHD_STUDENT: [0, 1, 1, 0]}
    result = {
        IS_EMPLOYEE: [False, False, True, True],
        IS_PHD_STUDENT: [False, True, True, False],
    }
    assert normalize_data(data) == result


def test_prepare_authors():
    data = prepare_test_authors_data()
    authors = prepare_test_authors(data)

    prepared_authors = prepare_authors(data)

    assert compare_lists(authors, prepared_authors)


def test_create_publications_list():
    ids, mons, points, ctbs = prepare_test_publications_data()
    pubs = prepare_test_publications(ids, mons, points, ctbs)

    result = create_publications_list(ids, mons, points, ctbs)
    assert compare_lists(result, pubs)


def test_prepare_publications():
    ids, mons, points, ctbs = prepare_test_publications_data()
    authors = prepare_test_authors(prepare_test_authors_data())
    test_authors = prepare_test_authors(prepare_test_authors_data())

    data = {
        PUBLICATION_ID: ids,
        IS_MONOGRAPH: mons,
        PUBLICATION_POINTS_FOR_AUTHOR: [points for _ in range(len(authors))],
        PUBLICATION_CONTRIB_FOR_AUTHOR: [ctbs for _ in range(len(authors))],
        INITIAL_PUBS: [[0 for _ in range(len(ids))] for _ in range(len(authors))],
    }

    for author in test_authors:
        author.load_publications(prepare_test_publications(ids, mons, points, ctbs))

    prepare_publications(authors, data)
    assert authors == test_authors


def test_prepare_authors_and_their_publications_with_multiple_authors():
    data = {
        PUBLICATION_ID: ["0", "1", "2"],
        IS_MONOGRAPH: [1, 1, 0],
        PUBLICATION_POINTS_FOR_AUTHOR: [[0, 0, 1], [2, 0, 0], [0, 1, 0]],
        PUBLICATION_CONTRIB_FOR_AUTHOR: [[0, 0, 1.0], [0.5, 0, 0], [0, 0, 0]],
        AUTHOR_ID: ["a", "b", "c"],
        IS_EMPLOYEE: [1, 1, 0],
        IS_PHD_STUDENT: [0, 1, 1],
        CONTRIBUTION: [1.0, 0.5, 1.0],
        IS_IN_N: [1, 1, 1],
        INITIAL_PUBS: [[0 for _ in range(3)] for _ in range(3)],
    }

    authors = prepare_authors_and_their_publications(data)

    data = normalize_data(data)
    test_authors = prepare_test_authors(data)

    test_authors[0].publications = [Publication("2", False, 1, 1.0)]
    test_authors[0].to_considerate = test_authors[0].publications
    test_authors[1].publications = [Publication("0", True, 2, 0.5)]
    test_authors[1].to_considerate = test_authors[1].publications
    test_authors[2].publications = []
    test_authors[2].to_considerate = []

    assert authors == test_authors


def test_prepare_authors_and_their_publications_with_one_pub_with_too_big_contrib():
    data = {
        PUBLICATION_ID: ["0", "1", "2"],
        IS_MONOGRAPH: [1, 0, 0],
        PUBLICATION_POINTS_FOR_AUTHOR: [[69, 0, 1]],
        PUBLICATION_CONTRIB_FOR_AUTHOR: [[96.0, 0, 1.0]],
        AUTHOR_ID: ["a"],
        IS_EMPLOYEE: [1],
        IS_PHD_STUDENT: [0],
        CONTRIBUTION: [1.0],
        IS_IN_N: [1],
        INITIAL_PUBS: [[0 for _ in range(3)] for _ in range(3)],
    }

    authors = prepare_authors_and_their_publications(data)

    data = normalize_data(data)
    test_authors = prepare_test_authors(data)
    test_publications = [
        Publication("0", True, 69, 96.0),
        Publication("2", False, 1, 1.0),
    ]
    test_authors[0].publications = test_publications
    test_authors[0].to_considerate = [test_publications[1]]

    assert authors == test_authors
