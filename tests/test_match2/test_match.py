import networkx as nx
from utils4plans.sets import set_equality

from polymap.examples.msd import get_one_msd_layout
from polymap.geometry.surfaces import print_surfaces
from polymap.layout.neighbors import get_nbs_for_surf

MSD_NUM = 106493


class MSDPairs:
    _106493 = {
        "balcony_0-east_1": ["living_room_8-west_0"],
        "living_room_8-east_0": ["kitchen_7-west_1"],
        "living_room_8-east_2": ["kitchen_7-west_0"],
        "living_room_8-east_1": ["kitchen_7-west_2", "corridor_2-west_2"],
        "bedroom_4-east_0": ["corridor_2-west_2"],
        "bedroom_6-east_0": ["corridor_2-west_0", "storeroom_1-west_0"],
    }  # TODO: should check that these are all actualy in the layout, in case of typos..


def make_graphs(inp: dict[str, list[str]]):
    graphs = []
    for k, values in inp.items():
        G = nx.DiGraph()
        for item in values:
            G.add_edge(k, item)
        graphs.append(G)

    Gf = nx.compose_all(graphs)
    return Gf


def test_get_candidates():
    _, layout = get_one_msd_layout(MSD_NUM)
    surf_name = list(MSDPairs._106493.keys())[0]
    surf_name = "balcony_0-east_1"
    surf = layout.get_surface_by_name(surf_name)

    for k, v in MSDPairs._106493.items():
        surf = layout.get_surface_by_name(k)
        res = get_nbs_for_surf(layout, surf)
        assert set_equality(
            v, print_surfaces(res)
        ), f"Wrong surfs for {k}: {print_surfaces(res)}. Expeceted {v}"


if __name__ == "__main__":
    # graph = make_graphs(msd_106493)
    test_get_candidates()
