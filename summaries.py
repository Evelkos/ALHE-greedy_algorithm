from src.greedy.settings import (
    PLOT_DATA,
    THRESHOLDS_SUFFIX,
    RESULTS_IMAGES_DIR,
    SUMMARIES_FILE,
    FINAL_GOAL_FUN,
)
from src.greedy.tools import get_list_of_files_from_dir
from src.greedy.data_loader import load_data
import os
import re
import matplotlib.pyplot as plt
from typing import List
import pandas as pd
import seaborn as sns


def find_thresholds_names(input_data: str) -> List[str]:
    pattern = THRESHOLDS_SUFFIX + r"[0-9]+"
    return re.findall(pattern, input_data)


def find_threshold(threshold_name: str) -> int:
    return int(re.search(r"[0-9]+", threshold_name).group())


def get_filename(filepath: str) -> str:
    return filepath.split("/")[-1]


def make_plot(name: str, x: List[int], y: List[float], result_dir: str) -> str:
    df = pd.DataFrame({"thresholds": x, "points": y})
    path = os.path.join(RESULTS_IMAGES_DIR, f"{name}.png")

    g = sns.catplot(x="thresholds", y="points", jitter=False, data=df)
    plt.title(f"Publications' points for {name}")
    plt.subplots_adjust(top=0.90)
    plt.savefig(path)

    return path


def save_best_result(filepath: str, file_with_max_goal: str, max_goal: float) -> None:
    with open(filepath, "a") as file:
        file.write(f"file = {file_with_max_goal}")
        file.write("\n")
        file.write(f"max_goal = {max_goal}")
        file.write("\n")
        file.write("\n")


def find_best_goal_function_in_files(filenames):
    max_goal = 0
    file_with_max_goal = None

    for filename in filenames:
        with open(filename, "r") as file:
            source_data = file.read()

        data = load_data(source_data, [FINAL_GOAL_FUN])

        if max_goal < data[FINAL_GOAL_FUN]:
            max_goal = data[FINAL_GOAL_FUN]
            file_with_max_goal = filename

    return max_goal, file_with_max_goal


def get_points_and_thresholds(filenames):
    x = []
    y = []

    for filename in filenames:
        with open(filename, "r") as file:
            source_data = file.read()

        thresholds_names = find_thresholds_names(source_data)
        data = load_data(source_data, thresholds_names)

        for threshold in thresholds_names:
            x.append(find_threshold(threshold))
            y.append(data[threshold])
    return x, y


if __name__ == "__main__":
    files_in_results_dir = get_list_of_files_from_dir(PLOT_DATA, "")
    result_dirs = filter(lambda x: os.path.isdir(x), files_in_results_dir)
    result_dirs = list(filter(lambda x: not x == "data/results/final", result_dirs))

    if os.path.exists(SUMMARIES_FILE):
        os.remove(SUMMARIES_FILE)

    for single_result_dir in result_dirs:
        filenames = get_list_of_files_from_dir(single_result_dir, ".txt")
        x, y = get_points_and_thresholds(filenames)
        max_goal, file_with_max_goal = find_best_goal_function_in_files(filenames)

        make_plot(get_filename(single_result_dir), x, y, RESULTS_IMAGES_DIR)
        save_best_result(SUMMARIES_FILE, file_with_max_goal, max_goal)
