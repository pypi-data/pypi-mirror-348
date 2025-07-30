from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from tempfile import NamedTemporaryFile
from typing import TYPE_CHECKING, ClassVar, Literal

from win32com.client import constants

from .base import Base, Collection, Element
from .color import rgb
from .font import Font

if TYPE_CHECKING:
    from typing import Self

    from matplotlib.figure import Figure
    from PIL.Image import Image
    from win32com.client import DispatchBaseClass

    from .slide import Slide
    from .table import Table


@dataclass(repr=False)
class Color(Base):
    @property
    def color(self) -> int:
        return self.api.ForeColor.RGB

    @color.setter
    def color(self, value: int | str | tuple[int, int, int]) -> None:
        self.api.ForeColor.RGB = rgb(value)

    @property
    def alpha(self) -> float:
        return self.api.Transparency

    @alpha.setter
    def alpha(self, value: float) -> None:
        self.api.Transparency = value

    def set(
        self,
        color: int | str | tuple[int, int, int] | None = None,
        alpha: float | None = None,
    ) -> Self:
        if color is not None:
            self.color = color
        if alpha is not None:
            self.alpha = alpha

        return self

    def update(self, color: Color) -> None:
        self.color = color.color
        self.alpha = color.alpha


@dataclass(repr=False)
class Fill(Color):
    pass


@dataclass(repr=False)
class Line(Color):
    @property
    def weight(self) -> float:
        return self.api.Weight

    @weight.setter
    def weight(self, value: float) -> None:
        self.api.Weight = value

    def set(
        self,
        color: int | str | tuple[int, int, int] | None = None,
        alpha: float | None = None,
        weight: float | None = None,
    ) -> Self:
        if color is not None:
            self.color = color
        if alpha is not None:
            self.alpha = alpha
        if weight is not None:
            self.weight = weight

        return self

    def update(self, line: Line) -> None:
        self.color = line.color
        self.alpha = line.alpha
        self.weight = line.weight


@dataclass(repr=False)
class Shape(Element):
    parent: Slide
    collection: Shapes

    @property
    def left(self) -> float:
        return self.api.Left

    @property
    def top(self) -> float:
        return self.api.Top

    @property
    def width(self) -> float:
        return self.api.Width

    @property
    def height(self) -> float:
        return self.api.Height

    @left.setter
    def left(self, value: float | Literal["center"]) -> float:
        slide = self.parent

        if value == "center":
            value = (slide.width - self.width) / 2
        elif value < 0:
            value = slide.width - self.width + value

        self.api.Left = value
        return value

    @top.setter
    def top(self, value: float | Literal["center"]) -> float:
        slide = self.parent

        if value == "center":
            value = (slide.height - self.height) / 2
        elif value < 0:
            value = slide.height - self.height + value

        self.api.Top = value
        return value

    @width.setter
    def width(self, value: float) -> None:
        self.api.Width = value

    @height.setter
    def height(self, value: float) -> None:
        self.api.Height = value

    @property
    def text_range(self) -> DispatchBaseClass:
        return self.api.TextFrame.TextRange

    @property
    def text(self) -> str:
        return self.text_range.Text

    @text.setter
    def text(self, text: str) -> None:
        self.text_range.Text = text

    @property
    def font(self) -> Font:
        return Font(self.text_range.Font)

    @property
    def fill(self) -> Fill:
        return Fill(self.api.Fill)

    @property
    def line(self) -> Line:
        return Line(self.api.Line)

    def copy(self) -> None:
        self.api.Copy()


@dataclass(repr=False)
class Shapes(Collection[Shape]):
    parent: Slide
    type: ClassVar[type[Element]] = Shape

    @property
    def title(self) -> Shape:
        return Shape(self.api.Title, self.parent, self)

    def add(
        self,
        kind: int | str,
        left: float,
        top: float,
        width: float,
        height: float,
        text: str = "",
    ) -> Shape:
        if isinstance(kind, str):
            kind = getattr(constants, f"msoShape{kind}")

        api = self.api.AddShape(kind, left, top, width, height)
        shape = Shape(api, self.parent, self)
        shape.text = text

        return shape

    def add_label(
        self,
        text: str,
        left: float,
        top: float,
        width: float = 72,
        height: float = 72,
        *,
        auto_size: bool = True,
    ) -> Shape:
        orientation = constants.msoTextOrientationHorizontal
        api = self.api.AddLabel(orientation, left, top, width, height)

        if auto_size is False:
            api.TextFrame.AutoSize = False

        label = Shape(api, self.parent, self)
        label.text = text
        return label

    def add_table(
        self,
        num_rows: int,
        num_columns: int,
        left: float = 100,
        top: float = 100,
        width: float = 100,
        height: float = 100,
    ) -> Table:
        from .table import Table

        api = self.api.AddTable(num_rows, num_columns, left, top, width, height)
        return Table(api, self.parent, self)

    def add_picture(
        self,
        file_name: str | Path,
        left: float = 0,
        top: float = 0,
        width: float = -1,
        height: float = -1,
        scale: float | None = None,
    ) -> Shape:
        file_name = Path(file_name).absolute()

        api = self.api.AddPicture(
            FileName=file_name,
            LinkToFile=False,
            SaveWithDocument=True,
            Left=left,
            Top=top,
            Width=width,
            Height=height,
        )

        if scale is not None:
            api.ScaleWidth(scale, 1)
            api.ScaleHeight(scale, 1)

        return Shape(api, self.parent, self)

    def add_image(
        self,
        image: Image,
        left: float = 0,
        top: float = 0,
        width: float = -1,
        height: float = -1,
        scale: float | None = None,
    ) -> Shape:
        with NamedTemporaryFile(suffix=".png", delete=False) as file:
            file_name = Path(file.name)
            image.save(file_name)
            shape = self.add_picture(file_name, left, top, width, height, scale)

        file_name.unlink()
        return shape

    def add_figure(
        self,
        fig: Figure,
        left: float = 0,
        top: float = 0,
        width: float = -1,
        height: float = -1,
        scale: float | None = None,
        dpi: int | Literal["figure"] = "figure",
        transparent: bool | None = None,
    ) -> Shape:
        with NamedTemporaryFile(suffix=".png", delete=False) as file:
            file_name = Path(file.name)
            fig.savefig(
                file_name,
                dpi=dpi,
                bbox_inches="tight",
                transparent=transparent,
            )
            shape = self.add_picture(file_name, left, top, width, height, scale)

        file_name.unlink()
        return shape

    def paste(
        self,
        left: float | None = None,
        top: float | None = None,
        width: float | None = None,
        height: float | None = None,
    ) -> Shape:
        api = self.api.Paste()

        if left is not None:
            api.Left = left
        if top is not None:
            api.Top = top
        if width is not None:
            api.Width = width
        if height is not None:
            api.Height = height

        return Shape(api, self.parent, self)

    def paste_special(
        self,
        data_type: int | str = 0,
        left: float | None = None,
        top: float | None = None,
        width: float | None = None,
        height: float | None = None,
    ) -> Shape:
        """
        Args:
            data_type (int):
                0: ppPasteDefault
                1: ppPasteBitmap
                2: ppPasteEnhancedMetafile
                4: ppPasteGIF
                8: ppPasteHTML
                5: ppPasteJPG
                3: ppPasteMetafilePicture
                10: ppPasteOLEObject
                6: ppPastePNG
                9: ppPasteRTF
                11: ppPasteShape
                7: ppPasteText
        """
        if isinstance(data_type, str):
            data_type = getattr(constants, f"ppPaste{data_type}")

        api = self.api.PasteSpecial(data_type)

        if left is not None:
            api.Left = left
        if top is not None:
            api.Top = top
        if width is not None:
            api.Width = width
        if height is not None:
            api.Height = height

        return Shape(api, self.parent, self)
