import matplotlib
from cyclopts import App
from loguru import logger

from polyfix.reconcile.main import reconcile_all

matplotlib.use("module://matplotlib-backend-kitty")
import matplotlib.pyplot as plt

from polyfix.cli.studies.paths import ProjectPaths
from polyfix.pydantic_models import read_layout_from_path
from polyfix.reconcile.hole_finder import HoleFinder, study_replace_domain_with_hole

rec = App("rec")


CASE = "5299"

path = ProjectPaths.inputs.ext_msd.proc / f"{CASE}/ymove/out.json"


@rec.command
def fc():

    layout = read_layout_from_path(path)
    hf = HoleFinder(layout)

    fig = hf.plot()
    plt.show()

    logger.info(f"path: {path}")


@rec.command
def fd():

    layout = read_layout_from_path(path)
    hf = HoleFinder(layout)
    holes = hf.holes_list[0]

    tree = hf.tree
    return tree.query(holes, "touches")


@rec.command
def fe():
    layout = read_layout_from_path(path)
    hf = HoleFinder(layout)
    hole = hf.holes_list[0]
    fig = study_replace_domain_with_hole(layout, hf.tree, hole)
    plt.show()


@rec.command
def fg():
    layout = read_layout_from_path(path)
    reconcile_all(layout)
