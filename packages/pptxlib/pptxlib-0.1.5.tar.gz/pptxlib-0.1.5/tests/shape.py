from __future__ import annotations

from pptxlib.core.app import App


def main():
    app = App()
    app.presentations.close()
    pr = app.presentations.add()
    shapes = pr.slides.add().shapes
    s1 = shapes.add("Rectangle", 100, 100, 100, 100)
    s2 = shapes.add("Oval", 150, 150, 90, 80)
    shapes.range([s1, s2])


if __name__ == "__main__":
    main()
