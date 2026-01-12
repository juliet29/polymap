# updates 2

from copy import deepcopy

from loguru import logger
from utils4plans.geom import InvalidRangeException


from polymap.geometry.modify.update import Move, update_domain
from polymap.geometry.modify.validate import (
    InvalidLayoutError,
    InvalidPolygonError,
    validate_layout,
)
from polymap.layout.graph import AxGraph, Edge, compute_delta_between_surfs
from polymap.layout.interfaces import Layout


def collect_moves(Gax: AxGraph):

    def get(edge: Edge):
        domain = layout.get_domain(edge.data.domain_name)
        surf = layout.get_surface_by_name(edge.u)

        # NOTE: recomputing the delta due to instabilities in reading and writing..
        nb = layout.get_surface_by_name(edge.v)
        logger.info(edge.summary_string())
        try:
            delta = compute_delta_between_surfs(surf, nb)
        except InvalidRangeException:
            delta = compute_delta_between_surfs(nb, surf)

        # delta = edge.data.delta
        m = Move(domain, surf, delta)
        logger.info(str(m))
        return m

    G, layout = Gax.G, Gax.layout
    moves = [get(e) for e in G.edge_data()]

    # TODO: later: logic on the moves, so can have negative deltas .. but do this on the graph stage..
    return moves


def apply_move_to_layout(layout: Layout, move: Move):
    new_domain = update_domain(move)
    unchanged_domains = [i for i in layout.domains if i.name != move.domain.name]
    new_layout = Layout(unchanged_domains + [new_domain])
    validate_layout(new_layout)  # TODO plot layout failure..
    return new_layout


def try_moves(Gax: AxGraph):
    moves = collect_moves(Gax)
    layout = deepcopy(Gax.layout)
    for move in moves:
        logger.trace(f"{move.delta=}")
        if abs(move.delta) == 0:
            continue
        updated_domain = layout.get_domain(move.domain.name)
        updated_surface = layout.get_surface_by_name(move.surface.name_w_domain)
        new_move = Move(updated_domain, updated_surface, move.delta)
        try:
            new_layout = apply_move_to_layout(layout, new_move)
        except (InvalidLayoutError, InvalidPolygonError) as e:
            e.message()
            e.plot()
            continue
        layout = new_layout

    return layout
