from pathlib import Path
from loguru import logger
from rich.pretty import pretty_repr
from polymap import logconf
from polymap.bends.iterate2 import clean_layout
from polymap.json_interfaces import read_layout_from_path
from polymap.process.process import make_ortho_layout
from polymap.rotate.rotate import rotate_layout
from cyclopts import App

app = App()


@app.command()
def rotate(path: Path):
    in_layout = read_layout_from_path(path)

    angle, layout = rotate_layout(in_layout)
    logger.info(f"{angle=}")

    return layout.dump()


@app.command()
def ortho(path: Path):
    in_layout = read_layout_from_path(path)
    layout = make_ortho_layout(in_layout)
    return layout.dump()


@app.command()
def simplify(path: Path):
    in_layout = read_layout_from_path(path)
    layout, bad_doms = clean_layout(in_layout, path.stem)
    if bad_doms:
        logger.warning(
            f"Bad domains exist which may cause problems: {pretty_repr(bad_doms)}"
        )
    return layout.dump()


@app.command()
def pull(path: Path):
    pass


@app.command()
def welcome():
    return "Hello old friend"


def main():
    logconf.logset()
    app()


if __name__ == "__main__":
    main()
