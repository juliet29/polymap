import matplotlib.pyplot as plt
import shapely
from matplotlib.figure import Figure

from polyfix.visuals.visuals import plot_polygon


def plot_geom_stages(
    stages: dict[str, shapely.geometry.base.BaseGeometry],
    bounds_source: shapely.geometry.base.BaseGeometry,
) -> Figure:
    min_x, min_y, max_x, max_y = bounds_source.buffer(2).bounds
    ncols = 3
    nrows = -(-len(stages) // ncols)
    fig, axs = plt.subplots(
        nrows=nrows, ncols=ncols, figsize=(5 * ncols, 5 * nrows), layout="tight"
    )
    flat_axs = axs.flatten()
    for ax, (title, geom) in zip(flat_axs, stages.items()):
        plot_polygon(geom, ax=ax, title=title)
        ax.set_xlim(min_x, max_x)
        ax.set_ylim(min_y, max_y)
        ax.set_aspect("equal")
    for empty_ax in flat_axs[len(stages) :]:
        empty_ax.set_axis_off()
    return fig


def plot_hole_finder(
    geoms: shapely.MultiPolygon,
    union: shapely.geometry.base.BaseGeometry,
    interiors: shapely.MultiPolygon,
) -> Figure:
    return plot_geom_stages(
        {"geoms": geoms, "union": union, "interiors": interiors}, union
    )


def plot_domain_hole_union(
    domain: shapely.Polygon,
    hole: shapely.Polygon,
    union: shapely.geometry.base.BaseGeometry,
) -> Figure:
    return plot_geom_stages(
        {"domain": domain, "hole": hole, "union": union}, union
    )
