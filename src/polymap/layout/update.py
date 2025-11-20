from typing import NamedTuple
from utils4plans.lists import sort_and_group_objects
from utils4plans.sets import set_difference
from rich import print
from polymap.geometry.ortho import FancyOrthoDomain
from polymap.geometry.update import update_domain
from polymap.interfaces import GraphPairs
from polymap.layout.graph import AxGraph
from polymap.layout.interfaces import Layout


def get_unchanged_domains(layout: Layout, new_doms: list[FancyOrthoDomain]):
    # TODO: this is something that might go under test!
    exist_names = [i.name for i in layout.domains]
    new_names = [i.name for i in new_doms]
    print(f"{new_names=}")
    unchanged_names = set_difference(exist_names, new_names)
    unchanged_doms = [layout.get_domain(i) for i in unchanged_names]
    return unchanged_doms


def handle_nb(axgraph: AxGraph, domain: FancyOrthoDomain, root: str, nb: str):
    layout = axgraph.layout
    surface = layout.get_surface_by_name(nb)
    # domain = layout.get_domain(surface.domain_name)
    delta = axgraph.get_delta(root, nb)
    print(f"root={root} | going to move {surface} by {delta:.3f}")
    new_dom = update_domain(domain, surface, delta, debug=True)
    return new_dom


def handle_root(axgraph: AxGraph, root: str):
    nbs = axgraph.get_neighors(root)
    new_doms = [handle_nb(axgraph, root, i) for i in nbs]
    print("\n")
    return new_doms


def get_new_doms_for_graph(axgraph: AxGraph):
    # not all domains will move..
    roots = axgraph.roots
    new_doms = []
    for root in roots:
        res = handle_root(axgraph, root)
        new_doms.extend(res)

    unchanged_doms = get_unchanged_domains(axgraph.layout, new_doms)

    return Layout(unchanged_doms + new_doms)


class SurfaceUpdates(NamedTuple):
    name: str
    delta: float


def collect_domain_changes(axgraph: AxGraph, nb_pairs: GraphPairs):
    # assumming all surfaces that are keys are for the same domain..
    updates: list[SurfaceUpdates] = []
    for surface, nbs in nb_pairs:
        deltas = [axgraph.get_delta(surface, nb) for nb in nbs]
        # going to take the largest collect_domain_changes
        true_delta = max(deltas)
        updates.append(SurfaceUpdates(surface, true_delta))
    return updates


def filter_nb_pairs(nb_pairs: GraphPairs, keys: list[str]) -> GraphPairs:
    return {k: v for k, v in nb_pairs.items() if k in keys}


def get_domain_nb_pairs(axgraph: AxGraph):
    edges_for_domain = sort_and_group_objects(
        axgraph.G.edge_data(), fx=lambda x: x.data.domain_name
    )
    domain_surfaces_to_change = [i.u for i in edges_for_domain]
    nb_pairs_for_domain = [
        filter_nb_pairs(axgraph.nb_pairs, i) for i in domain_surfaces_to_change
    ]
    updated_domains = [collect_domain_changes(axgraph, i) for i in nb_pairs_for_domain]
    pass
