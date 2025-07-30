from __future__ import annotations

from pptxlib.core.app import App


def main():
    app = App()
    app.presentations.close()
    pr = app.presentations.add()
    slides = pr.slides
    slide = slides.add()
    s1 = slide.shapes.add("Rectangle", 100, 100, 100, 100)
    s2 = slide.shapes.add("Oval", 140, 300, 40, 80)
    s1.connect(s2).line.set(3, "red").begin_arrow("Open").end_arrow("Stealth")

    line = slide.shapes.add_line(100, 200, 300, 400).line
    line.set(3, "red").dash()
    line.begin_arrowhead_style = "Open"

    # api.Line.Weight = weight
    # api.Line.ForeColor.RGB = rgb(color)

    # if begin_style is True:
    #     begin_style = constants.msoArrowheadOpen
    # elif isinstance(begin_style, str):
    #     begin_style = hasattr(constants, "msoArrowhead" + begin_style)
    # if begin_style is not False or begin_style is not None:
    #     api.Line.BeginArrowheadStyle = begin_style

    # if end_style is True:
    #     end_style = constants.msoArrowheadOpen
    # elif isinstance(end_style, str):
    #     end_style = hasattr(constants, "msoArrowhead" + end_style)
    # if end_style is not False or end_style is not None:
    #     api.Line.EndArrowheadStyle = end_style


if __name__ == "__main__":
    main()
