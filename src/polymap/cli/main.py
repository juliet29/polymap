from cyclopts import App
from utils4plans import logconfig

from polymap.cli.make.main import make_app

# from polymap.cli.studies.main import studies_app

# TODO: clean up imports to clean up project structure

app = App()
app.command(make_app)
# app.command(studies_app)


@app.command()
def welcome():
    return "Welcome to polymap"


def main():
    logconfig.logset(to_stderr=True)
    app()


if __name__ == "__main__":
    main()
