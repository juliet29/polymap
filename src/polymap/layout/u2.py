# updates 2

from copy import deepcopy


from polymap.geometry.modify.update import Move, update_domain
from polymap.geometry.modify.validate import (
    InvalidLayoutError,
    InvalidPolygonError,
    validate_layout,
)
from polymap.layout.graph import (
    AxGraph,
    Edge,
    EdgeData,
    EdgeDataDiGraph,
    compute_delta_between_surfs,
    create_move_graph,
)
from polymap.layout.interfaces import Layout


# def collect_moves(Gax: AxGraph):
#
#     def get(edge: Edge):
#         domain = layout.get_domain(edge.data.domain_name)
#         surf = layout.get_surface_by_name(edge.u)
#
#         # NOTE: recomputing the delta due to instabilities in reading and writing..
#         nb = layout.get_surface_by_name(edge.v)
#         logger.info(edge.summary_string())
#         try:
#             delta = compute_delta_between_surfs(surf, nb)
#         except InvalidRangeException:
#             delta = compute_delta_between_surfs(nb, surf)
#
#         # delta = edge.data.delta
#         m = Move(domain, surf, delta)
#         logger.info(str(m))
#         return m
#
#     G, layout = Gax.G, Gax.layout
#     moves = [get(e) for e in G.edge_data()]
#
#     # TODO: later: logic on the moves, so can have negative deltas .. but do this on the graph stage..
#     return moves
#


def apply_move_to_layout(layout: Layout, move: Move):
    new_domain = update_domain(move)
    unchanged_domains = [i for i in layout.domains if i.name != move.domain.name]
    new_layout = Layout(unchanged_domains + [new_domain])
    validate_layout(new_layout)  # TODO plot layout failure..
    return new_layout


def get_graph_from_root(layout: Layout, G: EdgeDataDiGraph, root: str):

    def update_deltas():
        # nbs = G.successors(root)
        edges = [i for i in G.edge_data() if i.u == root]
        new_edges = []
        # update delats
        for e in edges:
            surf = layout.get_surface_by_name(e.u)
            nb = layout.get_surface_by_name(e.v)
            delta = compute_delta_between_surfs(surf, nb)
            new_e = Edge(e.u, e.v, data=EdgeData(delta, e.data.domain_name))
            new_edges.append(new_e)
        new_G = EdgeDataDiGraph()
        for e in new_edges:
            new_G.add_edge(e.u, e.v, data=e.data)
        return new_G

    updated_G = update_deltas()
    return create_move_graph(layout, updated_G)

    # for nb in nbs:
    # for e in new_edges:
    #     if abs(e.data.delta) > 0:
    #         new_G.add_edge(e.u, e.v, data=e.data)


# def try_moves(Gax: AxGraph):
#     moves = collect_moves(Gax)
#     layout = deepcopy(Gax.layout)
#     for move in moves:
#         logger.trace(f"{move.delta=}")
#         if abs(move.delta) == 0:
#             continue
#         updated_domain = layout.get_domain(move.domain.name)
#         updated_surface = layout.get_surface_by_name(move.surface.name_w_domain)
#         new_move = Move(updated_domain, updated_surface, move.delta)
#         try:
#             new_layout = apply_move_to_layout(layout, new_move)
#         except (InvalidLayoutError, InvalidPolygonError) as e:
#             e.message()
#             e.plot()
#             continue
#         layout = new_layout
#
#     return layout
#
def handle_move(layout: Layout, move: Move):
    try:
        new_layout = apply_move_to_layout(layout, move)
    except (InvalidLayoutError, InvalidPolygonError) as e:
        e.message()
        e.plot()
        return layout
    return new_layout


def try_moves(Gax: AxGraph):
    def make(layout: Layout, edge: Edge):
        # logger.info(edge.summary_string())
        # moveG = get_graph_from_root(layout, Gax.G, edge.u)
        # logger.debug(moveG.edge_summary_list())
        # correct_edges = [
        #     i for i in moveG.edge_data() if set_equality([i.u, i.v], [edge.u, edge.v])
        # ]
        # if not correct_edges:
        #     return None
        # #
        # correct_edge = correct_edges[0]
        domain = layout.get_domain(edge.data.domain_name)
        surf = layout.get_surface_by_name(edge.u)
        delta = edge.data.delta
        # nb = layout.get_surface_by_name(edge.v)
        # try:
        #     delta = compute_delta_between_surfs(surf, nb)
        # except InvalidRangeException:
        #     delta = -1 * compute_delta_between_surfs(nb, surf)
        m = Move(domain, surf, delta)
        return m

    roots = [i.u for i in Gax.G.edge_data()]
    layout = deepcopy(Gax.layout)

    for root in roots:
        curr_graph = get_graph_from_root(layout, Gax.G, root)
        for edge in curr_graph.edge_data():
            move = make(layout, edge)
            new_layout = handle_move(layout, move)
            layout = new_layout
    # for e in Gax.G.edge_data():
    #     move = make(layout, e)
    #     if not move:
    #         logger.info(f"Move is redundant for ({e.u}, {e.v})")
    #         continue
    #     logger.info(f"{str(move)} to meet {e.v}")
    #     try:
    #         new_layout = apply_move_to_layout(layout, move)
    #     except (InvalidLayoutError, InvalidPolygonError) as e:
    #         e.message()
    #         e.plot()
    #         continue
    #     layout = new_layout
    #
    return layout
