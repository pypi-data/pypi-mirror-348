from __future__ import annotations

import matplotlib.pyplot as plt

from pptxlib.core.app import App


def main():
    app = App()
    app.presentations.close()
    pr = app.presentations.add()
    slide = pr.slides.add()

    fig, ax = plt.subplots(figsize=(2, 1), dpi=300)
    ax.plot([1, 2, 3, 4, 5])
    s = slide.shapes.add_figure(fig)
    s.copy()
    s = slide.shapes.paste_special("GIF", 20, 100, 200, 300)


if __name__ == "__main__":
    main()
