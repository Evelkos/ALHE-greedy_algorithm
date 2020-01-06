from typing import List, Tuple

from src.greedy.author import Author
from src.greedy.check_limits import (
    check_author_limits,
    check_limits,
    count_curr_sums_for_publications,
)
from src.greedy.data_loader import load_data
from src.greedy.data_preparation import (
    prepare_authors_and_their_publications,
    set_rate_for_authors,
    sort_authors,
)
from src.greedy.publication import Publication as Pub
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


def consider_single_publication(pub: Pub, curr_sums: dict, data: dict) -> bool:
    """
    Checks if publication will be accepted and checks limits.

    Args:
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
    if pub.get_author().is_phd_student() or not pub.get_author().is_employee():
        phd_out_modif = pub.get_contribution()

    tmp_sums = {
        "contrib_sum": curr_sums["contrib_sum"] + pub.get_contribution(),
        "monograph_sum": curr_sums["monograph_sum"] + mono_modif,
        "phd_and_outsiders": curr_sums["phd_and_outsiders"] + phd_out_modif,
    }
    return check_limits(data, tmp_sums)


def update_current_sums(curr_sums: dict, pub: Pub, auth: Author) -> dict:
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


def get_publications_to_considerate(authors: List[Author]) -> List[Pub]:
    """
    Returns list of publications that are not included in author's accepted
    publications lists.

    Args:
        authors: list of authors

    Returns:
        list of publications to considerate

    """
    publications = []
    for author in authors:
        publications += author.get_pubs_to_considerate()
    return publications


def sort_publications(publications: List[Pub]) -> List[Pub]:
    """
    Sorts publications by their rate and points.

    Args:
        publications: list of publications

    Returns:
        sorted list

    """
    return sorted(
        publications, key=lambda x: (x.get_rate(), x.get_points()), reverse=True
    )


def get_heuristic_value(pubs: List[Pub], idx: int, remaining_pubs: int) -> float:
    """
    Counts points for remaining publications. Heuristic function

    Args:
        pubs: list of publications to considerate
        idx: index of currently analysed publication
        remaining_pubs: heuristic number of publications to publish

    Returns:
        Heuristic value that represents points that will be added to goal function
        from remaining publications

    """
    heur = 0
    curr_pubs = 0
    for pub in pubs[idx:]:
        if curr_pubs >= remaining_pubs:
            break
        heur += pub.get_points()
    return heur


def choose_publications_to_publish(
    pubs: List[Pub], authors: List[Author], data: dict, heur_pubs: int
) -> Tuple[List[Pub], float]:
    """
    Chooses publications to publish

    Args:
        pubs: sorted list of publications to considerate
        authors: list of authors. Each author contains list of publications
        data: dictionary with data from input file
        heur_pubs: heuristic number of publications to publish

    Returns:
        list of publications to publish and value of goal function

    """
    publications_to_publish = []
    curr_sums = {"contrib_sum": 0, "monograph_sum": 0, "phd_and_outsiders": 0}
    goal_function = 0

    result_publications = []

    for auth in authors:
        for pub in auth.get_accepted_publications():
            if consider_single_publication(pub, curr_sums, data):
                curr_sums = update_current_sums(curr_sums, pub, pub.get_author())
                goal_function += pub.get_points()
                result_publications.append(pub)
                heur_pubs -= 1

    for idx, pub in enumerate(pubs, 0):
        if consider_single_publication(pub, curr_sums, data):
            heu_pub = get_heuristic_value(pubs, idx + 1, heur_pubs - 1)
            heu_without_pub = get_heuristic_value(pubs, idx + 1, heur_pubs)
            tmp_goal_function = goal_function + pub.get_points()

            if tmp_goal_function + heu_pub > goal_function + heu_without_pub:
                if pub.get_author().accept_publication(pub):
                    goal_function = tmp_goal_function
                    curr_sums = update_current_sums(curr_sums, pub, pub.get_author())
                    result_publications.append(pub)

    return result_publications, goal_function


def run_algorithm(data: dict, heur_pubs: int) -> Tuple[List[Pub], float]:
    """
    Runs full greedy algorithm. Prepares authors and publications, attaches
    publications to authors. Chooses which publications needs to be published

    Args:
        data: contains normalized data from input file
        heur_pubs: heuristic number of publications to publish

    Retrns:
        list of publications to publish and value of goal function

    """

    auths = prepare_authors_and_their_publications(data)
    pubs = sort_publications(get_publications_to_considerate(auths))
    res_pubs, goal_fun = choose_publications_to_publish(pubs, auths, data, heur_pubs)
    curr_sums = count_curr_sums_for_publications(res_pubs)

    assert check_limits(data, curr_sums)
    for author in auths:
        assert check_author_limits(author, author.get_accepted_publications())

    return res_pubs, goal_fun
