# updates 2

from copy import deepcopy

from loguru import logger
from rich.pretty import pretty_repr
from utils4plans.geom import InvalidRangeException
from utils4plans.sets import set_difference


from polymap.geometry.modify.update import Move, update_domain
from polymap.geometry.modify.validate import (
    InvalidLayoutError,
    InvalidPolygonError,
    validate_layout_overlaps,
)
from polymap.geometry.ortho import FancyOrthoDomain
from polymap.layout.interfaces import (
    AxGraph,
    Edge,
    EdgeData,
    EdgeDataDiGraph,
)
from polymap.layout.main.plan import compute_delta_between_surfs, create_move_graph

from polymap.geometry.layout import Layout


def study_small_change(name: str, l1: Layout, l2: Layout):
    old = l1.get_domain(name)
    new = l2.get_domain(name)

    res = new.normalized_coords == old.normalized_coords
    dif_coords = set_difference(
        old.polygon.exterior.coords, new.polygon.exterior.coords
    )
    logger.debug(f"{name} coords are same: {res}. diff coords: {dif_coords}")


def study_polygon_changes(l1: Layout, l2: Layout):
    for old in l1.domains:
        new = l2.get_domain(old.name)
        if old.polygon != new.polygon:
            logger.trace(f"{old.name} has changed!")


def apply_move_to_layout(layout: Layout, move: Move, other_dom: FancyOrthoDomain):
    new_domain = update_domain(move)
    old_doms = deepcopy(layout.domains)
    unchanged_domains = [i for i in old_doms if i.name != move.domain.name]

    new_layout = Layout(unchanged_domains + [new_domain])
    study_polygon_changes(layout, new_layout)
    validate_layout_overlaps(layout)

    # study_small_change("balcony_4", layout, new_layout)
    # study_small_change("bedroom_2", layout, new_layout)
    # study_small_change("living_room_6", layout, new_layout)
    return new_layout


def compute_delta_between_edge(u: str, v: str, layout: Layout):
    surf = layout.get_surface_by_name(u)
    nb = layout.get_surface_by_name(v)
    try:
        delta = compute_delta_between_surfs(surf, nb)
    except InvalidRangeException:
        delta = compute_delta_between_surfs(nb, surf)
    return delta


def get_graph_from_root(layout: Layout, G: EdgeDataDiGraph, root: str):
    def update_deltas():
        edges = [i for i in G.edge_data() if i.u == root]
        new_edges = []
        for e in edges:
            surf = layout.get_surface_by_name(e.u)
            nb = layout.get_surface_by_name(e.v)
            delta = compute_delta_between_surfs(surf, nb)
            new_e = Edge(e.u, e.v, data=EdgeData(delta, e.data.domain_name))

            # logger.debug(f"original edge: {e.summary_string()}")
            # logger.debug(f"new edge: {new_e.summary_string()}")

            new_edges.append(new_e)
        new_G = EdgeDataDiGraph()
        for e in new_edges:
            new_G.add_edge(e.u, e.v, data=e.data)
        return new_G

    updated_G = update_deltas()
    return create_move_graph(layout, updated_G)


def handle_move(layout: Layout, move: Move, other_dom: FancyOrthoDomain):
    try:
        new_layout = apply_move_to_layout(layout, move, other_dom)
    except (InvalidLayoutError, InvalidPolygonError) as e:
        e.message()
        return layout
    return new_layout


def try_moves(Gax: AxGraph):
    def make(layout: Layout, edge: Edge):
        domain = layout.get_domain(edge.data.domain_name)
        surf = layout.get_surface_by_name(edge.u)
        delta = edge.data.delta

        other_surf = layout.get_surface_by_name(edge.v)
        other_dom = layout.get_domain(other_surf.domain_name)
        m = Move(domain, surf, delta)

        return m, other_dom

    incoming_G_edges = [i.summary_string() for i in Gax.G.edge_data()]
    # logger.info(pretty_repr(incoming_G_edges))
    roots = sorted(
        set([i.u for i in Gax.G.edge_data()]),
        key=lambda x: Gax.layout.get_surface_by_name(x).location,
    )
    logger.info(f"{roots=}")
    layout = deepcopy(Gax.layout)

    for root in roots:
        curr_graph = get_graph_from_root(layout, Gax.G, root)
        logger.debug(
            f"\nroot:[bold]{root.upper()}[/bold].\n{pretty_repr(curr_graph.edge_summary_list())}\n"
        )
        for edge in curr_graph.edge_data():
            if abs(edge.data.delta) > 0:
                # logger.debug(f"curr edge to move: {edge.summary_string()}")
                move, other_dom = make(layout, edge)
                logger.debug(f"{move.summary()} to {edge.v}")
                new_layout = handle_move(layout, move, other_dom)
                layout = new_layout
        # for edge in curr_graph.edge_data():
        #     new_delta = compute_delta_between_edge(edge.u, edge.v, layout)
        # logger.debug(f"New delta betwen {edge.u} and {edge.v} is {new_delta}")

    validate_layout_overlaps(layout)
    #
    return layout
