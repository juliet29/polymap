# validation

from loguru import logger
from utils4plans import logconfig
from polymap.geometry.modify.validate import (
    validate_layout_no_holes,
)
from polymap.pydantic_models import read_layout_from_path
from polymap.paths import DynamicPaths


class StudyValidation:
    bad_case = "71308"
    good_case = "27540"
    ymove = "ymove/out.json"
    path = DynamicPaths.msd_outputs / bad_case / ymove

    @property
    def layout(self):
        return read_layout_from_path(self.path)

    def try_validate_no_holes(self):
        res = validate_layout_no_holes(self.layout)
        logger.info(res)

    # def try_validate_no_overlaps(self):
    #     validate_layout_domain(self.layout)


if __name__ == "__main__":

    logconfig.logset()
    s = StudyValidation()
