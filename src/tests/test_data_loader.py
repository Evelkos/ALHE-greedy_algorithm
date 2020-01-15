from src.greedy.data_loader import (
    extract_vars,
    find_data_segment,
    get_float_pattern,
    get_list_of_floats_pattern,
    get_list_of_strings_pattern,
    get_nested_list_pattern,
    load_data,
)


def test_find_data_segment_with_int_pattern():
    assert find_data_segment("A = 123;", "A", get_float_pattern()) == "123"


def test_find_data_segment_with_int_pattern_and_multiple_variables():
    assert find_data_segment("A = 88; B = 9;", "B", get_float_pattern()) == "9"


def test_find_data_segment_with_list_of_floats_pattern():
    pattern = get_list_of_floats_pattern()
    assert find_data_segment("A = [9, 8];", "A", pattern) == "[9, 8]"


def test_find_data_segment_with_list_of_floats_pattern_and_multiple_variables():
    pattern = get_list_of_floats_pattern()
    assert find_data_segment("A = [1]; B = [2, 3];", "B", pattern) == "[2, 3]"


def test_find_data_segment_with_list_of_strings_pattern():
    data = 'A = ["xyz", "zyx"];'
    pattern = get_list_of_strings_pattern()
    assert find_data_segment(data, "A", pattern) == '["xyz", "zyx"]'


def test_find_data_segment_with_list_of_strings_pattern_with_multiple_variables():
    data = 'A = ["b", "a"]; BB = ["z", "zz", "zzz"];'
    pattern = get_list_of_strings_pattern()
    assert find_data_segment(data, "BB", pattern) == '["z", "zz", "zzz"]'


def test_find_data_segment_with_nested_list_pattern():
    data = "Z = [[1, 1, 0], [0, 0, 1]];"
    pattern = get_nested_list_pattern()
    assert find_data_segment(data, "Z", pattern) == "[[1, 1, 0], [0, 0, 1]]"


def test_find_data_segment_with_nested_list_pattern_and_multiple_variables():
    data = "A = [3]; X = [[0, 1, 0], [0, 0, 1]];"
    pattern = get_nested_list_pattern()
    assert find_data_segment(data, "X", pattern) == "[[0, 1, 0], [0, 0, 1]]"


def test_extract_vars_with_int_pattern():
    assert extract_vars("A = 12;", ["A"], get_float_pattern()) == {"A": 12}


def test_extract_vars_with_list_of_floats_pattern():
    data = "ABC = [1.1, 2.2, 3.3];"
    pattern = get_list_of_floats_pattern()
    assert extract_vars(data, ["ABC"], pattern) == {"ABC": [1.1, 2.2, 3.3]}


def test_extract_vars_with_list_of_strings_pattern():
    data = 'S = ["abc", "def"];'
    pattern = get_list_of_strings_pattern()
    assert extract_vars(data, ["S"], pattern) == {"S": ["abc", "def"]}


def test_extract_vars_with_nested_list_pattern():
    data = "G = [[1], [2]];"
    pattern = get_nested_list_pattern()
    assert extract_vars(data, ["G"], pattern) == {"G": [[1], [2]]}


def test_extract_vars_with_multiple_variables():
    data = "A = 6; B = 5; C = 4;"
    pattern = get_float_pattern()
    assert extract_vars(data, ["A", "B"], pattern) == {"A": 6, "B": 5}


def test_load_data_with_int_variable():
    data = "A = 3;"
    assert load_data(data, ["A"]) == {"A": 3}


def test_load_data_with_float_list_variable():
    data = "B = [0.5, 1.0, 1.0];"
    assert load_data(data, None, ["B"]) == {"B": [0.5, 1.0, 1.0]}


def test_load_data_with_nested_list_variable():
    data = "F = [[0.1, 0.2]];"
    assert load_data(data, None, None, ["F"]) == {"F": [[0.1, 0.2]]}


def test_load_data_with_string_list_variable():
    data = 'G = ["aaa", "bbb"];'
    assert load_data(data, None, None, None, ["G"]) == {"G": ["aaa", "bbb"]}


def test_load_data_with_multiple_variables():
    data = "A = 3; B = [0.5, 1.0, 1.0];"
    assert load_data(data, ["A"], ["B"]) == {"A": 3, "B": [0.5, 1.0, 1.0]}
