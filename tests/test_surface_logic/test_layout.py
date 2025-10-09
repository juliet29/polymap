from polymap.layout.interfaces import (
    create_layout_from_dict,
)
from polymap.layout.neighbors import get_candidate_surface_neighbors, get_nbs_for_surf
from polymap.examples.layout import layout as sample_layout
from rich import print
from polymap.layout.graph import (
    create_graph_for_surface,
    create_graph_for_all_surfaces_along_axis,
    collect_node_nbs,
)
import pytest


def test_get_surface_in_layout():
    layout = create_layout_from_dict(sample_layout)
    surf = layout.get_domain("red").get_surface("south", 1)
    assert surf.location == 4
    assert surf.range.as_tuple == (2, 4)


def test_get_surface_by_name():
    layout = create_layout_from_dict(sample_layout)
    res = layout.get_surface_by_name("pink-north_0")
    assert str(res) == "pink-north_0"


def test_candidate_nbs():
    layout = create_layout_from_dict(sample_layout)
    surf = layout.get_domain("red").get_surface("south", 1)
    candidate_nbs = get_candidate_surface_neighbors(layout, surf)
    assert set([i.domain_name for i in candidate_nbs]) == set(["blue", "green", "pink"])


nbs_group: list[tuple[str, set]] = [
    ("red-south_0", {"yellow-north_0"}),
    ("red-south_1", {'green-north_1', 'pink-north_0'}),
    ("yellow-south_0", {"blue-north_0"}),
    ("green-south_0", {"blue-north_0"}),
    ("pink-south_0", {"green-north_0"}),
    # TODO add x
]

@pytest.fixture
def get_nbs_dict():
    layout = create_layout_from_dict(sample_layout)
    Gy = create_graph_for_all_surfaces_along_axis(layout, "Y")
    return collect_node_nbs(Gy)


@pytest.mark.parametrize("node, nbs", nbs_group)
def test_layout_nbs(get_nbs_dict, node, nbs ):
    nbs_dict = get_nbs_dict
    assert nbs_dict[node] == nbs

def test_layout_nodes(get_nbs_dict ):
    nbs_dict = get_nbs_dict
    nodes = set(nbs_dict.keys())
    expected_nodes = {i[0] for i in nbs_group}
    assert nodes == expected_nodes


if __name__ == "__main__":
    pass
    # layout = create_layout_from_dict(sample_layout)
    # surf = layout.get_domain("red").get_surface("south", 1)
    # nbs = get_nbs_for_surf(layout, surf)
    # g = create_graph_for_surface(surf, nbs)
