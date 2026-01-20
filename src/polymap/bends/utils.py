from loguru import logger
from polymap.geometry.modify.update import Move, update_domain
from polymap.geometry.modify.validate import InvalidPolygonError
from polymap.geometry.ortho import FancyOrthoDomain
from polymap.geometry.surfaces import Surface


TOLERANCE = 0.13  # TODO: make a constant


def apply_move(moves: list[Move]) -> FancyOrthoDomain:
    new_dom = None

    if len(moves) == 1:
        new_dom = update_domain(moves[0])
        return new_dom

    for ix, m in enumerate(moves):
        try:
            new_dom = update_domain(m)
        except InvalidPolygonError as e:
            if ix == len(moves) - 1:
                raise InvalidPolygonError(e.p, e.domain_name, e.reason)
            else:
                logger.warning(e.message())
                continue
    assert new_dom
    return new_dom


def is_small_surf(surf: Surface, tolerance: float = TOLERANCE):
    return surf.range.size <= tolerance


def find_small_surfs(domain: FancyOrthoDomain, tolerance: float = TOLERANCE):
    small_surfs = list(filter(lambda x: is_small_surf(x, tolerance), domain.surfaces))
    return small_surfs
