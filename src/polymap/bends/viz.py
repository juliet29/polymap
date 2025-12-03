from typing import NamedTuple
from matplotlib.axes import Axes
from shapely import plotting
from polymap.geometry.ortho import FancyOrthoDomain
import matplotlib.pyplot as plt
from polymap.geometry.surfaces import Surface
from polymap.visuals.styles import Color
from polymap.visuals.visuals import plot_polygon

import shapely as sp


class DomainMoveDetails(NamedTuple):
    start_domain: FancyOrthoDomain
    end_domain: FancyOrthoDomain
    surfs: list[Surface]


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


def plot_domain_move_only(dmd: DomainMoveDetails, ax: Axes, ax2: Axes):
    domain, domain2, surfs = dmd
    surf_color: Color = "saddlebrown"

    plot_polygon(
        domain.polygon,
        ax=ax,
    )
    lines = sp.MultiLineString([i.coords.shapely_line for i in surfs])
    plotting.plot_line(lines, ax=ax, color=surf_color)
    plot_polygon(
        domain2.polygon,
        ax=ax2,
    )
    plotting.plot_line(lines, ax=ax2, color=surf_color, alpha=0.4, add_points=False)


def plot_domain_move(
    domain: FancyOrthoDomain,
    domain2: FancyOrthoDomain,
    surfs: list[Surface],
    id: str = "",
):
    title = f"{id} | {domain.name}"
    fig, (ax, ax2) = plt.subplots(ncols=2)
    dmd = DomainMoveDetails(domain, domain2, surfs)
    plot_domain_move_only(dmd, ax, ax2)
    fig.suptitle(title)
    plt.show()


def plot_domain_iteration(moves: list[DomainMoveDetails], id: str):

    domain = moves[0].start_domain
    fig, axes = plt.subplots(ncols=2, nrows=len(moves))
    title = f"{id} | {domain.name}"
    fig.suptitle(title)

    if len(moves) == 1:
        plot_domain_move_only(moves[0], *axes)
    else:
        for row, dmd in zip(axes, moves):
            plot_domain_move_only(dmd, *row)

    plt.show()
