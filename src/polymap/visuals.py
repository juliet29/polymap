import shapely as sp
import numpy as np
from shapely import plotting
import matplotlib.pyplot as plt
from matplotlib.axes import Axes
from utils4plans.geom import Coord
from typing import NamedTuple

from polymap.interfaces import GraphPairs
from polymap.layout.interfaces import Layout
import matplotlib as mpl


class AnnotationPair(NamedTuple):
    coord: Coord
    name: str


def add_annotations(annotation_pairs: list[AnnotationPair], ax: Axes):
    for coord, name in annotation_pairs:
        ax.text(*coord.as_tuple, s=name)

    return ax


def plot_polygon(
    p: sp.Polygon | sp.MultiPolygon,
    ax: Axes | None = None,
    show=False,
    title="",
):

    if not ax:
        fig, ax = plt.subplots()
    plotting.plot_polygon(p, ax=ax)
    ax.set_title(title)
    if show:
        plt.show()
    return ax


def plot_polygon_comparison(
    polys: list[sp.Polygon], titles: list[str], big_title: str = ""
):
    n = len(polys)
    fig, axs = plt.subplots(
        ncols=n,
    )

    for ix, p in enumerate(polys):
        plotting.plot_polygon(p, ax=axs[ix])
        if len(titles) > ix:
            axs[ix].set_title(titles[ix])

    fig.suptitle(big_title)

    plt.show()


def plot_layout(
    layout: Layout, layout_name: str = "", ax: Axes | None = None, show=True
):

    if not ax:
        fig, ax = plt.subplots()
    polygons = sp.MultiPolygon([i.polygon for i in layout.domains])
    ax = plot_polygon(polygons, ax, title=layout_name)
    room_labels = [AnnotationPair(i.centroid, i.name) for i in layout.domains]
    ax = add_annotations(room_labels, ax)

    if show:
        plt.show()

    return ax


def plot_layout_comparison(layouts: list[Layout], names: list[str]):
    n = len(layouts)
    fig, axs = plt.subplots(ncols=n)
    assert len(layouts) == len(names)

    for ix, layout in enumerate(layouts):
        plot_layout(layout, names[ix], axs[ix], show=False)

    plt.show()


def plot_graph_pairs_on_layout(
    layout: Layout, graph_pairs: GraphPairs, ax: Axes, alpha: float = 1, show=True
):
    def get_line(main: str, nbs: list[str]):
        main_surface = layout.get_surface_by_name(main)
        nb_surfaces = [layout.get_surface_by_name(i) for i in nbs]
        surfaces = [main_surface] + nb_surfaces
        lines = [i.coords.shapely_line for i in surfaces]
        return sp.MultiLineString(lines)

    colors = mpl.colormaps["rainbow"](np.linspace(0, 1, len(graph_pairs)))
    for (key, values), color in zip(graph_pairs.items(), colors):
        mline = get_line(key, values)
        plotting.plot_line(mline, ax=ax, color=color, linewidth=3, alpha=alpha)

    if show:
        plt.show()

    return ax


# def plot_domain(self):
#     fig, ax = plt.subplots()
#     plot_polygon(self.polygon, ax=ax)
#     ax.set_title(f" {self.name}")
#     plt.show()


def plot_line(p: sp.LineString | sp.MultiLineString):
    fig, ax = plt.subplots()
    plotting.plot_line(p, ax=ax)
    plt.show()


if __name__ == "__main__":
    # dom = create_ortho_domain("NON_ORTHO")
    #
    pass  # plot_polygon(dom.polygon)
