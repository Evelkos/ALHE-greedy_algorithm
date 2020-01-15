from src.greedy.author import (
    BASIC_CONTRIB_COEFFICIENT,
    MAX_CONTRIBUTION,
    MIN_CONTRIBUTION,
    MONOGRAPH_COEFFICIENT,
    MONOGRAPH_LIMIT_MAX_POINTS,
    PUBLICATIONS_COEFFICIENT,
    PUBLICATIONS_COEFFICIENT_FOR_PHD,
    Author,
)
from src.greedy.publication import Publication
from src.greedy.tools import compare_lists

IS_EMP = True
IS_PHD = False
CONTRIB = 0.5
CZYN = 1
IN_N = 1
AUTH_ID = "WEITI-e85bc237-d711-46c7-b31e-e4c991c79392"


def count_publications_rates_sum(publications):
    result = 0
    for pub in publications:
        result += pub.get_points()
    return result


def create_example_publications_list():
    publications = [
        Publication("1", False, 100.0, 0.5),
        Publication("2", False, 50.0, 1.0),
        Publication("3", False, 10.0, 1.0),
    ]
    return publications


def create_complex_publications_list():
    pubs = ["0", "1", "2", "3", "4", "5", "6", "7", "8", "9"]
    mons = [True, True, True, False, True, False, False, False, True, True]
    points = [100.0, 10.0, 90.0, 20.0, 80.0, 30.0, 70.0, 40.0, 60.0, 50.0]
    contribs = [1.0, 0.0, 0.5, 1.0, 0.0, 0.5, 1.0, 0.0, 0.5, 1.0]
    publications = []
    for pub_id, is_mono, pts, contrib in zip(pubs, mons, points, contribs):
        publications.append(Publication(pub_id, is_mono, pts, contrib))
    return publications


def create_example_author(
    a_id: str = AUTH_ID,
    is_emp: bool = IS_EMP,
    is_phd: bool = IS_PHD,
    contrib: float = CONTRIB,
    in_n: bool = IN_N,
):
    return Author(a_id, is_emp, is_phd, contrib, in_n)


def create_example_publication(
    publication_id: str = "id",
    is_mono: bool = False,
    points: float = 10.0,
    contrib: float = 0.1,
    author: Author = None,
    accepted: bool = False,
):
    return Publication(publication_id, is_mono, points, contrib, author, accepted)


def prepare_complex_test_data():
    publications = create_complex_publications_list()
    author = Author("author", True, False, 0.5, 1)
    author.load_publications(publications)
    author.create_publications_ranking()
    return author, publications


def prepare_data_for_check_mono_limit_test():
    """
    Prepares data that fails _Author__check_moographs_limit() test

    """
    is_phd = False
    is_emp = False
    is_mon = True
    tmp_sum = MONOGRAPH_COEFFICIENT * CONTRIB + 1.0
    points = MONOGRAPH_LIMIT_MAX_POINTS / 2

    author = Author(AUTH_ID, is_emp, is_phd, CONTRIB, CZYN)

    return author, is_mon, tmp_sum, points


def test__check_if_publication_is_on_publications_list():
    a = create_example_author()
    p = create_example_publication()
    a.publications = [p]
    assert a._Author__check_if_publication_is_on_publications_list(p) is None


def test_update_contribution():
    value = (MAX_CONTRIBUTION + MIN_CONTRIBUTION) / 2
    assert Author._Author__update_contribution(value) == value


def test_update_contribution_with_value_greater_than_MAX_CONTRIBUTION():
    value = MAX_CONTRIBUTION + 0.1
    assert Author._Author__update_contribution(value) == MAX_CONTRIBUTION


def test_update_contribution_with_value_smaller_than_MIN_CONTRIBUTION():
    value = MIN_CONTRIBUTION - 0.1
    assert Author._Author__update_contribution(value) == MIN_CONTRIBUTION


def test_get_contribution():
    auth = create_example_author()
    assert auth.get_contribution() == auth.contribution


def test_get_id():
    auth = create_example_author(a_id="xyz")
    assert auth.get_id() == "xyz"


def test_get_publications_number():
    a = create_example_author()
    pubs = [create_example_publication() for _ in range(5)]
    a.publications = pubs
    assert a.get_publications_number() == 5


def test_is_phd_student():
    assert create_example_author(is_phd=True).is_phd_student()
    assert not create_example_author(is_phd=False).is_phd_student()


def test_is_employee():
    assert create_example_author(is_emp=True).is_employee()
    assert not create_example_author(is_emp=False).is_employee()


def test_is_in_n():
    assert create_example_author(in_n=True).is_in_n()
    assert not create_example_author(in_n=False).is_in_n()


def test_load_publications():
    a = create_example_author(contrib=1.0)
    pubs = [
        create_example_publication(publication_id="1", contrib=0.5),
        create_example_publication(publication_id="2", contrib=69.0),
        create_example_publication(publication_id="3", contrib=1.0),
    ]
    a.load_publications(pubs)

    assert compare_lists(a.publications, pubs)


def test_load_publications_with_accepted_publications():
    a = create_example_author(contrib=1.0)
    pubs = [
        create_example_publication(publication_id="1", contrib=0.5, accepted=True),
        create_example_publication(publication_id="2", contrib=69.0),
        create_example_publication(publication_id="3", contrib=1.0),
    ]
    a.load_publications(pubs)

    assert compare_lists(a.publications, pubs)
    assert compare_lists(a.accepted_publications, [pubs[0]])


def test_load_publications_with_publication_with_too_big_contrib_accepted():
    a = create_example_author(contrib=1.0)
    ctb = PUBLICATIONS_COEFFICIENT * a.get_contribution() + 1
    pubs = [
        create_example_publication(publication_id="1", contrib=0.5),
        create_example_publication(publication_id="2", contrib=ctb, accepted=True),
        create_example_publication(publication_id="3", contrib=1.0),
    ]
    a.load_publications(pubs)

    assert compare_lists(a.publications, pubs)
    assert compare_lists(a.accepted_publications, [])


def test_get_pubs_to_considerate():
    a = create_example_author(contrib=1.0)
    pubs = [
        create_example_publication(publication_id="1", contrib=0.5, accepted=True),
        create_example_publication(publication_id="2", contrib=69.0),
        create_example_publication(publication_id="3", contrib=1.0),
    ]
    a.load_publications(pubs)

    assert compare_lists(a.get_pubs_to_considerate(), pubs[1:])


def test_get_accepted_publications():
    a = create_example_author()
    pubs = [create_example_publication(publication_id=str(i)) for i in range(5)]
    a.accepted_publications = pubs
    assert compare_lists(a.get_accepted_publications(), pubs)


def test_check_full_limits():
    a = create_example_author()
    p = create_example_publication(contrib=BASIC_CONTRIB_COEFFICIENT)
    assert a._Author__check_limits(p)


def test_check_full_limits_with_too_big_contrib():
    a = create_example_author()
    p = create_example_publication(contrib=BASIC_CONTRIB_COEFFICIENT + 1)
    assert not a._Author__check_limits(p)


def test_check_limits():
    a = create_example_author()
    p = create_example_publication(contrib=a.get_contribution() / 2)
    assert a._Author__check_full_limits(p)


def test_check_moographs_limit_with_too_big_contribution():
    a = create_example_author()
    p = create_example_publication(contrib=a.get_contribution() + 1, is_mono=True)
    assert not a._Author__check_moographs_limit(p)


def test_check_moographs_limit_when_author_is_an_phd():
    a = create_example_author(is_phd=True)
    p = create_example_publication(contrib=a.get_contribution() + 1, is_mono=True)
    assert a._Author__check_moographs_limit(p)


def test_check_moographs_limit_when_publication_is_not_a_monograph():
    a = create_example_author()
    p = create_example_publication(contrib=a.get_contribution() + 1, is_mono=False)
    assert a._Author__check_moographs_limit(p)


def test_check_moographs_limit_with_valuable_monograph():
    a = create_example_author()
    contrib = a.get_contribution() + 1
    points = MONOGRAPH_LIMIT_MAX_POINTS + 1
    p = create_example_publication(contrib=contrib, is_mono=True, points=points)
    assert a._Author__check_moographs_limit(p)


def test_check_publications_limit_with_standard_contributions_sum():
    a = create_example_author()
    p = create_example_publication(contrib=a.get_contribution() / 2, is_mono=True)
    assert a._Author__check_moographs_limit(p)


def test_check_publications_limit_with_max_contributions_sum():
    a = create_example_author(is_phd=False)
    contrib = a.get_contribution() * PUBLICATIONS_COEFFICIENT
    p = create_example_publication(contrib=contrib)
    assert a._Author__check_publications_limit(p)


def test_check_publications_limit_with_too_big_contributions_sum():
    a = create_example_author(is_phd=False)
    contrib = a.get_contribution() * PUBLICATIONS_COEFFICIENT + 1
    p = create_example_publication(contrib=contrib)
    assert not a._Author__check_publications_limit(p)


def test_check_limits_for_phd_students_with_standard_value():
    a = create_example_author(is_phd=True)
    p = create_example_publication(contrib=PUBLICATIONS_COEFFICIENT_FOR_PHD / 2)
    assert a._Author__check_limits_for_phd_students(p)


def test_check_limits_for_phd_students_with_max_tmp_contrib_sum():
    a = create_example_author(is_phd=True)
    p = create_example_publication(contrib=PUBLICATIONS_COEFFICIENT_FOR_PHD)
    assert a._Author__check_limits_for_phd_students(p)


def test_check_limits_for_phd_students_with_too_big_tmp_contrib_sum():
    a = create_example_author(is_phd=True)
    p = create_example_publication(contrib=PUBLICATIONS_COEFFICIENT_FOR_PHD + 1)
    assert not a._Author__check_limits_for_phd_students(p)


def test_check_limits_for_phd_students_when_author_is_not_phd():
    a = create_example_author(is_phd=False)
    p = create_example_publication(contrib=PUBLICATIONS_COEFFICIENT_FOR_PHD + 1)
    assert a._Author__check_limits_for_phd_students(p)


def test_accept_publication():
    a = create_example_author(contrib=4.0)
    pubs = [create_example_publication(publication_id=i, contrib=1) for i in range(3)]
    a.load_publications(pubs)
    for pub in a.publications:
        assert a.accept_publication(pub)
    assert compare_lists(a.accepted_publications, pubs)


def test_accept_publication_with_multiple_publications():
    a = create_example_author(contrib=4.0)
    contrib = BASIC_CONTRIB_COEFFICIENT * 69
    pubs = [
        create_example_publication(publication_id="1", contrib=0.01),
        create_example_publication(publication_id="2", contrib=contrib),
        create_example_publication(publication_id="3", contrib=0.01),
    ]
    a.load_publications(pubs)
    assert a.accept_publication(pubs[0])
    assert not a.accept_publication(pubs[1])
    assert a.accept_publication(pubs[2])

    assert compare_lists(a.accepted_publications, [pubs[0], pubs[2]])


def test_remove_from_accepted_publications():
    a = create_example_author(contrib=4.0)
    pubs = [create_example_publication(publication_id=i, contrib=1) for i in range(3)]
    a.load_publications(pubs)
    a.accepted_publications = pubs
    for idx, pub in enumerate(pubs, 1):
        a.remove_from_accepted_publications(pub)
        assert len(a.publications) == 3
        assert len(a.accepted_publications) == 3 - idx
