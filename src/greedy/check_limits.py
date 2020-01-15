from typing import List

from src.greedy.author import (
    MONOGRAPH_COEFFICIENT,
    PUBLICATIONS_COEFFICIENT,
    PUBLICATIONS_COEFFICIENT_FOR_PHD,
    Author,
)
from src.greedy.publication import Publication
from src.greedy.settings import EMPLOYEES_NUM, N0, N1, N2


def check_publications_number_limit(data: dict, contrib_sum: float) -> bool:
    limit = 3 * data[EMPLOYEES_NUM] - 3 * data[N0] - 6 * data[N1] - 6 * data[N2]
    return contrib_sum < limit


def check_monographs_number_limit(data: dict, monograph_sum: float) -> bool:
    return monograph_sum < 0.15 * data[EMPLOYEES_NUM]


def check_phd_students_and_outsiders(data: dict, phd_and_outsiders: float) -> bool:
    return phd_and_outsiders < 0.6 * data[EMPLOYEES_NUM]


def check_full_limits(data: dict, current_sums: dict):
    if not check_publications_number_limit(data, current_sums["contrib_sum"]):
        return False
    if not check_monographs_number_limit(data, current_sums["monograph_sum"]):
        return False
    if not check_phd_students_and_outsiders(data, current_sums["phd_and_outsiders"]):
        return False
    return True


def check_limits(data: dict, current_sums: dict):
    if current_sums["contrib_sum"] <= 3 * data[EMPLOYEES_NUM]:
        return True


def check_full_author_limits(auth: Author, publications: List[Publication]):
    if auth.is_employee():
        publications_sum = 0
        for pub in publications:
            publications_sum += pub.get_contribution()
        assert publications_sum <= auth.get_contribution() * PUBLICATIONS_COEFFICIENT

    if auth.is_employee() and not auth.is_phd_student():
        monograph_sum = 0
        for pub in publications:
            monograph_sum += pub.get_contribution() if pub.is_monograph() else 0.0
        assert monograph_sum <= auth.get_contribution() * MONOGRAPH_COEFFICIENT

    if auth.is_phd_student():
        publications_sum = 0
        for pub in publications:
            publications_sum += pub.get_contribution()
        assert publications_sum <= PUBLICATIONS_COEFFICIENT_FOR_PHD
    return True


def check_author_limits(auth: Author, publications: List[Publication]):
    publications_sum = 0
    for pub in publications:
        publications_sum += pub.get_contribution()
    assert publications_sum <= 4.0
    return True


def count_curr_sums_for_publications(publications):
    contrib_sum = 0
    monograph_sum = 0
    phd_and_outsiders = 0

    for pub in publications:
        contrib_sum += pub.get_contribution()
        if pub.is_monograph():
            monograph_sum += pub.get_contribution()
        if pub.get_author().is_phd_student() or not pub.get_author().is_employee():
            phd_and_outsiders += pub.get_contribution()

    curr_sums = {
        "contrib_sum": contrib_sum,
        "monograph_sum": monograph_sum,
        "phd_and_outsiders": phd_and_outsiders,
    }
    return curr_sums
