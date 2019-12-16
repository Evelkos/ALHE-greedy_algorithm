from implementation.sorter import run_greedy
from implementation.loader.data_loader import load_data

FILEPATH = "/tmp/ALHE-greedy_algorithm/data/filozofia-input.txt"
DIGITAL_VARIABLES = ["A", "N0", "N1", "N2", "P"]
LIST_VARIABLES = ["udzial", "doktorant", "pracownik", "czyN", "monografia"]
NESTED_LIST_VARIABLES = ["u", "w"]
STRING_LIST_VARIIABLES = ["authorIdList", "publicationIdList"]


if __name__ == "__main__":
    data = load_data(
        FILEPATH,
        DIGITAL_VARIABLES,
        LIST_VARIABLES,
        NESTED_LIST_VARIABLES,
        STRING_LIST_VARIIABLES,
    )

    run_greedy(data)
