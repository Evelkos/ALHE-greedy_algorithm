from typing import Any, List

from src.greedy.publication import Publication

PUBLICATIONS_COEFFICIENT = 4
MONOGRAPH_COEFFICIENT = 2
MONOGRAPH_LIMIT_MAX_POINTS = 100.0
MIN_CONTRIBUTION = 0.25
MAX_CONTRIBUTION = 1
PUBLICATIONS_COEFFICIENT_FOR_PHD = 2


class Author:
    def __init__(
        self, author_id: str, is_emp: bool, is_phd: bool, contrib: float, czyn: int
    ):
        self.id = author_id
        self.is_phd = is_phd
        self.is_emp = is_emp
        self.czyn = czyn
        self.contribution = Author.__update_contribution(contrib)

        self.publications = None
        self.to_considerate = None
        self.rate = None
        self.__publications_to_considerate_sum = None

    def __str__(self):
        return f"{self.id}"

    def __check_if_to_considerate_list_is_not_none(self):
        if self.to_considerate is None:
            raise AttributeError(
                "No publications ranking. Use create_publications_ranking() first"
            )

    def __check_if_to_considerate_list_is_not_empty(self):
        self.__check_if_to_considerate_list_is_not_none()
        if len(self.to_considerate) == 0:
            raise AttributeError(
                """No publications to considerate.
                Use load_publications() and create_publications_ranking() first"""
            )

    def __check_if_publications_are_loaded(self):
        if self.publications is None:
            raise AttributeError(
                """Publications not loaded.
                Use load_publications() first"""
            )

    def __check_if_rate_is_set(self):
        if self.rate is None:
            raise AttributeError("Rate not set. Use set_rate() first")

    def __check_limits(
        self,
        tmp_contrib_sum: float,
        tmp_contrib_mono_sum: float,
        is_mono: bool,
        pub: Publication,
    ) -> bool:
        if self.is_emp:
            if not self.__check_publications_limit(tmp_contrib_sum):
                return False
            if not self.__check_moographs_limit(tmp_contrib_mono_sum, is_mono, pub):
                return False
        if not self.__check_limits_for_phd_students(tmp_contrib_sum):
            return False
        return True

    def __check_moographs_limit(
        self, tmp_contrib_monograph_sum: float, is_monograph: bool, pub: Publication
    ) -> bool:
        if self.is_phd:
            return True
        elif not is_monograph:
            return True
        elif tmp_contrib_monograph_sum <= MONOGRAPH_COEFFICIENT * self.contribution:
            return True
        elif pub.get_points() > MONOGRAPH_LIMIT_MAX_POINTS:
            return True
        return False

    def __check_publications_limit(self, tmp_contrib_sum: float) -> bool:
        return tmp_contrib_sum <= PUBLICATIONS_COEFFICIENT * self.contribution

    def __check_limits_for_phd_students(self, tmp_contrib_sum: float) -> bool:
        if not self.is_phd:
            return True
        elif tmp_contrib_sum <= PUBLICATIONS_COEFFICIENT_FOR_PHD:
            return True
        return False

    def __choose_best_publications(self, rated_pubs: List[Publication]):
        contrib_sum = 0
        contrib_monograph_sum = 0
        best_publications = []

        for pub in rated_pubs:
            pub_contrib = pub.get_contribution()
            is_mono = pub.is_monograph()
            tmp_contrib_sum = contrib_sum + pub_contrib
            tmp_contrib_mono_sum = 0
            if is_mono:
                tmp_contrib_mono_sum = contrib_monograph_sum + pub_contrib
            if self.__check_limits(tmp_contrib_sum, tmp_contrib_mono_sum, is_mono, pub):
                best_publications.append(pub)
                contrib_sum = tmp_contrib_sum
                contrib_monograph_sum = tmp_contrib_mono_sum

        return best_publications

    def __get_sorted_publications(self):
        return sorted(self.publications, key=lambda pub: pub.get_rate(), reverse=True)

    def __update_contribution(contribution: float):
        # TODO - check first limit - how to count contribution
        if contribution < MIN_CONTRIBUTION:
            return MIN_CONTRIBUTION
        elif contribution > MAX_CONTRIBUTION:
            return MAX_CONTRIBUTION
        else:
            return contribution

    def count_sum_of_publications_to_considerate(self):
        self.__check_if_to_considerate_list_is_not_none()
        pub_sum = 0
        for pub in self.to_considerate:
            pub_sum += pub.get_rate()
        return pub_sum

    def create_publications_ranking(self):
        self.__check_if_publications_are_loaded()

        rated_pubs = self.__get_sorted_publications()
        self.to_considerate = self.__choose_best_publications(rated_pubs)

        return self.to_considerate

    def get_contribution(self):
        return self.contribution

    def get_publications(self):
        self.__check_if_publications_are_loaded()
        return self.publications

    def get_publications_to_considerate(self):
        return self.to_considerate

    def get_number_of_publications_to_considerate(self):
        self.__check_if_to_considerate_list_is_not_none()
        return len(self.to_considerate)

    def get_sum_of_publications_to_considerate(self):
        self.__check_if_to_considerate_list_is_not_none()

        if self.__publications_to_considerate_sum is None:
            self.__publications_to_considerate_sum = (
                self.count_sum_of_publications_to_considerate()
            )

        return self.__publications_to_considerate_sum

    def get_average_pub_points(self):
        self.__check_if_to_considerate_list_is_not_empty()
        return self.get_sum_of_publications_to_considerate() / len(self.to_considerate)

    def get_rate(self):
        self.__check_if_rate_is_set()
        return self.rate

    def is_phd_student(self):
        return self.is_phd

    def is_employee(self):
        return self.is_emp

    def load_publications(self, publications) -> None:
        result = []
        for pub in publications:
            if pub.get_points() > 0 and pub.get_contribution() > 0:
                result.append(pub)

        self.publications = result

    def set_rate(self, new_rate: float):
        self.rate = new_rate
