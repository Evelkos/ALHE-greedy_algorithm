from src.greedy.settings import (
    RESULTS_DIR,
    THRESHOLDS_SUFFIX,
    RESULTS_IMAGES_DIR,
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


if __name__ == "__main__":
    files_in_results_dir = get_list_of_files_from_dir(RESULTS_DIR, "")
    result_dirs = filter(lambda x: os.path.isdir(x), files_in_results_dir)
    result_dirs = list(filter(lambda x: not x == "data/results/final", result_dirs))

    for single_result_dir in result_dirs:
        filenames = get_list_of_files_from_dir(single_result_dir, ".txt")
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

        name = get_filename(single_result_dir)
        df = pd.DataFrame({"thresholds": x, "points": y})
        g = sns.catplot(x="thresholds", y="points", jitter=False, data=df)
        plt.title(f"Publications' points for {name}")
        plt.subplots_adjust(top=0.90)
        plt.savefig(os.path.join(RESULTS_IMAGES_DIR, f"{name}.png"))