from loguru import logger
from rich.logging import RichHandler
from rich.console import Console

DEBUG_LEVEL = "TRACE"

HANDLERS = [
    {
        "sink": RichHandler(
            markup=True, show_time=False, show_path=False, console=Console(stderr=True)
        ),
        "format": "<cyan>{level.icon}</cyan>:<cyan>{name}</cyan>:<cyan>{function}</cyan>:<cyan>{line}</cyan> | {message}",
    }
]


def logset():
    logger.remove()
    logger.level("START", no=22, color="<CYAN>", icon="▶▶▶▶▶▶")
    logger.level("END", no=22, color="<CYAN>", icon="◀◀◀◀◀◀")
    logger.level("SUMMARY", no=27, color="<YELLOW>", icon="%")
    # logger.add(level=DEBUG_LEVEL, **HANDLERS[0])
    logger.add(level=DEBUG_LEVEL, **HANDLERS[0])

    # TODO figure out logging to individual files for each.. or snakemake..
