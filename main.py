from src.greedy.greedy import run_algorithm
from src.greedy.data_loader import load_data
from src.greedy.settings import FILEPATH, DIRPATH, DIGITAL_VARIABLES, LIST_VARIABLES, NESTED_LIST_VARIABLES, STRING_LIST_VARIIABLES, INITIAL_PUBS, PUBLICATIONS_NUM
from src.greedy.output_converter import convert_dictionary_to_vector
from src.greedy.publication import Publication
from src.greedy.data_preparation import normalize_data, get_initial_publications
from typing import List
import os
import json
import numpy as np


def get_result_path(input_path: str, mode: int, idx: int, test_try: int) -> str:
    path = input_path.split("/")
    filename = path[len(path) - 1].split(("-"))[0]
    path[len(path) - 1] = "results"
    path.append(f"{filename}_{mode}_{idx}_{test_try}.txt")

    return f"/{os.path.join(*path)}"

def get_list_of_input_files_from_dir(dirpath: str):
    files = []
    for file in os.listdir(DIRPATH):
        if file.endswith(".txt"):
            files.append(os.path.join(DIRPATH, file))
    return files


def convert_publications_to_dictionary(publications: List[Publication]) -> dir:
    result_publications = {}
    for pub in publications:
        if not pub.get_id() in result_publications:
            result_publications.update({pub.get_id(): [pub.get_author().get_id()]})
        else:
            result_publications[pub.get_id()].append(pub.get_author().get_id())
    return result_publications


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


def test_algorithm(mode: int, auth_pubs_num: int, number_of_tests: int, test_try: int, data: dict, filepath: str):
    """
    0 - empty publications list
    1 - full publications list
    2 - first auth_pubs_num publications from sorted publications list
    3 - first auth_pubs_num publications from shuffled publications list
    """
    for test_num in range(number_of_tests):
        print(f"{mode}: {test_num}/{number_of_tests}")
        data[INITIAL_PUBS] = get_initial_publications(mode, data, auth_pubs_num)

        heuristic_len = int(data[PUBLICATIONS_NUM] * 0.7)

        publications, goal_function = run_algorithm(data, heuristic_len)
        result_publications = convert_publications_to_dictionary(publications)
        result_vector = convert_dictionary_to_vector(result_publications, data)

        path = get_result_path(filepath, mode, test_num, test_try)
        save_results(path, data, goal_function, result_vector)
    print()


if __name__ == "__main__":
    # files = get_list_of_input_files_from_dir(DIRPATH)
    files = [FILEPATH]

    for filepath in files:
        print(filepath)
        best_h = 0
        best_goal = 0
        best_pubs = []

        points = 0
        if not os.path.isfile(filepath):
            raise FileNotFoundError(f"Datafile {filepath} not found")

        with open(filepath, "r") as file:
            data = file.read()

        source_data = normalize_data(load_data(
            data,
            DIGITAL_VARIABLES,
            LIST_VARIABLES,
            NESTED_LIST_VARIABLES,
            STRING_LIST_VARIIABLES,
        ))

        data = source_data.copy()

        try:
            test_algorithm(0, 2, 28, 0, source_data.copy(), filepath)
            test_algorithm(1, 2, 28, 0, source_data.copy(), filepath)
            test_algorithm(2, 2, 28, 0, source_data.copy(), filepath)
            for i in range(25):
                test_algorithm(3, 2, 28, i, source_data.copy(), filepath)

        except Exception as e:
            print(e)
            continue
