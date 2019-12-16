from typing import Any, List

import numpy as np
import pandas as pd

from implementation.author import Author
from implementation.publication import Publication
from implementation.settings import (
    AUTHOR_ID,
    CONTRIBUTION,
    CZYN,
    IS_EMPLOYEE,
    IS_MONOGRAPH,
    IS_PHD_STUDENT,
    PUBLICATION_CONTRIB_FOR_AUTHOR,
    PUBLICATION_ID,
    PUBLICATION_POINTS_FOR_AUTHOR,
)


def prepare_publications_dictionary(publications: List[str], monograph: List[int]):
    assert len(publications) == len(monograph)
    return {
        idx: {
            "id": publications[idx],
            "is_monograph": True if monograph[idx] == 1 else False,
        }
        for idx in range(len(publications))
    }


def prepare_authors(
    authors: List[str],
    employees: List[int],
    phd_students: List[int],
    contribution: List[float],
    czyn: List[int],
) -> pd.DataFrame:
    result = []
    for author, is_emp, is_phd, cont, cz in zip(
        authors,
        employees,
        phd_students,
        contribution,
        czyn,
    ):
        is_emp = False if 0 else True
        is_phd = False if 0 else True
        author = Author(author, is_emp, is_phd, cont, cz)
        result.append(author)

    return result

def prepare_publications(
    authors: List[Author],
    publications: List[Any],
    monographs: List[int],
    publications_points: List[float],
    publications_contributions: List[Any],
    ) -> None:
    for author, points, contrib in zip(authors, publications_points, publications_contributions):
        author.load_publications(publications, monographs, points, contrib)
        author.create_publications_ranking()


def run_greedy(data):
    authors = prepare_authors(
        data[AUTHOR_ID],
        data[IS_EMPLOYEE],
        data[IS_PHD_STUDENT],
        data[CONTRIBUTION],
        data[CZYN],
    )
    prepare_publications(authors, data[PUBLICATION_ID], data[IS_MONOGRAPH], data[PUBLICATION_POINTS_FOR_AUTHOR], data[PUBLICATION_CONTRIB_FOR_AUTHOR])

    return 0
