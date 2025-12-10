from copy import deepcopy
from typing import NamedTuple
from warnings import warn

from rich import print
from utils4plans.lists import sort_and_group_objects_dict
from utils4plans.sets import set_difference

from polymap.geometry.modify.update import Move, update_domain
from polymap.geometry.ortho import FancyOrthoDomain
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


class SurfaceUpdates(NamedTuple):
    name: str
    delta: float


def collect_domain_changes(axgraph: AxGraph, domain_name: str, nb_pairs: GraphPairs):
    # assumming all surfaces that are keys are for the same domain.., this could be a good place to check if have issues!
    updates: list[SurfaceUpdates] = []
    for surface, nbs in nb_pairs.items():
        deltas = [axgraph.get_delta(surface, nb) for nb in nbs]
        print(domain_name)
        print(deltas)
        # going to take the largest collect_domain_changes
        true_delta = max(deltas)
        updates.append(SurfaceUpdates(surface, true_delta))
    domain = deepcopy(axgraph.layout.get_domain(domain_name))
    for update in updates:
        try:
            surface = axgraph.layout.get_surface_by_name(update.name)
        except AssertionError:
            warn(
                f"Ran into an error while looking for a domain surface:{update.name}. Skipping... "
            )
            domain.summarize_surfaces
            continue
            # raise Exception(
            #     f"Could not find {update.name} in surfaces of {domain.name}: Error {e}"
            # )
        domain = update_domain(Move(domain, surface, update.delta))

    return domain


def filter_nb_pairs(nb_pairs: GraphPairs, keys: list[str]) -> GraphPairs:
    return {k: v for k, v in nb_pairs.items() if k in keys}


def collect_updated_domains(axgraph: AxGraph):
    edges_for_domain = sort_and_group_objects_dict(
        axgraph.G.edge_data(), fx=lambda x: x.data.domain_name
    )

    domain_and_surfaces = {
        domain_name: [i.u for i in matching_edges]
        for domain_name, matching_edges in edges_for_domain.items()
    }

    domain_and_nb_pairs = {
        domain_name: filter_nb_pairs(axgraph.nb_pairs, domain_surfs_to_move)
        for domain_name, domain_surfs_to_move in domain_and_surfaces.items()
    }

    updated_domains = [
        collect_domain_changes(axgraph, domain_name, nb_pairs)
        for domain_name, nb_pairs in domain_and_nb_pairs.items()
    ]
    return updated_domains


def create_updated_layout(axgraph: AxGraph):
    new_doms = collect_updated_domains(axgraph)
    unchanged_doms = get_unchanged_domains(axgraph.layout, new_doms)

    return Layout(unchanged_doms + new_doms)
