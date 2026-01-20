from loguru import logger
import numpy as np
import matplotlib as mpl
import matplotlib.pyplot as plt
from utils4plans.geom import Coord
from utils4plans.lists import chain_flatten
from polymap.geometry.surfaces import Surface
from polymap.layout.interfaces import AxGraph
from polymap.visuals.styles import EnclosedAnnotationStyle
from polymap.visuals.visuals import AnnotationPair, add_annotations, plot_layout
from rich.pretty import pretty_repr


def create_edge_dict(Gax: AxGraph):
    # edge = [k for k, v in edge_dict.items() if v == ix][0]
    def edge_order_metric(edge: tuple[str, str]):
        n1, n2 = edge
        n1_loc = Gax.layout.get_surface_by_name(n1).centroid
        n2_loc = Gax.layout.get_surface_by_name(n2).centroid
        return max(n1_loc, n2_loc)
        # if Gax.ax == "X":
        #     return max(n1_loc.y, n2_loc.y)
        # else:
        #     return max(n1_loc.x, n2_loc.x)

    edges = list(Gax.G.edges)
    sorted_edges = sorted(edges, key=lambda x: edge_order_metric(x), reverse=True)
    edge_dict = {e: ix for ix, e in enumerate(sorted_edges)}
    return edge_dict


def collect_node_edges(Gax: AxGraph):

    d = {}
    # TODO add to the graph class
    edge_dict = create_edge_dict(Gax)
    logger.info(pretty_repr(edge_dict))

    def find_edge_num(e: tuple[str, str]):
        try:
            n1, n2 = e
            num = edge_dict[(n1, n2)]
        except KeyError:
            n2, n1 = e
            num = edge_dict[(n1, n2)]

        return num

    for node in Gax.G.nodes:
        nbs = Gax.G.to_undirected().neighbors(node)
        nums = [find_edge_num((node, nb)) for nb in nbs]
        d[node] = nums

    return d


def plan_labels_for_surface(Gax: AxGraph, surf: Surface, edge_ixes: list[int]):

    sorted_edges = sorted(edge_ixes)

    increment_size = (surf.range.size / 2) / (len(sorted_edges) + 1)

    if Gax.ax == "X":
        locs = [
            Coord(surf.centroid.x, surf.centroid.y - (ix) * increment_size)
            for ix, _ in enumerate(sorted_edges)
        ]
    else:
        locs = [
            Coord(surf.centroid.x - (ix) * increment_size, surf.centroid.y)
            for ix, _ in enumerate(sorted_edges)
        ]

    return sorted_edges, locs


def create_annotation_for_graph(Gax: AxGraph):
    surface_edge_ixes = collect_node_edges(Gax)

    def handle(surf_name: str, ixes: list[int]):
        surf = Gax.layout.get_surface_by_name(surf_name)
        sorted_edge_ixes, locs = plan_labels_for_surface(Gax, surf, ixes)
        annotations = [
            AnnotationPair(coord, ix) for ix, coord in zip(sorted_edge_ixes, locs)
        ]
        return annotations

    all_annots = [handle(k, v) for k, v in surface_edge_ixes.items()]
    return sorted(chain_flatten(all_annots), key=lambda x: x.name)


def plot_layout_with_graph_info(Gax: AxGraph, layout_name: str = "", show=True):
    fig, ax = plt.subplots()
    ax = plot_layout(Gax.layout, layout_name, show=False, ax=ax)
    annots = create_annotation_for_graph(Gax)
    colors = mpl.colormaps["rainbow"](np.linspace(0, 1, len(annots) // 2))
    doubled_colors = [item for item in colors for _ in range(2)]
    styles = [EnclosedAnnotationStyle(edge_color=c) for c in doubled_colors]

    ax = add_annotations(annots, ax, styles)
    if show:
        plt.show()
    return fig, ax
