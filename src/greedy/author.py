from src.greedy.publication import Publication
from src.greedy.tools import compare_lists

PUBLICATIONS_COEFFICIENT = 4
MONOGRAPH_COEFFICIENT = 2
MONOGRAPH_LIMIT_MAX_POINTS = 100.0
MIN_CONTRIBUTION = 0.25
MAX_CONTRIBUTION = 1
PUBLICATIONS_COEFFICIENT_FOR_PHD = 4


class Author:
    def __init__(
        self, author_id: str, is_emp: bool, is_phd: bool, contrib: float, in_n: int
    ):
        self.id = author_id
        self.is_phd = is_phd
        self.is_emp = is_emp
        self.in_n = in_n
        self.contribution = Author.__update_contribution(contrib)

        self.publications = []
        self.rate = None
        self.__publications_to_considerate_sum = None

        self.accepted_publications = []
        self.__accepted_pubs_contrib_sum = 0
        self.__accepted_mons_contrib_sum = 0

    def __str__(self):
        return f"{self.id} {self.is_emp} {self.is_phd} {self.contribution} {self.in_n}"

    def __eq__(self, other):
        return (
            self.id == other.id
            and self.is_phd == other.is_phd
            and self.is_emp == other.is_emp
            and self.contribution == other.contribution
            and self.in_n == other.in_n
            and compare_lists(self.publications, other.publications)
        )

    def __check_if_publication_is_on_publications_list(self, pub: Publication):
        if pub not in self.publications:
            raise AttributeError(f"Publication {pub} not in publications list")

    def __update_contribution(contribution: float):
        if contribution < MIN_CONTRIBUTION:
            return MIN_CONTRIBUTION
        elif contribution > MAX_CONTRIBUTION:
            return MAX_CONTRIBUTION
        else:
            return contribution

    def get_contribution(self):
        return self.contribution

    def get_id(self):
        return self.id

    def get_publications(self):
        self.__check_if_publications_are_loaded()
        return self.publications

    def get_publications_number(self):
        return len(self.publications)

    def get_rate(self):
        self.__check_if_rate_is_set()
        return self.rate

    def is_phd_student(self):
        return self.is_phd

    def is_employee(self):
        return self.is_emp

    def is_in_n(self):
        return self.in_n

    def set_rate(self, new_rate: float):
        self.rate = new_rate

    def load_publications(self, publications) -> None:
        # TODO: reset
        result = []
        for pub in publications:
            if pub.get_points() > 0 and pub.get_contribution() > 0:
                pub.set_author(self)
                result.append(pub)

        publications_to_accept = list(filter(lambda x: x.is_accepted(), result))
        self.publications = result

        for pub in publications_to_accept:
            if not self.accept_publication(pub):
                pub.set_is_accepted(False)

    def get_pubs_to_considerate(self):
        pubs = list(
            filter(lambda x: x not in self.accepted_publications, self.publications)
        )
        return pubs

    def get_accepted_publications(self):
        return self.accepted_publications

    def __check_limits(self, pub: Publication) -> bool:
        if self.is_emp:
            if not self.__check_publications_limit(pub):
                return False
            if not self.__check_moographs_limit(pub):
                return False
        if not self.__check_limits_for_phd_students(pub):
            return False
        return True

    def __check_moographs_limit(self, pub: Publication) -> bool:
        tmp_mons_contrib = self.__accepted_mons_contrib_sum + pub.get_contribution()
        if self.is_phd:
            return True
        elif not pub.is_monograph():
            return True
        elif tmp_mons_contrib <= MONOGRAPH_COEFFICIENT * self.contribution:
            return True
        elif pub.get_points() > MONOGRAPH_LIMIT_MAX_POINTS:
            return True
        return False

    def __check_publications_limit(self, pub: Publication) -> bool:
        tmp_contrib = self.__accepted_pubs_contrib_sum + pub.get_contribution()
        return tmp_contrib <= PUBLICATIONS_COEFFICIENT * self.contribution

    def __check_limits_for_phd_students(self, pub: Publication) -> bool:
        tmp_contrib = self.__accepted_pubs_contrib_sum + pub.get_contribution()
        if not self.is_phd:
            return True
        elif tmp_contrib <= PUBLICATIONS_COEFFICIENT_FOR_PHD:
            return True
        return False

    def accept_publication(self, pub: Publication) -> bool:
        self.__check_if_publication_is_on_publications_list(pub)
        if pub not in self.accepted_publications and self.__check_limits(pub):
            self.accepted_publications.append(pub)
            pub.set_is_accepted(True)
            self.__accepted_pubs_contrib_sum += pub.get_contribution()
            if pub.is_monograph():
                self.__accepted_mons_contrib_sum += pub.get_contribution()
            return True
        return False

    def remove_from_accepted_publications(self, pub) -> None:
        pub.set_is_accepted(False)
        self.__accepted_pubs_contrib_sum -= pub.get_contribution()
        if pub.is_monograph():
            self.__accepted_mons_contrib_sum -= pub.get_contribution()
        self.accepted_publications.remove(pub)
