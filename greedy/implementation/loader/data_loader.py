import ast
import re
from os.path import isfile
from typing import Any, List


def get_int_pattern() -> str:
    return r"(\d+)"


def get_list_of_floats_pattern() -> str:
    return r"(\[(\d+|, |\d+\.\d+)+\])"


def get_nested_list_pattern() -> str:
    return r"(\[(\[|\]|\d+|\d+\.\d+|, )+\])"


def get_list_of_strings_pattern() -> str:
    return r"(\[(\"|\w|-|, )+\])"


def extract_vars(data: str, list_variables: List[str], pattern: str) -> dict:
    """
    Returns dictionary with variables listed in list_variables. Variables needs to
    be stored in data string.

    Args:
        data: string to extract data from
        list_variables: names of variables to extract from data

    Returns:
        Dictionary with variables and their values.

    """
    return {
        var: ast.literal_eval(find_data_segment(data, var, pattern))
        for var in list_variables
    }


def find_data_segment(data: str, variable_name: str, element_pattern: str) -> List[Any]:
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
    return match.group(1)


def load_data(
    path: str,
    digital_vars: List[str] = None,
    list_vars: List[str] = None,
    nested_list_vars: List[str] = None,
    string_list_vars: List[str] = None,
):
    if not isfile(path):
        raise FileNotFoundError(f"Datafile {path} not found")

    result = {}
    with open(path, "r") as file:
        data = file.read()
        if digital_vars:
            result.update(extract_vars(data, digital_vars, get_int_pattern()))
        if list_vars:
            result.update(extract_vars(data, list_vars, get_list_of_floats_pattern()))
        if nested_list_vars:
            result.update(
                extract_vars(data, nested_list_vars, get_nested_list_pattern())
            )
        if string_list_vars:
            result.update(
                extract_vars(data, string_list_vars, get_list_of_strings_pattern())
            )
    return result
