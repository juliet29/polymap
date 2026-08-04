from pathlib import Path

from polyfix.main.process import (
    move,
    ortho,
    plan,
    reconcile,
    rotate,
    save_adjacencies,
    simplify,
)
from polyfix.main.workflow_paths import SingleWorkflowPaths


def execute_polyfix(output_path: Path, save_adj: bool = False):
    paths = SingleWorkflowPaths(output_path)

    rotate(paths.init, paths.rotate)
    ortho(paths.rotate, paths.ortho)
    simplify(paths.ortho, paths.simplify)
    plan("X", paths.rotate, paths.xplan)
    move("X", paths.xplan, paths.xmove)

    plan("Y", paths.xmove, paths.yplan)
    move("Y", paths.yplan, paths.ymove)
    reconcile(paths.ymove, paths.reconcile)

    if save_adj:
        save_adjacencies(paths.xplan, paths.yplan, paths.adjacencies)
