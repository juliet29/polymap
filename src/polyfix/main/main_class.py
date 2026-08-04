from pathlib import Path

from utils4plans.io.extras.yaml import write_yaml

from polyfix.adjacencies.zonal import capture_zone_adjacencies
from polyfix.layout.interfaces import AxGraph
from polyfix.main.fix_fxs import (
    Ortho,
    Reconcile,
    Rotate,
    Simplify,
    XMove,
    XPlan,
    YMove,
    YPlan,
)
from polyfix.pydantic_models import read_layout_from_path


class PolyFixer:
    def __init__(self, init_geom: Path, save_loc: Path, save_angle: bool) -> None:
        self.init_geom_path = init_geom
        self.save_loc = save_loc
        self.save_angle = save_angle

        # self.lo: Layout | None = None
        # self.gx: AxGraph | None = None
        # self.gy: AxGraph | None = None
        #

    def __call__(self):
        in_layout = read_layout_from_path(self.init_geom_path)
        self.lo = Rotate(self.save_loc, self.save_angle)(in_layout)
        self.lo = Ortho(self.save_loc)(self.lo)
        self.lo = Simplify(self.save_loc)(self.lo)

        self.gx = XPlan(self.save_loc)(self.lo)
        self.lo = XMove(self.save_loc)(self.gx)

        self.gy = YPlan(self.save_loc)(self.lo)
        self.lo = YMove(self.save_loc)(self.gy)

        self.lo = Reconcile(self.save_loc)(self.lo)
        return self.lo

    def save_adjacencies(self):
        assert isinstance(self.gx, AxGraph) and isinstance(self.gy, AxGraph)
        adj = capture_zone_adjacencies(self.gx, self.gy)
        write_yaml(adj, self.save_loc / "out.adj.yaml")

    def save_rotation_angle(self):
        pass
