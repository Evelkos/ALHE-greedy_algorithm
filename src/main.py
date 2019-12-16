from greedy.greedy import run_algorithm
from greedy.settings import FILEPATH
from os.path import isfile

if __name__ == "__main__":
    if not isfile(FILEPATH):
        raise FileNotFoundError(f"Datafile {FILEPATH} not found")

    with open(FILEPATH, "r") as file:
        data = file.read()
    run_algorithm(data)
