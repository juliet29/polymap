import shapely as sp
from utils4plans.geom import CoordsList
from utils4plans.lists import get_unique_items_in_list_keep_order

from polyfix.geometry.modify.update import Move, apply_vector_to_paired_coord
from polyfix.geometry.modify.validate import InvalidPolygonError, validate_polygon
from polyfix.geometry.ortho import FancyOrthoDomain
from polyfix.geometry.paired_coords import PairedCoord
from polyfix.geometry.shapely_helpers import get_coords_from_shapely_polygon
from polyfix.geometry.vectors import (
    is_perpendicular,
    make_vector_2D,
    vector_from_coords,
)


def edge_vector(pc: PairedCoord):
    return vector_from_coords(*pc, _2D=True)


def move_segment(move: Move) -> FancyOrthoDomain:
    domain, surface, delta = move
    vector = make_vector_2D(surface.positive_perpendicular_vector) * delta

    pcs = domain.paired_coords
    target = surface.coords
    ix = pcs.index(target)
    n = len(pcs)
    alpha, beta = pcs[(ix - 1) % n], pcs[(ix + 1) % n]

    tvec = edge_vector(target)
    alpha_perp = is_perpendicular(edge_vector(alpha), tvec)
    beta_perp = is_perpendicular(edge_vector(beta), tvec)

    moved = apply_vector_to_paired_coord(target, vector)
    left = [moved.first] if alpha_perp else [target.first, moved.first]
    right = [moved.last] if beta_perp else [moved.last, target.last]

    verts = [pc.first for pc in pcs]
    new_verts = []
    for k in range(n):
        if k == ix:
            new_verts.extend(left)
        elif k == (ix + 1) % n:
            new_verts.extend(right)
        else:
            new_verts.append(verts[k])

    tuple_list = get_unique_items_in_list_keep_order(CoordsList(new_verts).tuple_list)
    try:
        test_poly = sp.Polygon(tuple_list)
    except ValueError as e:
        raise InvalidPolygonError(sp.Polygon(), domain.name, f"{tuple_list}: {e}")

    validate_polygon(test_poly, domain.name)
    return FancyOrthoDomain(
        coords=get_coords_from_shapely_polygon(test_poly), name=domain.name
    )
