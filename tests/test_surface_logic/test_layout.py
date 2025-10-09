from polymap.geometry.layout import (
    create_layout_from_dict,
    get_candidate_surface_neighbors,
)
from polymap.examples.layout import layout as sample_layout
from rich import print


def test_get_surface_in_layout():
    layout = create_layout_from_dict(sample_layout)
    surf = layout.get_domain("red_l").get_surface("south", 1)
    assert surf.location == 4
    assert surf.range.as_tuple == (2, 4)


def test_candidate_nbs():
    layout = create_layout_from_dict(sample_layout)
    surf = layout.get_domain("red_l").get_surface("south", 1)
    candidate_nbs = get_candidate_surface_neighbors(layout, surf)
    assert set([i.domain_name for i in candidate_nbs]) == set(
        ["blue_rect", "green_l", "pink_rect"]
    )


if __name__ == "__main__":
    test_get_surface_in_layout()
