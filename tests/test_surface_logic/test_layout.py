import pytest
from rich import print

from polymap.examples.layout import layout as sample_layout
from polymap.geometry.vectors import Axes
from polymap.layout.graph import (
    collect_node_nbs,
    create_graph_for_all_surfaces_along_axis,
    create_graph_for_surface,
)
from polymap.layout.interfaces import create_layout_from_dict
from polymap.layout.neighbors import get_candidate_surface_neighbors, get_nbs_for_surf


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


nbs_group: list[tuple[Axes, str, set]] = [
    ("Y", "red-south_0", {"yellow-north_0"}),
    ("Y", "red-south_1", {"green-north_1", "pink-north_0"}),
    ("Y", "yellow-south_0", {"blue-north_0"}),
    ("Y", "green-south_0", {"blue-north_0"}),
    ("Y", "pink-south_0", {"green-north_0"}),
    ("X", "green-west_0", {"yellow-east_0", "red-east_0"}),
    ("X", "pink-west_0", {"green-east_0"}),
    # TODO add x
]


@pytest.fixture
def get_nbs_dict():
    layout = create_layout_from_dict(sample_layout)
    Gx = create_graph_for_all_surfaces_along_axis(layout, "X")
    Gy = create_graph_for_all_surfaces_along_axis(layout, "Y")
    return collect_node_nbs(Gx.G), collect_node_nbs(Gy.G)


@pytest.mark.parametrize("ax, node, nbs", nbs_group)
def test_layout_nbs(get_nbs_dict, ax, node, nbs):
    nbs_dict_x, nbs_dict_y = get_nbs_dict
    if ax == "X":
        assert nbs_dict_x[node] == nbs
    if ax == "Y":
        assert nbs_dict_y[node] == nbs


@pytest.mark.parametrize("ax", ["X", "Y"])
def test_layout_nodes(get_nbs_dict, ax):
    nbs_dict_x, nbs_dict_y = get_nbs_dict
    if ax == "X":
        nodes = set(nbs_dict_x.keys())
    else:
        nodes = set(nbs_dict_y.keys())
    expected_nodes = {i[1] for i in nbs_group if i[0] == ax}
    assert nodes == expected_nodes


def test_update_layout():
    layout = create_layout_from_dict(sample_layout)
    blue = layout.get_domain("blue").update_surface_by_direction(
        "south", 0, location_delta=-2
    )
    yellow = layout.get_domain("yellow").update_surface_by_direction(
        "west", 0, location_delta=-2
    )

    new_layout = layout.update_layout([blue, yellow])
    print(new_layout)
    assert new_layout.get_domain("blue").get_surface("south").location == -1
    assert new_layout.get_domain("yellow").get_surface("west").location == -1


# def test_set_update():
#     lst = [0, 1, 2]
#     new_lst = [10, 100, 1]
#     expected_list = [0, 1, 2, 10, 100]
#     assert set(expected_list) == set(set_update(lst, new_lst))


if __name__ == "__main__":
    test_update_layout()
    # layout = create_layout_from_dict(sample_layout)
    # surf = layout.get_domain("red").get_surface("south", 1)
    # nbs = get_nbs_for_surf(layout, surf)
    # g = create_graph_for_surface(surf, nbs)
