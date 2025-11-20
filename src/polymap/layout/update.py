from utils4plans.sets import set_difference
from rich import print
from polymap.geometry.ortho import FancyOrthoDomain
from polymap.geometry.update import update_domain
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


def handle_nb(axgraph: AxGraph, root: str, nb: str):
    layout = axgraph.layout
    surface = layout.get_surface_by_name(nb)
    domain = layout.get_domain(surface.domain_name)
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
