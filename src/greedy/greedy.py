from greedy.data_loader import load_data
from greedy.data_preparation import (
    prepare_authors_and_publications,
    sort_authors,
)
from greedy.settings import (
    DIGITAL_VARIABLES,
    FILEPATH,
    HEURISTIC_AUTHORS_LIST_LEN,
    LIST_VARIABLES,
    NESTED_LIST_VARIABLES,
    STRING_LIST_VARIIABLES,
)


def count_approximated_pubs_rate(authors):
    rate = 0
    for idx, auth in enumerate(authors):
        if idx < HEURISTIC_AUTHORS_LIST_LEN:
            rate += auth.get_rate()
    return rate


def run_algorithm():
    data = load_data(
        FILEPATH,
        DIGITAL_VARIABLES,
        LIST_VARIABLES,
        NESTED_LIST_VARIABLES,
        STRING_LIST_VARIIABLES,
    )
    authors = sort_authors(prepare_authors_and_publications(data))
    print(count_approximated_pubs_rate(authors))
