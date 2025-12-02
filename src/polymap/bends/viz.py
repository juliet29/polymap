from shapely import plotting
from polymap.geometry.ortho import FancyOrthoDomain
import matplotlib.pyplot as plt
from polymap.geometry.surfaces import Surface
from polymap.visuals.styles import Color
from polymap.visuals.visuals import plot_polygon

import shapely as sp


def plot_domain_and_surf(
    domain: FancyOrthoDomain,
    surfs: list[Surface],
    title: str = "",
    surf_color: Color = "navy",
):
    fig, ax = plt.subplots()
    plot_polygon(domain.polygon, ax=ax, title=title)
    lines = sp.MultiLineString([i.coords.shapely_line for i in surfs])
    plotting.plot_line(lines, ax=ax, color=surf_color)
    plt.show()


def plot_domain_move(
    domain: FancyOrthoDomain,
    domain2: FancyOrthoDomain,
    surfs: list[Surface],
    id: str = "",
    surf_color: Color = "navy",
):
    title = f"{id} | {domain.name}"
    fig, (ax, ax2) = plt.subplots(ncols=2)
    plot_polygon(domain.polygon, ax=ax, title=title)
    lines = sp.MultiLineString([i.coords.shapely_line for i in surfs])
    plotting.plot_line(lines, ax=ax, color=surf_color)
    plot_polygon(domain2.polygon, ax=ax2, title=title)
    plotting.plot_line(lines, ax=ax2, color=surf_color)
    plt.show()
