import pytest

from pptxlib.core.app import is_app_available
from pptxlib.core.presentation import Presentation, Presentations

pytestmark = pytest.mark.skipif(
    not is_app_available(),
    reason="PowerPoint is not available",
)


def test_repr_collection(prs: Presentations):
    assert repr(prs).startswith("<Presentations (")


@pytest.fixture(scope="module")
def pr(prs: Presentations):
    return prs.add()


def test_active(prs: Presentations, pr: Presentation):
    assert prs.active.name == pr.name


def test_getitem(prs: Presentations, pr: Presentation):
    assert prs[0].name == pr.name
    assert prs[-1].name == pr.name


def test_iter(prs: Presentations, pr: Presentation):
    assert next(iter(prs)).name == pr.name


def test_slides(pr: Presentation):
    assert len(pr.slides) == 0


def test_width(pr: Presentation):
    assert pr.width == 960
    assert pr.height == 540


def test_repr_element(pr: Presentation):
    assert repr(pr).startswith("<Presentation")


def test_name(pr: Presentation):
    name = pr.name
    pr.name = "abc"
    assert pr.name == "abc"
    pr.name = name
