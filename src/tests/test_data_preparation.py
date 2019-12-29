import pytest

from src.greedy.tools import compare_lists
from src.greedy.author import Author
from src.greedy.data_preparation import (
    count_author_rate,
    create_publications_list,
    normalize_data,
    prepare_authors,
    prepare_publications,
    prepare_authors_and_their_publications,
    set_rate_for_authors,
    sort_authors,
)
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
from src.tests.test_author import (
    count_publications_rates_sum,
    create_complex_publications_list,
    prepare_basic_test_data,
    prepare_complex_test_data,
)
from typing import List


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


def test_count_author_rate():
    author, publications, pubs_rates_sum = prepare_basic_test_data()
    assert count_author_rate(author) == pubs_rates_sum / len(publications)


def test_count_author_rate_with_publications_reloaded():
    author, _, _ = prepare_basic_test_data()
    publications = create_complex_publications_list()

    prev_pubs = author.to_considerate
    author.load_publications(publications)
    author.create_publications_ranking()

    pubs_rates_sum = count_publications_rates_sum(author.to_considerate)

    assert not prev_pubs == author.to_considerate
    assert count_author_rate(author) == pubs_rates_sum / len(author.to_considerate)


def test_count_author_rate_with_zero_publications_to_considerate():
    author, _, _ = prepare_basic_test_data()
    author.to_considerate = []

    assert count_author_rate(author) == 0


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
    }

    for author in test_authors:
        author.load_publications(prepare_test_publications(ids, mons, points, ctbs))
        author.create_publications_ranking()

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
    }

    authors = prepare_authors_and_their_publications(data)

    data = normalize_data(data)
    test_authors = prepare_test_authors(data)
    test_publications = [
        Publication("0", True, 69, 96.0),
        Publication("2", False, 1, 1.0)
    ]
    test_authors[0].publications = test_publications
    test_authors[0].to_considerate = [test_publications[1]]
    
    assert authors == test_authors


def test_set_rate_for_authors():
    authors = prepare_test_authors(prepare_test_authors_data())
    for idx, author in enumerate(authors, 0):
        author.set_rate(idx)

    sorted_authors = sort_authors(authors)
    authors.reverse()

    assert sorted_authors == authors
