from cyclopts import App

from polymap.cli.studies.study_msd import StudyMSDBends

from pathlib import Path

from loguru import logger
from utils4plans.io import read_json
from polymap.pydantic_models import AxGraphModel
from polymap.layout.main.move import try_moves


from utils4plans.io import write_json

from polymap.examples.layout import example_layouts
from polymap.geometry.layout import create_layout_from_dict
from polymap.paths import DynamicPaths


studies_app = App(name="studies")


@studies_app.command()
def generate_examples():
    for ix, coords in enumerate(example_layouts):
        layout = create_layout_from_dict(coords)
        path = DynamicPaths.example_paths / f"{1000 + ix}.json"
        write_json(layout, path)


@studies_app.command()
def report_bends_on_msd():
    # TODO: possible to pass debug level to main caller?
    s = StudyMSDBends()
    s.study_moves_all_domain()


@studies_app.command()
def trial_move(path: Path):
    logger.info(path)
    Gax = AxGraphModel.model_validate(read_json(path)).to_axgraph()
    try_moves(Gax)
