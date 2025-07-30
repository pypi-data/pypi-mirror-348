from __future__ import annotations

from pptxlib.core.app import App


def main():
    app = App()
    app.presentations.close()
    pr = app.presentations.add()
    slide = pr.slides.add()

    s = slide.shapes.add("Rectangle", 100, 100, 100, 100)
    s.text = "abc"
    s.font.set("Times New Roman", 16, True, True, "red")
    s.fill.set(color="red", alpha=0.5)
    s.line.set(color="blue", weight=5, alpha=0.5)

    table = slide.shapes.add_table(2, 3, 100, 250, 100, 100)
    table.fill("red", alpha=0.5)
    table.columns[1].fill("blue", alpha=0.5)
    table.rows.height = [40, 40]
    for i in range(4):
        table[0].borders[i].set(color="red", weight=5, alpha=0.5)
    table[1, 1].borders[0].set(color="red", weight=5, alpha=0.5)
    table.columns.borders["bottom"].set(color="green", weight=5, alpha=0.5)
    table[1].borders["left"].set(color="green", weight=5, alpha=0.5)

    c = table[0, 0]
    c.text = "abc"
    for c in table.columns:
        c.width = 100

    s.select()
    # table.fill("red", (0, 0), (1, 2))
    # print(table[0, 0].shape.api.Fill.Transparency)
    # table[0, 0].shape.api.Fill.Transparency = 1


if __name__ == "__main__":
    main()
