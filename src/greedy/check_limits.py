from typing import List

from src.greedy.author import (
    MONOGRAPH_COEFFICIENT,
    PUBLICATIONS_COEFFICIENT,
    PUBLICATIONS_COEFFICIENT_FOR_PHD,
    Author,
)
from src.greedy.publication import Publication


def check_author_limits(auth: Author, publications: List[Publication]):
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
