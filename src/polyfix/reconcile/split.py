from utils4plans.geom import Coord
from utils4plans.lists import pairwise

from polyfix.geometry.ortho import FancyOrthoDomain
from polyfix.geometry.paired_coords import (
    PairedCoord,
    coords_from_paired_coords_list,
)
from polyfix.geometry.surfaces import Surface
from polyfix.geometry.vectors import Axes


def axis_value(coord: Coord, ax: Axes) -> float:
    return coord.x if ax == "X" else coord.y


def coord_on_axis(pos: float, location: float, ax: Axes) -> Coord:
    return Coord(pos, location) if ax == "X" else Coord(location, pos)


def split_surface(
    domain: FancyOrthoDomain, surface: Surface, at: list[float]
) -> FancyOrthoDomain:
    ax = surface.parallel_axis
    rng = surface.range
    positions = sorted(set(at))
    assert positions, "no split positions given"
    assert all(rng.min < p < rng.max for p in positions), (
        f"split positions {positions} must lie strictly within {rng} of {surface.name_w_domain}"
    )

    pcs = domain.paired_coords
    target = surface.coords
    try:
        ix = pcs.index(target)
    except ValueError:
        raise ValueError(
            f"{surface.name_w_domain} is not an edge of domain {domain.name}"
        )

    first, last = target
    ascending = axis_value(last, ax) > axis_value(first, ax)
    ordered = positions if ascending else list(reversed(positions))
    verts = [first, *[coord_on_axis(p, surface.location, ax) for p in ordered], last]
    sub_pcs = [PairedCoord(a, b) for a, b in pairwise(verts)]

    new_pcs = pcs[:ix] + sub_pcs + pcs[ix + 1 :]
    coords = coords_from_paired_coords_list(new_pcs)
    return FancyOrthoDomain(coords=coords, name=domain.name)
