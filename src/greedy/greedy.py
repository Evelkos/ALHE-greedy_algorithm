from greedy.data_loader import load_data
from greedy.data_preparation import prepare_authors_and_their_publications, sort_authors
from greedy.settings import (
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


def check_publications_number_limit(data, tmp_contrib_sum: float) -> bool:
    return (
        tmp_contrib_sum
        < 3 * data[EMPLOYEES_NUM] - 3 * data[N0] - 6 * data[N1] - 6 * data[N2]
    )


def check_monographs_number_limit(data, tmp_monograpth_sum: float) -> bool:
    return tmp_monograpth_sum < 0.15 * data[EMPLOYEES_NUM]


def check_phd_students_and_outsiders(data, tmp_phd_and_outsiders) -> bool:
    return tmp_phd_and_outsiders < 0.6 * data[EMPLOYEES_NUM]


def check_limits(data, tmp_sums):
    if not check_publications_number_limit(data, tmp_sums["contrib_sum"]):
        return False
    if not check_monographs_number_limit(data, tmp_sums["monograpth_sum"]):
        return False
    if not check_phd_students_and_outsiders(data, tmp_sums["phd_and_outsiders"]):
        return False
    return True


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


def get_pub_points_from_author_below(authors, idx):
    if len(authors) > HEURISTIC_AUTHORS_LIST_LEN + idx:
        return authors[HEURISTIC_AUTHORS_LIST_LEN + idx].get_average_pub_points()
    return 0


def update_current_sums(curr_sums, pub, auth):
    monograph_sum = curr_sums["monograpth_sum"]
    phd_and_outsiders = curr_sums["phd_and_outsiders"]

    if pub.is_monograph():
        monograph_sum += pub.get_contribution()
    if auth.is_phd_student() or not auth.is_employee():
        phd_and_outsiders += pub.get_contribution()

    result = {
        "contrib_sum": curr_sums["contrib_sum"] + pub.get_contribution(),
        "monograpth_sum": monograph_sum,
        "phd_and_outsiders": phd_and_outsiders,
    }
    return result


def choose_final_publications(authors, data):
    result = []
    curr_sums = {"contrib_sum": 0, "monograpth_sum": 0, "phd_and_outsiders": 0}

    final_publications = []
    current_contrib_sum = 0
    goal_function = 0
    heuristic_function = count_approximated_pubs_rate(authors)

    points = 0
    all_authors_contrib_sum = 0

    di = 0
    for auth in authors:
        di += auth.get_contribution()

    i = 0
    for idx, auth in enumerate(authors):
        auth_contrib_sum = 0
        for pub in auth.get_publications_to_considerate():
            # Count tmp_goal_function
            if consider_single_publication(auth, pub, curr_sums, data):
                tmp_points = points + pub.get_points()
                tmp_auth_contrib_sum = auth_contrib_sum + pub.get_contribution()
                tmp_all_authors_contrib_sum = (
                    all_authors_contrib_sum + pub.get_contribution()
                )
                pub_modif = 0
                all_pub_modif = 0
                if tmp_auth_contrib_sum - 4 * auth.get_contribution() > 0:
                    pub_modif += -250 * pub.get_contribution()
                if tmp_all_authors_contrib_sum - 3 * di > 0:
                    all_pub_modif = -250 * pub.get_contribution()

                tmp_goal_function = tmp_points + pub_modif + all_pub_modif

                # Count tmp heuristic functions
                heuristic_if_pub_added = heuristic_function - pub.get_points()
                heuristic_if_pub_not_added = (
                    heuristic_if_pub_added
                    + get_pub_points_from_author_below(authors, idx)
                )

                # Update values
                if (
                    goal_function + heuristic_if_pub_not_added
                    > tmp_goal_function + heuristic_if_pub_added
                ):
                    heuristic_function = heuristic_if_pub_not_added
                else:
                    goal_function = tmp_goal_function
                    points = tmp_points
                    auth_contrib_sum = tmp_auth_contrib_sum
                    all_authors_contrib_sum = tmp_all_authors_contrib_sum
                    heuristic_function = heuristic_if_pub_added
                    curr_sums = update_current_sums(curr_sums, pub, auth)

                    final_publications.append(pub)
    return final_publications


def run_algorithm(data_from_file: str):
    data = load_data(
        data_from_file,
        DIGITAL_VARIABLES,
        LIST_VARIABLES,
        NESTED_LIST_VARIABLES,
        STRING_LIST_VARIIABLES,
    )
    authors = sort_authors(prepare_authors_and_their_publications(data))
    approximated_pubs_rate = count_approximated_pubs_rate(authors)
    publications = choose_final_publications(authors, data)
    print(publications)
