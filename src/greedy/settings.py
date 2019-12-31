# Variables from datafile
EMPLOYEES_NUM = "A"
N0 = "N0"
N1 = "N1"
N2 = "N2"
PUBLICATIONS_NUM = "P"

# Standard lists from datafile
AUTHOR_ID = "authorIdList"
PUBLICATION_ID = "publicationIdList"
IS_MONOGRAPH = "monografia"
CONTRIBUTION = "udzial"
IS_PHD_STUDENT = "doktorant"
IS_EMPLOYEE = "pracownik"
IS_IN_N = "czyN"

# Nested lists from datafile
PUBLICATION_POINTS_FOR_AUTHOR = "w"
PUBLICATION_CONTRIB_FOR_AUTHOR = "u"


DIGITAL_VARIABLES = [EMPLOYEES_NUM, N0, N1, N2, PUBLICATIONS_NUM]
LIST_VARIABLES = [CONTRIBUTION, IS_PHD_STUDENT, IS_EMPLOYEE, IS_IN_N, IS_MONOGRAPH]
NESTED_LIST_VARIABLES = [PUBLICATION_CONTRIB_FOR_AUTHOR, PUBLICATION_POINTS_FOR_AUTHOR]
STRING_LIST_VARIIABLES = [AUTHOR_ID, PUBLICATION_ID]

# Path to the file with data
# inzynieria_biomedyczna-input.txt - BLAD
FILEPATH = "/home/ewelina/Studia/Semestr 7/ALHE/Projekt/ALHE-greedy_algorithm/data/filozofia-input.txt"
DIRPATH = "/home/ewelina/Studia/Semestr 7/ALHE/Projekt/ALHE-greedy_algorithm/data/"

HEURISTIC_AUTHORS_LIST_LEN = 5
