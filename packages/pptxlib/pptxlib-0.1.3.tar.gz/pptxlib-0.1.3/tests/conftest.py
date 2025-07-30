import pytest

from pptxlib.core.app import App
from pptxlib.core.presentation import Presentation, Presentations
from pptxlib.core.slide import Slide, Slides


@pytest.fixture(scope="session")
def app():
    with App() as app:
        yield app


@pytest.fixture(scope="session")
def prs(app: App):
    prs = app.presentations
    yield prs
    prs.close()


@pytest.fixture
def pr(prs: Presentations):
    pr = prs.add()
    yield pr
    pr.close()


@pytest.fixture
def slides(pr: Presentation):
    return pr.slides


@pytest.fixture
def slide(slides: Slides):
    slide = slides.add()
    yield slide
    slide.delete()


@pytest.fixture
def shapes(slide: Slide):
    return slide.shapes
