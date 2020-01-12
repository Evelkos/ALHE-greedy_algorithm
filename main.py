import os
from typing import List

from src.greedy.data_loader import load_data
from src.greedy.data_preparation import get_initial_publications, normalize_data
from src.greedy.greedy import run_algorithm
from src.greedy.output_converter import (
    convert_dictionary_to_vector,
    convert_publications_to_dictionary,
)
from src.greedy.publication import Publication
from src.greedy.settings import (
    DIGITAL_VARIABLES,
    DIRPATH,
    FILEPATH,
    HEURISTIC_RESULT_PUBS_LEN,
    INITIAL_PUBS,
    LIST_VARIABLES,
    NESTED_LIST_VARIABLES,
    PUBLICATIONS_NUM,
    STRING_LIST_VARIIABLES,
    RESULTS_DIR,
)


def get_result_path(input_path: str, mode: int, idx: int, test_try: int, results_dir: str) -> str:
    path = input_path.split("/")
    filename = path[len(path) - 1].split(("-"))[0]
    single_test_dir = os.path.join(results_dir, filename)

    if not os.path.exists(single_test_dir):
        os.mkdir(single_test_dir)

    return os.path.join(single_test_dir, f"{filename}_{mode}_{idx}_{test_try}.txt")

def get_list_of_input_files_from_dir(dirpath: str):
    files = []
    for file in os.listdir(dirpath):
        if file.endswith(".txt"):
            files.append(os.path.join(dirpath, file))
    return files


def save_results(path: str, data: dir, goal: float, vec: List[List[int]]) -> None:
    with open(path, "w") as f:
        tmp_goals = data["threshold_goal_values"]
        for threshold in tmp_goals:
            f.write(f"threshold_{threshold} = {tmp_goals[threshold]};")
            f.write("\n")
        f.write("\n")
        f.write(f"final_goal_function = {goal};")
        f.write("\n")
        f.write("\n")
        f.write(f"vector = {vec};")


def test_algorithm(
    mode: int,
    auth_pubs_num: int,
    number_of_tests: int,
    test_try: int,
    data: dict,
    filepath: str,
    results_dir: str
):
    """
    0 - empty publications list
    1 - full publications list
    2 - first auth_pubs_num publications from sorted publications list
    3 - first auth_pubs_num publications from shuffled publications list
    """
    max_goal = 0
    for test_num in range(number_of_tests):
        data[INITIAL_PUBS] = get_initial_publications(mode, data, auth_pubs_num)
        data["goal_calculations_num"] = 0
        data["threshold_goal_values"] = {}
        data["best_result"] = {"res_pubs": [], "goal_fun": 0}
        heuristic_len = int(data[PUBLICATIONS_NUM] * HEURISTIC_RESULT_PUBS_LEN)
        publications, goal_function = run_algorithm(data, heuristic_len)
        result_publications = convert_publications_to_dictionary(publications)
        result_vector = convert_dictionary_to_vector(result_publications, data)
        max_goal = max(max_goal, goal_function)
        path = get_result_path(filepath, mode, test_num, test_try, RESULTS_DIR)
        save_results(path, data, goal_function, result_vector)
    return max_goal


if __name__ == "__main__":
    # files = get_list_of_input_files_from_dir(DIRPATH)
    files = [FILEPATH]

    for filepath in files:
        print(filepath)

        try:
            with open(filepath, "r") as file:
                data = file.read()

            source_data = normalize_data(
                load_data(
                    data,
                    DIGITAL_VARIABLES,
                    LIST_VARIABLES,
                    NESTED_LIST_VARIABLES,
                    STRING_LIST_VARIIABLES,
                )
            )

            val = test_algorithm(0, 2, 28, 0, source_data.copy(), filepath, RESULTS_DIR)
            print(f"0: 1/1: {val}")
            val = test_algorithm(1, 2, 28, 0, source_data.copy(), filepath, RESULTS_DIR)
            print(f"1: 1/1: {val}")
            val = test_algorithm(2, 2, 28, 0, source_data.copy(), filepath, RESULTS_DIR)
            print(f"2: 1/1: {val}")
            for i in range(25):
                val = test_algorithm(3, 2, 28, i, source_data.copy(), filepath, RESULTS_DIR)
                print(f"3: {i + 1}/25: {val}")
            print()
            print()

        except Exception as e:
            print(e)
            continue
