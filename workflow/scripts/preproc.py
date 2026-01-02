from pathlib import Path
from polymap.layout.interfaces import create_layout_from_path
from polymap.rotate.rotate import rotate_layout
from cyclopts import App

app = App()


@app.command()
def rotate(path: Path):
    layout = create_layout_from_path(path)  # make this more flexible using Pydantic

    angle, layout = rotate_layout(layout)
    print(f"{angle=}")

    return layout


@app.command()
def welcome():
    return "Hello friend"


app()
