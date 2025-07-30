from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from tempfile import NamedTemporaryFile
from typing import TYPE_CHECKING, ClassVar

from win32com.client import constants

from .base import Collection, Element
from .shape import Shapes

if TYPE_CHECKING:
    from .presentation import Presentation


@dataclass(repr=False)
class Slide(Element):
    parent: Presentation
    collection: Slides

    @property
    def shapes(self) -> Shapes:
        return Shapes(self.api.Shapes, self)

    @property
    def title(self) -> str:
        return self.shapes.title.text if len(self.shapes) else ""

    @title.setter
    def title(self, text: str) -> None:
        if len(self.shapes):
            self.shapes.title.text = text

    @property
    def width(self) -> float:
        return self.parent.width

    @property
    def height(self) -> float:
        return self.parent.height

    def export(self, file_name: str | Path, fmt: str | None = None) -> None:
        if fmt is None:
            fmt = Path(file_name).suffix[1:]
        self.api.Export(str(file_name), fmt.upper())

    def png(self) -> bytes:
        with NamedTemporaryFile(suffix=".png", delete=False) as file:
            file_name = Path(file.name)

        self.export(file_name)
        data = file_name.read_bytes()
        file_name.unlink()
        return data


@dataclass(repr=False)
class Slides(Collection[Slide]):
    parent: Presentation
    type: ClassVar[type[Element]] = Slide

    def add(self, index: int | None = None, layout: int | str | None = None) -> Slide:
        if index is None:
            index = len(self)

        if isinstance(layout, str):
            layout = getattr(constants, f"ppLayout{layout}")
        elif layout is None:
            title_only = constants.ppLayoutTitleOnly
            if index == 0:
                layout = title_only
            else:
                slide = self[index - 1]
                layout = getattr(slide.api, "CustomLayout", title_only)

        if isinstance(layout, int):
            slide = self.api.Add(index + 1, layout)
        else:
            slide = self.api.AddSlide(index + 1, layout)

        return Slide(slide, self.parent, self)

    @property
    def active(self) -> Slide:
        index = self.app.ActiveWindow.Selection.SlideRange.SlideIndex - 1
        return self[index]
