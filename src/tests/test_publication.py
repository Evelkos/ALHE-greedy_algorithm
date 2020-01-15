from src.greedy.publication import Publication
from src.tests.test_author import create_example_author, create_example_publication

PUBLICATION_ID = "XXX"
IS_MONO = True
POINTS = 100.0
CONTRIBUTION = 0.5


# def create_example_publication():
#     return Publication(PUBLICATION_ID, IS_MONO, POINTS, CONTRIBUTION)


def test_publication__init():
    publication = Publication(PUBLICATION_ID, IS_MONO, POINTS, CONTRIBUTION)
    assert publication.id == PUBLICATION_ID
    assert publication.is_mono == IS_MONO
    assert publication.points == POINTS
    assert publication.contribution == CONTRIBUTION


def test_is_accepted_with_true():
    assert create_example_publication(accepted=True).is_accepted()


def test_is_accepted_with_false():
    assert not create_example_publication(accepted=False).is_accepted()


def test_is_monograph_with_true():
    assert create_example_publication(is_mono=True).is_monograph()


def test_is_monograph_with_false():
    assert not create_example_publication(is_mono=False).is_monograph()


def test_get_author():
    a = create_example_author()
    p = create_example_publication(author=a)
    assert p.get_author() == a


def test_get_contribution():
    assert create_example_publication(contrib=2.0).get_contribution() == 2.0


def test_get_id():
    assert create_example_publication(publication_id="xxx").get_id() == "xxx"


def test_get_points():
    assert create_example_publication(points=69.0).get_points() == 69.0


def test_get_rate():
    assert create_example_publication(points=100.0, contrib=2.0).get_rate() == 50.0


def test_set_author():
    a = create_example_author()
    p = create_example_publication()
    assert p.get_author() is None
    p.set_author(a)
    assert p.get_author() == a


def test_set_is_accepted_with_value_unchanged():
    p = create_example_publication(accepted=False)
    p.set_is_accepted(False)
    assert not p.is_accepted()

    p = create_example_publication(accepted=True)
    p.set_is_accepted(True)
    assert p.is_accepted()


def test_set_is_accepted_with_false_base():
    p = create_example_publication(accepted=False)
    p.set_is_accepted(True)
    assert p.is_accepted()


def test_set_is_accepted_with_truth_base():
    p = create_example_publication(accepted=True)
    p.set_is_accepted(False)
    assert not p.is_accepted()
