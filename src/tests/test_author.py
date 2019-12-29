import pytest

from src.greedy.author import (
    MAX_CONTRIBUTION,
    MIN_CONTRIBUTION,
    MONOGRAPH_COEFFICIENT,
    MONOGRAPH_LIMIT_MAX_POINTS,
    PUBLICATIONS_COEFFICIENT,
    PUBLICATIONS_COEFFICIENT_FOR_PHD,
    Author,
)
from src.greedy.check_limits import check_author_limits
from src.greedy.publication import Publication

IS_EMP = True
IS_PHD = False
CONTRIB = 0.5
CZYN = 1
AUTH_ID = "WEITI-e85bc237-d711-46c7-b31e-e4c991c79392"


def count_publications_rates_sum(publications):
    result = 0
    for pub in publications:
        result += pub.get_rate()
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


def create_example_author():
    return Author(AUTH_ID, IS_EMP, IS_PHD, CONTRIB, CZYN)


def prepare_basic_test_data():
    """
    Creates author and publications then adds publications to author "to_considerate"
    list.

    Returns:
    author, list of publications and sum of rates for all publications

    """
    author = create_example_author()
    publications = create_example_publications_list()
    pubs_rates_sum = count_publications_rates_sum(publications)
    author.to_considerate = publications

    return author, publications, pubs_rates_sum


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


def test_check_moographs_limit_with_data_prepared_for_test():
    auth, is_mon, tmp_sum, points = prepare_data_for_check_mono_limit_test()
    assert not auth._Author__check_moographs_limit(tmp_sum, is_mon, points)


def test_check_moographs_limit_when_author_is_an_phd():
    auth, is_mon, tmp_sum, points = prepare_data_for_check_mono_limit_test()
    auth.is_phd = True
    assert auth._Author__check_moographs_limit(tmp_sum, is_mon, points)


def test_check_moographs_limit_when_publication_is_not_a_monograph():
    auth, is_mon, tmp_sum, points = prepare_data_for_check_mono_limit_test()
    is_mon = False
    assert auth._Author__check_moographs_limit(tmp_sum, is_mon, points)


def test_check_moographs_limit_with_appropiate_tmp_contrib_monograph_sum():
    auth, is_mon, tmp_sum, points = prepare_data_for_check_mono_limit_test()
    tmp_sum = MONOGRAPH_COEFFICIENT * auth.get_contribution()
    assert auth._Author__check_moographs_limit(tmp_sum, is_mon, points)


def test_check_moographs_limit_with_valuable_monograph():
    auth, is_mon, tmp_sum, points = prepare_data_for_check_mono_limit_test()
    points = MONOGRAPH_LIMIT_MAX_POINTS + 0.1
    assert auth._Author__check_moographs_limit(tmp_sum, is_mon, points)


def test_check_publications_limit_with_standard_contributions_sum():
    author = Author(AUTH_ID, IS_EMP, False, CONTRIB, CZYN)
    value = PUBLICATIONS_COEFFICIENT * author.get_contribution() / 2
    assert author._Author__check_publications_limit(value)


def test_check_publications_limit_with_max_contributions_sum():
    author = Author(AUTH_ID, IS_EMP, False, CONTRIB, CZYN)
    value = PUBLICATIONS_COEFFICIENT * author.get_contribution()
    assert author._Author__check_publications_limit(value)


def test_check_publications_limit_with_too_big_contributions_sum():
    author = Author(AUTH_ID, IS_EMP, False, CONTRIB, CZYN)
    value = PUBLICATIONS_COEFFICIENT * author.get_contribution() + 0.1
    assert not author._Author__check_publications_limit(value)


def test_check_limits_for_phd_students_with_standard_value():
    author = Author(AUTH_ID, IS_EMP, True, CONTRIB, CZYN)
    value = PUBLICATIONS_COEFFICIENT_FOR_PHD / 2
    assert author._Author__check_limits_for_phd_students(value)


def test_check_limits_for_phd_students_with_max_tmp_contrib_sum():
    author = Author(AUTH_ID, IS_EMP, True, CONTRIB, CZYN)
    value = PUBLICATIONS_COEFFICIENT_FOR_PHD
    assert author._Author__check_limits_for_phd_students(value)


def test_check_limits_for_phd_students_with_too_big_tmp_contrib_sum():
    author = Author(AUTH_ID, IS_EMP, True, CONTRIB, CZYN)
    value = PUBLICATIONS_COEFFICIENT_FOR_PHD + 1
    assert not author._Author__check_limits_for_phd_students(value)


def test_check_limits_for_phd_students_when_author_is_not_phd():
    author = Author(AUTH_ID, IS_EMP, False, CONTRIB, CZYN)
    value = PUBLICATIONS_COEFFICIENT_FOR_PHD * 10
    assert author._Author__check_limits_for_phd_students(value)


def test_choose_best_publications():
    author, pubs = prepare_complex_test_data()
    pubs = filter(lambda x: x.get_contribution() > 0 and x.get_points() > 0, pubs)
    pubs = list(pubs)
    pubs = sorted(pubs, key=lambda pub: pub.get_rate(), reverse=True)

    result = author._Author__choose_best_publications(pubs)
    check_author_limits(author, result)


def test_get_sorted_publications():
    author, publications, _ = prepare_basic_test_data()
    author.load_publications(publications)
    pubs = sorted(publications, key=lambda pub: pub.get_rate(), reverse=True)
    assert author._Author__get_sorted_publications() == pubs


def test_update_contribution():
    value = (MAX_CONTRIBUTION + MIN_CONTRIBUTION) / 2
    assert Author._Author__update_contribution(value) == value


def test_update_contribution_with_value_greater_than_MAX_CONTRIBUTION():
    value = MAX_CONTRIBUTION + 0.1
    assert Author._Author__update_contribution(value) == MAX_CONTRIBUTION


def test_update_contribution_with_value_smaller_than_MIN_CONTRIBUTION():
    value = MIN_CONTRIBUTION - 0.1
    assert Author._Author__update_contribution(value) == MIN_CONTRIBUTION


def test_count_sum_of_publications_to_considerate():
    author, publications, pubs_rates_sum = prepare_basic_test_data()
    assert author.count_sum_of_publications_to_considerate() == pubs_rates_sum


def test_count_sum_of_publications_to_considerate_without_loaded_publications():
    with pytest.raises(AttributeError):
        create_example_author().count_sum_of_publications_to_considerate()


def test_create_publications_ranking():
    author = create_example_author()
    publications = [
        Publication("1", False, 50.0, 1.0),
        Publication("2", False, 100.0, 0.5),
        Publication("3", False, 10.0, 0.5),
    ]
    author.load_publications(publications)
    assert len(author.create_publications_ranking()) == len(publications)
    assert author.to_considerate[0] == publications[1]
    assert author.to_considerate[1] == publications[0]
    assert author.to_considerate[2] == publications[2]


def test_create_publications_ranking_without_loaded_publications():
    with pytest.raises(AttributeError):
        create_example_author().create_publications_ranking()


def test_get_contribution():
    assert create_example_author().get_contribution() == CONTRIB


def test_get_publications():
    author, publications, _ = prepare_basic_test_data()
    author.publications = publications
    assert author.get_publications() == publications


def test_get_publications_without_loaded_publications():
    with pytest.raises(AttributeError):
        create_example_author().get_publications()


def test_get_publications_to_considerate():
    author, publications, _ = prepare_basic_test_data()
    assert author.get_publications_to_considerate() == publications


def test_get_number_of_publications_to_considerate():
    author = create_example_author()
    author.to_considerate = [Publication("6", False, 10.0, 0.5)]
    assert author.get_number_of_publications_to_considerate() == 1


def test_get_number_of_publications_to_considerate_with_no_pubs_to_considerate():
    with pytest.raises(AttributeError):
        create_example_author().get_number_of_publications_to_considerate()


def test_get_sum_of_publications_to_considerate():
    author, _, pubs_rates_sum = prepare_basic_test_data()
    assert author.get_sum_of_publications_to_considerate() == pubs_rates_sum


def test_get_sum_of_publications_to_considerate_with_existing_result():
    author, _, _ = prepare_basic_test_data()
    author.get_sum_of_publications_to_considerate()

    new_pubs = [Publication("x", False, 999.0, 1.0)]
    author.to_considerate = new_pubs
    new_pubs_rates_sum = count_publications_rates_sum(new_pubs)

    assert author.get_sum_of_publications_to_considerate() != new_pubs_rates_sum


def test_get_sum_of_publications_to_considerate_with_no_pubs_to_considerate():
    with pytest.raises(AttributeError):
        create_example_author().get_sum_of_publications_to_considerate()


def test_get_average_pub_points_with_nonempty_list_of_publications_to_considerate():
    author, publications, pubs_rates_sum = prepare_basic_test_data()
    assert author.get_average_pub_points() == pubs_rates_sum / len(publications)


def test_get_average_pub_points_with_empty_list_of_publications_to_considerate():
    author = create_example_author()
    author.to_considerate = []
    with pytest.raises(AttributeError):
        create_example_author().get_average_pub_points()


def test_get_average_pub_points_with_no_publications_to_considerate():
    with pytest.raises(AttributeError):
        create_example_author().get_average_pub_points()


def test_get_rate_when_rate_is_set():
    author = create_example_author()
    author.rate = 10.0
    assert author.get_rate() == 10.0


def test_get_rate_when_rate_not_set():
    author = create_example_author()
    with pytest.raises(AttributeError):
        author.get_rate()


def test_is_phd_student():
    assert create_example_author().is_phd_student() == IS_PHD


def test_is_employee():
    assert create_example_author().is_employee() == IS_EMP


def test_load_publications():
    author = create_example_author()
    publications = [
        Publication("1", False, 100.0, 0.0),
        Publication("2", False, 50.0, 0.5),
        Publication("3", False, 0.0, 1.0),
    ]
    author.load_publications(publications)

    assert len(author.publications) == 1
    assert author.publications[0].get_points() == 50.0


def test_set_rate():
    author = create_example_author()
    author.set_rate(951.0)
    assert author.rate == 951.0
