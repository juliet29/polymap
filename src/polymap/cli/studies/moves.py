from pathlib import Path

from loguru import logger
from utils4plans.io import read_json
from polymap.cli.studies.main import studies_app
from polymap.json_interfaces import AxGraphModel
from polymap.layout.main.move import try_moves


@studies_app.command()
def trial_move(path: Path):
    logger.info(path)
    Gax = AxGraphModel.model_validate(read_json(path)).to_axgraph()
    try_moves(Gax)
