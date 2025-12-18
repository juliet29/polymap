from loguru import logger
from rich.logging import RichHandler


def logset():
    logger.remove()
    logger.configure(
        handlers=[
            {
                "sink": RichHandler(markup=True, show_time=False),
                "format": "<cyan>{name}</cyan>:<cyan>{function}</cyan>:<cyan>{line}</cyan> | {message}",
            }
        ]
    )
