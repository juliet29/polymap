from pathlib import Path

from polyfix.bends.main import remove_bends_from_layout
from polyfix.geometry.modify.precision import decrease_layout_precision
from polyfix.layout.main.move import try_moves
from polyfix.layout.main.plan import create_move_graph_for_all_surfaces_along_axis
from polyfix.main.fix_class import FixBaseClass, Stage
from polyfix.nonortho.main import orthogonalize_layout
from polyfix.reconcile.main import reconcile_all
from polyfix.rotate.main import rotate_layout


class Rotate(FixBaseClass):
    def __init__(self, save_loc: Path):
        super().__init__(
            fix_type="Action", stage=Stage.ROTATE, fx=self.local_fx, save_loc=save_loc
        )
        self.angle: float = 0.0

    def local_fx(self, layout):
        angle, layout = rotate_layout(layout)
        self.angle = angle
        return layout


class Ortho(FixBaseClass):
    def __init__(self, save_loc: Path):
        super().__init__(
            fix_type="Action",
            stage=Stage.ORTHO,
            fx=orthogonalize_layout,
            save_loc=save_loc,
        )


class Simplify(FixBaseClass):
    def __init__(self, save_loc: Path):
        super().__init__(
            fix_type="Action", stage=Stage.SIMPLIFY, fx=self.local_fx, save_loc=save_loc
        )
        self.bad_doms = []

    def local_fx(self, layout):
        layout, self.bad_doms = remove_bends_from_layout(layout)
        return decrease_layout_precision(layout)


class XPlan(FixBaseClass):
    def __init__(self, save_loc: Path):
        super().__init__(
            fix_type="Plan", stage=Stage.XPLAN, fx=self.local_fx, save_loc=save_loc
        )

    def local_fx(self, layout):
        return create_move_graph_for_all_surfaces_along_axis(layout, "X")


class YPlan(FixBaseClass):
    def __init__(self, save_loc: Path):
        super().__init__(
            fix_type="Plan", stage=Stage.YPLAN, fx=self.local_fx, save_loc=save_loc
        )

    def local_fx(self, layout):
        return create_move_graph_for_all_surfaces_along_axis(layout, "Y")


class XMove(FixBaseClass):
    def __init__(self, save_loc: Path):
        super().__init__(
            fix_type="Move", stage=Stage.XMOVE, fx=try_moves, save_loc=save_loc
        )


class YMove(FixBaseClass):
    def __init__(self, save_loc: Path):
        super().__init__(
            fix_type="Move", stage=Stage.YMOVE, fx=try_moves, save_loc=save_loc
        )


class Reconcile(FixBaseClass):
    def __init__(self, save_loc: Path):
        super().__init__(
            fix_type="Action",
            stage=Stage.RECONCILE,
            fx=self.local_fx,
            save_loc=save_loc,
        )

    def local_fx(self, layout):

        return reconcile_all(layout)
