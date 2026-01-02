from loguru import logger
from rich.logging import RichHandler

DEBUG_LEVEL = "START"

HANDLERS = [
    {
        "sink": RichHandler(markup=True, show_time=False),
        "format": "<cyan>{name}</cyan>:<cyan>{function}</cyan>:<cyan>{line}</cyan> | {message}",
    }
]


def logset():
    logger.remove()
    logger.level("START", no=22, color="<CYAN>", icon="*")
    logger.level("END", no=22, color="<CYAN>", icon="*")
    logger.level("SUMMARY", no=27, color="<YELLOW>", icon="%")
    logger.add(level=DEBUG_LEVEL, **HANDLERS[0])

    # TODO figure out logging to individual files for each.. or snakemake..
