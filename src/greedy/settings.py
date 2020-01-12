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


# Additional key in data directory: included publications
INITIAL_PUBS = "included_publications"

# number of full iterations after which results will be stored
THRESHOLDS = [1, 10, 100, 1000]

# probability of publication's revocation
ALPHA = 0.5

# Heuristic coefficient
# length of result publications = HEURISTIC_RESULT_PUBS_LEN * length of publications
HEURISTIC_RESULT_PUBS_LEN = 0.8

# Path to the file with input data (for tests)
FILEPATH = "data/filozofia-input.txt"

# Path to the directory with input files
DIRPATH = "data/results/data/"

# Path to the directory where results will be stored
RESULTS_DIR = "data/results"
