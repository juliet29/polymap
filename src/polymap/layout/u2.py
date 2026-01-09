# updates 2

from polymap.geometry.modify.update import Move, update_domain
from polymap.geometry.modify.validate import InvalidLayoutError, validate_layout
from polymap.layout.graph import AxGraph, Edge
from polymap.layout.interfaces import Layout


def collect_moves(Gax: AxGraph):

    def get(edge: Edge):
        domain = layout.get_domain(edge.data.domain_name)
        surf = layout.get_surface_by_name(edge.u)
        delta = edge.data.delta
        m = Move(domain, surf, delta)
        return m

    G, layout = Gax.G, Gax.layout
    moves = [get(e) for e in G.edge_data()]

    # TODO: later: logic on the moves, so can have negative deltas .. but do this on the graph stage..
    return moves


def apply_move_to_layout(layout: Layout, move: Move):
    new_domain = update_domain(move)
    unchanged_domains = [i for i in layout.domains if i.name != move.domain.name]
    new_layout = Layout(unchanged_domains + [new_domain])
    validate_layout(new_layout)
    return new_layout


def try_moves(layout: Layout, moves: list[Move]):
    for move in moves:
        try:
            new_layout = apply_move_to_layout(layout, move)
        except InvalidLayoutError as e:
            e.message()
            continue
        layout = new_layout

    return layout
