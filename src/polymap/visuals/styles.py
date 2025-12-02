from typing import Literal, TypedDict
from dataclasses import dataclass


FontSize = Literal[
    "xx-small", "x-small", "small", "medium", "large", "x-large", "xx-large"
]

NormedColor = tuple[float, float, float, float]

Color = (
    Literal["navy", "deepskyblue", "gray", "snow", "saddlebrown", "white", "black"]
    | NormedColor
)
LineStyle = Literal[
    "-",
    "--",
    "-.",
    ":",
]


class BoundingBox(TypedDict):
    boxstyle: str
    ec: Color
    fc: Color
    alpha: int


@dataclass
class PlotStyles:
    @property
    def values(self):
        return self.__dict__


@dataclass
class AnnotationStyles(PlotStyles):
    # face_color: Color = "white"
    # bbox: BoundingBox = field(
    #     default_factory=lambda: {
    #         "boxstyle": "round,pad=0.2",
    #         "ec": "black",
    #         "fc": "white",
    #         "alpha": 1,
    #     }
    # )
    fontsize: FontSize = "small"
    horizontalalignment: Literal["left", "center", "right"] = "center"
    verticalalignment: Literal["top", "center", "baseline", "bottom"] = "center"
    rotation: Literal["vertical"] | None = None
    zorder = 10

    # def update_bbox_color(self, color: Color):
    #     self.bbox["fc"] = color
