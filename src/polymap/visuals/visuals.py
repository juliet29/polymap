import shapely as sp
from shapely import plotting
import matplotlib.pyplot as plt
from matplotlib.axes import Axes
from utils4plans.geom import Coord
from typing import NamedTuple

from polymap.geometry.ortho import FancyOrthoDomain
from polymap.geometry.layout import Layout

from polymap.visuals.styles import AnnotationStyles, EnclosedAnnotationStyle


class AnnotationPair(NamedTuple):
    coord: Coord
    name: str | int | float


def add_annotations(
    annotation_pairs: list[AnnotationPair], ax: Axes, styles=[AnnotationStyles()]
):
    if len(styles) == 1:
        for coord, name in annotation_pairs:
            ax.text(*coord.as_tuple, s=str(name), **styles[0].values)
    else:
        assert len(annotation_pairs) == len(styles)
        for (coord, name), style in zip(annotation_pairs, styles):
            ax.text(*coord.as_tuple, s=str(name), **style.values)

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


def plot_domain_with_surfaces(
    domain: FancyOrthoDomain, title: str = "", ax: Axes | None = None, show=True
):
    if not ax:
        fig, ax = plt.subplots()
    ax = plot_polygon(domain.polygon, show=False, title=title, ax=ax)
    surfs = domain.surfaces
    surface_labels = [AnnotationPair(i.centroid, i.name) for i in surfs]
    ax = add_annotations(surface_labels, ax)

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
    layout: Layout,
    layout_name: str = "",
    ax: Axes | None = None,
    add_labels=True,
    show=True,
):

    if not ax:
        fig, ax = plt.subplots()

    if not layout.domains:
        return ax

    polygons = sp.MultiPolygon([i.polygon for i in layout.domains])
    ax = plot_polygon(polygons, ax, title=layout_name)

    if add_labels:
        room_labels = [AnnotationPair(i.centroid, i.name) for i in layout.domains]
        ax = add_annotations(room_labels, ax)

    if show:
        plt.show()

    return ax


def plot_layout_alone(
    layout: Layout, layout_name: str = "", show_surface_labels: bool = False
):

    fig, ax = plt.subplots()
    for domain in layout.domains:
        ax = plot_polygon(domain.polygon, show=False, ax=ax)
        room_label = AnnotationPair(domain.centroid, domain.name)
        ax = add_annotations([room_label], ax)

        if show_surface_labels:
            surfs = domain.surfaces
            style = EnclosedAnnotationStyle(
                fontsize="xx-small", edge_color="white", alpha=1
            )
            surface_labels = [AnnotationPair(i.centroid, i.short_name) for i in surfs]
            ax = add_annotations(surface_labels, ax, styles=[style])

    ax.set_title(layout_name)

    return fig, ax


def plot_layout_comparison(layouts: list[Layout], names: list[str]):
    n = len(layouts)
    fig, axs = plt.subplots(ncols=n)
    assert len(layouts) == len(names)

    for ix, layout in enumerate(layouts):
        plot_layout(layout, names[ix], axs[ix], show=False)

    plt.show()


if __name__ == "__main__":
    # dom = create_ortho_domain("NON_ORTHO")
    #
    pass  # plot_polygon(dom.polygon)
