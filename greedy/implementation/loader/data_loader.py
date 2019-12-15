from os.path import isfile
from typing import List, Any
import re


DIGITAL_VARIABLES = ["A", "N0", "N1", "N2", "P"]
STANDARD_LIST_VARIABLES = ["udzial", "doktorant", "pracownik", "czyN", "monografia"]


def get_float_pattern() -> str:
    return r"\[((\d+|, |\d+\.\d+)+)\]"


def extract_int_variables(data: str, digital_variables: List[str]) -> dict:
    """
    Returns dictionary with variables listed in digital_variables. Variables needs to
    be stored in data string.

    Args:
        data: string to extract data from
        digital_variables: names of variables to extract from data

    Returns:
        Dictionary with variables and their values.

    Examples:
    >>> extract_int_variables("A = 12;", ["A"])
    {"A": 12}

    """
    return {var: find_int(data, var) for var in digital_variables}


def extract_list_variables(data: str, list_variables: List[str]) -> dict:
    """
    Returns dictionary with variables listed in digital_variables. Variables needs to
    be stored in data string.

    Args:
        data: string to extract data from
        list_variables: names of variables to extract from data

    Returns:
        Dictionary with variables and their values.

    Examples:
    >>> extract_int_variables("A = [12, 13];", ["A"])
    {"A": [12, 13]}

    """
    return {var: find_list(data, var, get_float_pattern()) for var in list_variables}


def find_int(data: str, variable_name: str) -> int:
    """
    Finds int variable in given string and returns its value

    Args:
        data: string to extract data from
        variable_name: name of variable located in file

    Returns:
        Value of variable with name variable_name

    Examples:
    >>> find_int("A = 12;", "A")
    12
    >>> find_int("N0 = 1;", "N0")
    1

    """
    pattern = re.escape(variable_name) + r" = ((\d)+);"
    match = re.search(pattern, data)
    if not match:
        raise ValueError(f"Variable {variable_name} not found in given string")
    return int(match.group(1))


def find_list(data: str, variable_name: str, element_pattern: str) -> List[Any]:
    """
    Finds list with float elements

    Args:
        data: string to extract data from
        variable_name: name of variable located in file

    Returns:
        Value of variable with name variable_name

    """
    pattern = re.escape(variable_name) + r" = " + element_pattern + r";"
    match = re.search(pattern, data)
    if not match:
        raise ValueError(f"Variable {variable_name} not found in given string")
    return [float(var) for var in match.group(1).split(", ")]


def load_data(path: str):
    if not isfile(path):
        raise FileNotFoundError(f"Datafile {path} not found")

    with open(path, "r") as file:
        data = file.read()
        print(extract_int_variables(data, DIGITAL_VARIABLES))
        print(extract_list_variables(data, STANDARD_LIST_VARIABLES))
