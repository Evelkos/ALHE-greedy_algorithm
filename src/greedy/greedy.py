from src.greedy.data_loader import load_data
from src.greedy.data_preparation import (
    prepare_authors_and_their_publications,
    sort_authors,
    set_rate_for_authors,
)
from src.greedy.settings import (
    DIGITAL_VARIABLES,
    EMPLOYEES_NUM,
    FILEPATH,
    HEURISTIC_AUTHORS_LIST_LEN,
    LIST_VARIABLES,
    N0,
    N1,
    N2,
    NESTED_LIST_VARIABLES,
    STRING_LIST_VARIIABLES,
)
from src.greedy.check_limits import check_limits, count_curr_sums_for_publications
from typing import List
from src.greedy.author import Author


def count_approximated_pubs_rate(authors):
    rate = 0
    for idx, auth in enumerate(authors):
        if idx < HEURISTIC_AUTHORS_LIST_LEN:
            rate += auth.get_sum_of_publications_to_considerate()
    return rate


def consider_single_publication(auth, pub, curr_sums, data):
    mono_modif = 0
    phd_out_modif = 0
    if pub.is_monograph():
        mono_modif = pub.get_contribution()
    if auth.is_phd_student() or not auth.is_employee():
        phd_out_modif = pub.get_contribution()

    tmp_sums = {
        "contrib_sum": curr_sums["contrib_sum"] + pub.get_contribution(),
        "monograpth_sum": curr_sums["monograpth_sum"] + mono_modif,
        "phd_and_outsiders": curr_sums["phd_and_outsiders"] + phd_out_modif,
    }
    return check_limits(data, tmp_sums)


def get_points_from_auth_below(authors, idx):
    if len(authors) > HEURISTIC_AUTHORS_LIST_LEN + idx:
        return authors[HEURISTIC_AUTHORS_LIST_LEN + idx].get_average_pub_points()
    return 0


def update_current_sums(curr_sums, pub, auth):
    monograph_sum = curr_sums["monograpth_sum"]
    phd_and_outsiders = curr_sums["phd_and_outsiders"]

    if pub.is_monograph():
        monograph_sum += pub.get_contribution()
    if auth.is_phd_student() or not auth.is_in_n():
        phd_and_outsiders += pub.get_contribution()

    result = {
        "contrib_sum": curr_sums["contrib_sum"] + pub.get_contribution(),
        "monograpth_sum": monograph_sum,
        "phd_and_outsiders": phd_and_outsiders,
    }
    return result


def choose_final_publications(authors: List[Author], data: dict):
    result = []
    curr_sums = {"contrib_sum": 0, "monograpth_sum": 0, "phd_and_outsiders": 0}
    heuristic_function = count_approximated_pubs_rate(authors)
    goal_function = 0

    for idx, author in enumerate(authors, 0):
        for pub in author.get_publications_to_considerate():
            if consider_single_publication(author, pub, curr_sums, data):
                heu_pub = heuristic_function - pub.get_points()
                heu_without_pub = heu_pub + get_points_from_auth_below(authors, idx)
                tmp_goal_function = goal_function + pub.get_points()

                if goal_function + heu_without_pub > tmp_goal_function + heu_pub:
                    heuristic_function = heu_without_pub
                else:
                    goal_function = tmp_goal_function
                    heuristic_function = heu_pub
                    curr_sums = update_current_sums(curr_sums, pub, author)
                    result.append(pub)
    return result


def run_algorithm(data_from_file: str):
    data = load_data(
        data_from_file,
        DIGITAL_VARIABLES,
        LIST_VARIABLES,
        NESTED_LIST_VARIABLES,
        STRING_LIST_VARIIABLES,
    )
    authors = prepare_authors_and_their_publications(data)
    set_rate_for_authors(authors)
    authors = sort_authors(authors)
    publications = choose_final_publications(authors, data)
    assert check_limits(data, count_curr_sums_for_publications(publications))
    return publications
