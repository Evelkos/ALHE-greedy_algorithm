from src.greedy.greedy import run_algorithm, load_data
from src.greedy.settings import FILEPATH, DIRPATH, DIGITAL_VARIABLES, LIST_VARIABLES, NESTED_LIST_VARIABLES, STRING_LIST_VARIIABLES, INITIAL_PUBS
from src.greedy.output_converter import convert_dictionary_to_vector
from src.greedy.publication import Publication
from src.greedy.data_preparation import normalize_data, get_initial_publications
from typing import List
import os
import json


def get_result_path(input_path: str):
    path = input_path.split("/")
    filename = path[len(path) - 1].split(("-"))[0]
    path[len(path) - 1] = "results"
    path.append(f"{filename}.txt")

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


if __name__ == "__main__":
    # files = get_list_of_input_files_from_dir(DIRPATH)
    files = [FILEPATH]

    for filepath in files:
        best_h = 0
        best_goal = 0


        for i in range(40, 41):
        # try:
            if not os.path.isfile(filepath):
                raise FileNotFoundError(f"Datafile {filepath} not found")

            with open(filepath, "r") as file:
                data = file.read()

            data = load_data(
                data,
                DIGITAL_VARIABLES,
                LIST_VARIABLES,
                NESTED_LIST_VARIABLES,
                STRING_LIST_VARIIABLES,
            )
            data = normalize_data(data)
            mode = 3
            auth_pubs_num = 2
            data[INITIAL_PUBS] = get_initial_publications(mode, data, auth_pubs_num)

            publications, goal_function = run_algorithm(data, i)
            result_publications = convert_publications_to_dictionary(publications)
            result = {
                "publications": result_publications,
                "goal_function": goal_function,
            }
            print(goal_function)

        #     result_vector = convert_dictionary_to_vector(result_publications, data)

        #     path = get_result_path(filepath)

        #     print(goal_function)
        #     # if(goal_function > best_goal):
        #     #     best_goal = goal_function
        #     #     best_h = i
        #     #     with open(path, "w") as file:
        #     #         file.write(f"vector = {result_vector};")
        #     #         file.write("\n")
        #     #         file.write("\n")
        #     #         file.write(f"goal_function = {goal_function};")

        #         # best_goal = goal_function
        #         # best_h = i
        #     # with open(path, "a") as file:
        #     #     file.write(f"heuristic_publications_number = {i}")
        #     #     file.write("\n")
        #     #     file.write(f"goal_function = {goal_function};")
        #     #     file.write("\n")
        #     #     file.write("\n")

        # # except Exception as e:
        # #     print(e)
        # #     continue
