from polymap.examples.layout import layout_coords as sample_layout
from polymap.geometry.layout import create_layout_from_dict


def test_get_surface_in_layout():
    layout = create_layout_from_dict(sample_layout)
    surf = layout.get_domain("red").get_surface("south", 1)
    assert surf.location == 4
    assert surf.range.as_tuple == (2, 4)


def test_get_surface_by_name():
    layout = create_layout_from_dict(sample_layout)
    res = layout.get_surface_by_name("pink-north_0")
    assert str(res) == "pink-north_0"
