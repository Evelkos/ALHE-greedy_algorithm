from src.greedy.publication import Publication

PUBLICATION_ID = "XXX"
IS_MONO = True
POINTS = 100.0
CONTRIBUTION = 0.5


def create_example_publication():
    return Publication(PUBLICATION_ID, IS_MONO, POINTS, CONTRIBUTION)


def test_publication__init():
    publication = Publication(PUBLICATION_ID, IS_MONO, POINTS, CONTRIBUTION)
    assert publication.id == PUBLICATION_ID
    assert publication.is_mono == IS_MONO
    assert publication.points == POINTS
    assert publication.contribution == CONTRIBUTION


def test_is_monograph():
    assert create_example_publication().is_monograph() == IS_MONO


def test_is_monograph():
    assert create_example_publication().get_contribution() == CONTRIBUTION


def test_get_id():
    assert create_example_publication().get_id() == PUBLICATION_ID


def test_get_points():
    assert create_example_publication().get_points() == POINTS


def test_get_rate():
    assert create_example_publication().get_rate() == POINTS / CONTRIBUTION
