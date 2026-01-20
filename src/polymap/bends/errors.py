from polymap.geometry.ortho import FancyOrthoDomain

from polymap.bends.interfaces import Bend, BendHolder
from polymap.geometry.surfaces import Surface
from typing import Literal

from loguru import logger

FAIL_TYPES = Literal[
    "Invalid Move",
    "Problem Finding Bends",
    "Failed to Clean Domain Correctly",
    "Invalid Incoming Domain",
    "Exceeded number of iterations",
]


class DomainCleanFailure(Exception):
    def __init__(
        self,
        domain: FancyOrthoDomain,
        fail_type: FAIL_TYPES,
        details: str,
        surfaces: list[Surface] = [],
        bends: BendHolder | None = None,
        current_bend: Bend | None = None,
    ):
        self.domain = domain
        self.fail_type = fail_type
        self.details = details
        self.surfaces = surfaces
        self.bends = bends
        self.current_bend = current_bend

    def __rich_repr__(self):
        yield "domain", self.domain.name
        yield "fail_type", self.fail_type
        yield "details", self.details

    def show_message(self, layout_id: str):
        logger.warning(f"[red bold]{self.fail_type} for {layout_id}-{self.domain.name}")
        logger.warning(f"{self.details}")

        if self.bends:
            logger.warning(self.bends.summary_str)

        if self.current_bend:
            logger.warning(f"Current bend is {str(self.current_bend)}")
            logger.warning(self.current_bend.study_vectors())


class DomainCleanIterationFailure(Exception):
    def __init__(
        self, domain_name: str, fail_type: FAIL_TYPES, current_bend: Bend | None = None
    ):
        self.domain = domain_name
        self.fail_type = fail_type
        self.current_bend = current_bend

    def message(self):
        logger.warning(f"[red bold]{self.fail_type} for {self.domain}")
