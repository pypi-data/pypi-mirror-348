import pytest


def test_rgb_invalid_format():
    from pptxlib.core.color import rgb

    with pytest.raises(ValueError):
        rgb("invalid")


def test_rgb_invalid_type():
    from pptxlib.core.color import rgb

    with pytest.raises(ValueError):
        rgb(None)  # type: ignore
