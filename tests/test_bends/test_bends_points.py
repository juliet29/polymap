from utils4plans.sets import set_equality
import pytest
from polymap.bends.points import (
    find_new_surf_for_vector_group,
    find_vector_groups_on_domain,
    fix_vector_group_on_domain,
    heal_extra_points_on_domain,
)
from polymap.examples.domains import OrthoNames, create_ortho_domain
from rich import print

from polymap.geometry.modify.update import validate_polygon

# TODO: move to tests!


def test_find_vector_groups():
    domain = create_ortho_domain("SQUARE_W_EXTRA_POINTS")
    result = find_vector_groups_on_domain(domain)
    group_names = list(map(lambda x: tuple(i.name for i in x), result))
    print(group_names)

    expected_groups = [("north_0", "north_1"), ("east_0",), ("south_0",), ("west_0",)]
    assert set_equality(group_names, expected_groups)


def test_create_new_surf():
    domain = create_ortho_domain("SQUARE_W_EXTRA_POINTS")
    surfs = [domain.get_surface("north", i) for i in [0, 1]]
    new_surf = find_new_surf_for_vector_group(surfs, "")
    coords = [i.as_tuple for i in new_surf.coords.as_list]

    expected_coords = [(0, 1), (1, 1)]

    assert coords == expected_coords


def test_remove_extra_point_from_domain():
    domain = create_ortho_domain("SQUARE_W_EXTRA_POINTS")
    og_surf_names = [i.name_w_domain for i in domain.surfaces]
    print(og_surf_names)
    surfs = [domain.get_surface("north", i) for i in [0, 1]]
    new_domain = fix_vector_group_on_domain(domain, surfs)
    new_surf_names = [i.name_w_domain for i in new_domain.surfaces]

    og_surf_names.remove("-north_1")
    assert og_surf_names == new_surf_names

    assert new_domain.is_orthogonal
    validate_polygon(new_domain.polygon, new_domain.name)

    print(new_surf_names)


domain_names: list[OrthoNames] = ["SQUARE_W_EXTRA_POINTS", "SQUARE_EXTRA_WEST"]


@pytest.mark.parametrize("domain_name", domain_names)
def test_heal_north(domain_name):
    domain = create_ortho_domain(domain_name)
    new_domain = heal_extra_points_on_domain(domain)
    assert len(new_domain.surfaces) == 4
    assert new_domain.is_orthogonal
    validate_polygon(new_domain.polygon, new_domain.name)


def test_extra_points():
    domain = create_ortho_domain("SQUARE_EXTRA_NORTH_WEST")
    with pytest.raises(Exception):
        heal_extra_points_on_domain(domain)


if __name__ == "__main__":
    test_remove_extra_point_from_domain()
