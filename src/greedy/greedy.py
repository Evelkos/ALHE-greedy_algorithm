from typing import List, Tuple
import numpy as np

from src.greedy.author import Author
from src.greedy.check_limits import (
    check_author_limits,
    check_limits,
    count_curr_sums_for_publications,
)
from src.greedy.data_preparation import prepare_authors_and_their_publications
from src.greedy.publication import Publication as Pub
from src.greedy.data_preparation import shuffle_pubs


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


def get_all_accepted_publications(authors: List[Author]) -> List[Pub]:
    """
    Returns list of publications that are included in author's accepted
    publications lists.

    Args:
        authors: list of authors

    Returns:
        list of accepted publications

    """
    accepted = []
    for author in authors:
        accepted += author.get_accepted_publications()
    return accepted


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
        curr_pubs += 1

    return heur


def get_points_from_pub(pubs: List[Pub], idx: int) -> float:
    if len(pubs) > idx:
        return pubs[idx].get_points()
    return 0


def count_goal_function(prev_goal_fun: float, points: float, data: dict) -> float:
    update_iterations_info(data)
    return prev_goal_fun + points


def choose_publications_to_publish(
    pubs: List[Pub], accepted: List[Pub], data: dict, heur_pubs: int
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
    curr_sums = {"contrib_sum": 0, "monograph_sum": 0, "phd_and_outsiders": 0}
    goal_function = 0

    result_publications = []

    for pub in accepted:
        if consider_single_publication(pub, curr_sums, data):
            curr_sums = update_current_sums(curr_sums, pub, pub.get_author())
            goal_function += pub.get_points()
            result_publications.append(pub)
            heur_pubs -= 1

    heuristic_value = get_heuristic_value(pubs, 0, heur_pubs)

    for idx, pub in enumerate(pubs, 0):
        heuristic_value = round(heuristic_value, 3)
        if consider_single_publication(pub, curr_sums, data):
            heu_pub = heuristic_value - pub.get_points()
            heu_without_pub = heuristic_value - pub.get_points()
            if heur_pubs > 0:
                heu_without_pub += get_points_from_pub(pubs, idx + heur_pubs)

            heu_pub = heu_pub if heu_pub >= 0 else 0
            heu_without_pub = heu_without_pub if heu_without_pub >= 0 else 0
            tmp_goal_function = goal_function + pub.get_points()

            if tmp_goal_function + heu_pub > goal_function + heu_without_pub:
                if pub.get_author().accept_publication(pub):
                    goal_function = tmp_goal_function
                    heuristic_value = heu_pub
                    heur_pubs -= 1
                    curr_sums = update_current_sums(curr_sums, pub, pub.get_author())
                    result_publications.append(pub)
                else:
                    heuristic_value -= pub.get_points()
                    if heur_pubs > 0:
                        heuristic_value += get_points_from_pub(pubs, idx + heur_pubs)
            else:
                heuristic_value = heu_without_pub
        else:
            heuristic_value -= pub.get_points()
            if heur_pubs > 0:
                heuristic_value += get_points_from_pub(pubs, idx + heur_pubs)

    return result_publications, round(goal_function, 3)


def choose_publications_to_cancel(accepted: List[Pub], alpha: float) -> List[Pub]:
    pubs = sort_publications(accepted)

    to_cancel = []

    for idx, pub in enumerate(pubs, 1):
        cancel_prob = np.random.uniform(0, 1)
        threshold = alpha
        if cancel_prob <= threshold:
            to_cancel.append(pub)

    return to_cancel


def count_auth_pub_pairs_num(authors: List[Author]) -> int:
    """
    Counts number of pairs (author, publication),

    Args:
         authors: list of authors. Each author has a list of publications
    """
    auth_pub_pairs_num = 0
    for auth in authors:
        auth_pub_pairs_num += auth.get_publications_number()
    return auth_pub_pairs_num


def update_iterations_info(data: dict) -> None:
    goal_fun = data["best_result"]["goal_fun"]
    data["goal_calculations_num"] += 1
    if data["goal_calculations_num"] in data["thresholds"]:
        curr_th = data["goal_calculations_num"]
        if data["threshold_goal_values"] == {}:
            data["threshold_goal_values"][curr_th] = goal_fun
        else:
            max_th = max(data["threshold_goal_values"])
            if goal_fun > data["threshold_goal_values"][max_th]:
                data["threshold_goal_values"][curr_th] = goal_fun
            else:
                data["threshold_goal_values"][curr_th] = data["threshold_goal_values"][max_th]


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
    auth_pub_pairs_num = count_auth_pub_pairs_num(auths)
    data["goal_calculations_num"] = 0
    data["thresholds"] = [i * auth_pub_pairs_num for i in [1, 10, 100]]
    data["threshold_goal_values"] = {}

    data["best_result"] = {"res_pubs": [], "goal_fun": 0}

    alpha = 0.5
    while data["goal_calculations_num"] < max(data["thresholds"]):
        pubs = shuffle_pubs(get_publications_to_considerate(auths))
        acc = get_all_accepted_publications(auths)
        res_pubs, goal_fun = choose_publications_to_publish(pubs, acc, data, heur_pubs)

        if data["best_result"]["goal_fun"] < goal_fun:
            data["best_result"]["goal_fun"] = goal_fun
            data["best_result"]["res_pubs"] = res_pubs.copy()

        update_iterations_info(data)

        to_cancel = choose_publications_to_cancel(res_pubs, alpha)
        for pub in to_cancel:
            pub.get_author().remove_from_accepted_publications(pub)

    curr_sums = count_curr_sums_for_publications(data["best_result"]["res_pubs"])
    assert check_limits(data, curr_sums)
    for author in auths:
        assert check_author_limits(author, author.get_accepted_publications())

    return data["best_result"]["res_pubs"], data["best_result"]["goal_fun"]
