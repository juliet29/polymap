from loguru import logger
from rich.logging import RichHandler

DEBUG_LEVEL = "SUCCESS"

HANDLERS = [
    {
        "sink": RichHandler(markup=True, show_time=False),
        "format": "<cyan>{name}</cyan>:<cyan>{function}</cyan>:<cyan>{line}</cyan> | {message}",
    }
]


def logset():
    logger.remove()
    logger.add(level=DEBUG_LEVEL, **HANDLERS[0])
