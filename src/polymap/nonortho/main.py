from loguru import logger
from polymap.geometry.modify.validate import InvalidPolygonError
from polymap.geometry.ortho import FancyOrthoDomain
from polymap.geometry.layout import Layout
from polymap.nonortho.dot import make_ortho_coords


def orthogonalize_dom(dom: FancyOrthoDomain):
    with logger.contextualize(name=dom.name):
        if not dom.is_orthogonal:
            logger.info(f"Resolving non-ortho on {dom.name}")
            coords = make_ortho_coords(dom.normalized_coords, dom.vectors)

            new_dom = FancyOrthoDomain(coords, name=dom.name)
            try:
                assert new_dom.is_orthogonal
            except AssertionError:
                raise InvalidPolygonError(new_dom.polygon, dom.name, "NOT ORTHOGONAL")
            logger.info(f"Finished resolving non-ortho on {dom.name}\n")
            return new_dom

        logger.trace(f"No non-ortho on {dom.name}\n")
    return dom


def orthogonalize_layout(layout: Layout):
    new_doms = map(lambda x: orthogonalize_dom(x), layout.domains)
    return Layout(list(new_doms))
