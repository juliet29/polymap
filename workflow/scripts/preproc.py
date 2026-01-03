from pathlib import Path
from loguru import logger
from polymap import logconf
from polymap.json_interfaces import read_layout_from_path
from polymap.rotate.rotate import rotate_layout
from cyclopts import App

app = App()


@app.command()
def rotate(path: Path):
    logconf.logset()
    layout = read_layout_from_path(path)

    angle, layout = rotate_layout(layout)
    logger.info(f"{angle=}")

    return layout.dump()


@app.command()
def welcome():
    return "Hello old friend"


app()
