from __future__ import annotations

from dataclasses import dataclass
from typing import TYPE_CHECKING, ClassVar

from .base import Collection, Element
from .slide import Slides

if TYPE_CHECKING:
    from .app import App


@dataclass(repr=False)
class Presentation(Element):
    parent: App
    collection: Presentations

    def close(self) -> None:
        self.api.Close()

    def delete(self) -> None:
        self.close()

    @property
    def slides(self) -> Slides:
        return Slides(self.api.Slides, self)

    @property
    def width(self) -> float:
        return self.api.PageSetup.SlideWidth

    @property
    def height(self) -> float:
        return self.api.PageSetup.SlideHeight


@dataclass(repr=False)
class Presentations(Collection[Presentation]):
    parent: App
    type: ClassVar[type[Element]] = Presentation

    def add(self) -> Presentation:
        api = self.api.Add()
        return Presentation(api, self.parent, self)

    def close(self) -> None:
        for pr in self:
            pr.close()

    @property
    def active(self) -> Presentation:
        api = self.app.ActivePresentation
        return Presentation(api, self.parent, self)
