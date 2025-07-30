from __future__ import annotations

from pathlib import Path

from pptxlib.core.app import App


def main():
    app = App()
    app.presentations.close()
    pr = app.presentations.add().size(400, 300)

    slide = pr.slides.add()
    shapes = slide.shapes
    shapes.add("Rectangle", 100, 100, 100, 100)
    shapes.add("Oval", 150, 150, 90, 80)
    slide.export(Path(__file__).parent / "a.png")


if __name__ == "__main__":
    main()
