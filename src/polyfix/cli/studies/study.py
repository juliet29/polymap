from cyclopts import App
from utils4plans.logs import logset

from polyfix.cli.studies.reconcile import rec

app = App()
app.command(rec)


def main():
    logset(to_stderr=False)
    app()


if __name__ == "__main__":
    main()
