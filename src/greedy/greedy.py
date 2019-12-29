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
from typing import List, Tuple
from src.greedy.author import Author
from src.greedy.publication import Publication


def count_approximated_pubs_rate(authors: List[Author]) -> float:
    """
    Counts first value of heuristic function.

    Args:
        authors: list of authors

    Returns:
        firs value of heuristic function

    """
    rate = 0
    for idx, auth in enumerate(authors):
        if idx < HEURISTIC_AUTHORS_LIST_LEN:
            rate += auth.get_sum_of_publications_to_considerate()
    return rate


def consider_single_publication(auth: Author, pub: Publication, curr_sums: dict, data: dict) -> bool:
    """
    Assumes that publication will be accepted and checks limits.

    Args:
        auth: publication's author
        pub: publication
        curr_sums: dictionary with sums needed to decide if publication meets the
            limits. Keys:
            contrib_sum: sum of contributions from all accepted publicatons (float)
            monograph_sum: sum of contributions from all accepted monographs (float)
            phd_and_outsiders: sum of contributions from all accepted phds' and
                outsiders' publicatons (float)
        data: dictionary with data from file

    Returns:
        True if publication meets the limits. Otherwise returns False

    """
    mono_modif = 0
    phd_out_modif = 0
    if pub.is_monograph():
        mono_modif = pub.get_contribution()
    if auth.is_phd_student() or not auth.is_employee():
        phd_out_modif = pub.get_contribution()

    tmp_sums = {
        "contrib_sum": curr_sums["contrib_sum"] + pub.get_contribution(),
        "monograph_sum": curr_sums["monograph_sum"] + mono_modif,
        "phd_and_outsiders": curr_sums["phd_and_outsiders"] + phd_out_modif,
    }
    return check_limits(data, tmp_sums)


def get_points_from_auth_below(authors: List[Author], idx: int) -> float:
    """
    Gets average publication's points from author with smaller rate value than
    author currently analysed in choose_publications_to_publish().

    Args:
        authors: list of authors
        idx: idx of currently analysed author

    Returns:
        average publication's points from author with smaller rate value

    """
    if len(authors) > HEURISTIC_AUTHORS_LIST_LEN + idx:
        return authors[HEURISTIC_AUTHORS_LIST_LEN + idx].get_average_pub_points()
    return 0


def update_current_sums(curr_sums: dict, pub: Publication, auth: Author) -> dict:
    """
    Updates temporary values needed to run greedy algorithm. Instead of recount
    values in every loop iteration, we simply update them.

    Args:
        curr_sums: dictionary with values to update
            contrib_sum: sum of contributions from all accepted publicatons (float)
            monograph_sum: sum of contributions from all accepted monographs (float)
            phd_and_outsiders: sum of contributions from all accepted phds' and
                outsiders' publicatons (float)
        pub: newly accepted publication
        auth: publication's author

    Returns:
        dictionary with updated values

    """
    monograph_sum = curr_sums["monograph_sum"]
    phd_and_outsiders = curr_sums["phd_and_outsiders"]

    if pub.is_monograph():
        monograph_sum += pub.get_contribution()
    if auth.is_phd_student() or not auth.is_in_n():
        phd_and_outsiders += pub.get_contribution()

    result = {
        "contrib_sum": curr_sums["contrib_sum"] + pub.get_contribution(),
        "monograph_sum": monograph_sum,
        "phd_and_outsiders": phd_and_outsiders,
    }
    return result


def choose_publications_to_publish(authors: List[Author], data: dict) -> Tuple[List[Publication], float]:
    """
    Chooses publications to publish

    Args:
        authors: list of authors. Each author contains list of publications
        data: dictionary that contains data loaded from file with load_dada()

    Returns:
        list of publications to publish and value of goal function

    """
    publications_to_publish = []
    curr_sums = {"contrib_sum": 0, "monograph_sum": 0, "phd_and_outsiders": 0}
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
                    publications_to_publish.append(pub)
    return publications_to_publish, goal_function


def run_algorithm(data_from_file: str) -> Tuple[List[Publication], float]:
    """
    Runs full greedy algorithm. Loads data from given string, prepares authors and
    publications, attaches publications to authors. When all data is loaded
    publications to publish are choosen and checked.

    Args:
        data_from_file: contains data from file

    Retrns:
        list of publications to publish and value of goal function

    """
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
    publications, goal_function = choose_publications_to_publish(authors, data)
    assert check_limits(data, count_curr_sums_for_publications(publications))
    return publications, goal_function
