from itertools import combinations

from loguru import logger
from polymap.config import PRECISION
import shapely as sp
from polymap.geometry.layout import Layout
from polymap.geometry.modify.validate import InvalidPolygonError, validate_polygon
from polymap.geometry.ortho import FancyOrthoDomain
from polymap.geometry.shapely_helpers import (
    decrease_precision,
    get_coords_from_shapely_polygon,
)


def decrease_domain_precision(domain: FancyOrthoDomain, precision: int = PRECISION):
    new_poly = decrease_precision(domain.polygon, precision)
    if isinstance(new_poly, sp.Polygon):
        validate_polygon(new_poly, domain.name)
    else:
        raise InvalidPolygonError(
            new_poly,  # pyright: ignore[reportArgumentType]
            domain.name,
            f"Could not decrease precision to {precision} digits.",
        )

    coords = get_coords_from_shapely_polygon(new_poly)
    new_dom = FancyOrthoDomain(coords, domain.name)
    return new_dom


def precision_decrease_is_ok(combos: list[tuple[str, str]], l1: Layout, l2: Layout):
    def get_relation(layout: Layout, a: str, b: str):
        da, db = layout.get_domain(a), layout.get_domain(b)
        return sp.relate(da.polygon, db.polygon)

    def check_relation(l1: Layout, l2: Layout, combo: tuple[str, str]):
        r1 = get_relation(l1, *combo)
        r2 = get_relation(l2, *combo)
        if r1 == r2:
            return True
        else:
            a, b = combo
            logger.warning(
                f"{a}: {r1} | {b}: {r2} DON'T MACTCH - Increasing precision,..."
            )
            return False

    for combo in combos:
        if not check_relation(l1, l2, combo):
            return False
    return True


def decrease_layout_precision(layout: Layout, precision: int = PRECISION):
    def decrease(layout: Layout, curr_precision: int):
        new_doms = [
            decrease_domain_precision(dom, curr_precision) for dom in layout.domains
        ]
        return Layout(new_doms)

    combos = list(combinations([i.name for i in layout.domains], 2))

    new_layout = decrease(layout, precision)
    while not precision_decrease_is_ok(combos, layout, new_layout):
        precision += 1
        new_layout = decrease(layout, precision)

        MAX_PREC = 10

        if precision > MAX_PREC:
            raise RuntimeError(
                f"Having a difficult time decreasing precision - now {precision} is > {MAX_PREC}"
            )

    logger.info(f"New precision is {precision}")
    return new_layout
