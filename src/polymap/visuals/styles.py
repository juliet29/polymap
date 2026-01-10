from copy import deepcopy
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
    #


@dataclass
class EnclosedAnnotationStyle(AnnotationStyles):
    edge_color: Color = "white"
    fontsize: FontSize = "medium"
    alpha: float = 0.4

    @property
    def bbox(self):
        return {
            "boxstyle": "circle,pad=0.2",
            "ec": self.edge_color,
            "fc": self.edge_color,
            "alpha": self.alpha,
            "fill": True,
        }

    @property
    def values(self) -> dict:
        d = deepcopy(self.__dict__)
        d["bbox"] = self.bbox
        # d["color"] = self.edge_color
        d.pop("edge_color")
        d.pop("alpha")
        return d
