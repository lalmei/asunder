from logging import Logger, getLogger
from typing import cast

from rich.console import Console
from rich.logging import RichHandler


def get_logger_console() -> tuple[Logger, Console]:

    logger = getLogger("asunder")

    if len(logger.handlers) > 0:

        handler: RichHandler = cast(RichHandler, logger.handlers[0])
        console = handler.console
        print("handler names = ", [handle.__dict__ for handle in logger.handlers])
    else:
        raise AttributeError("No Handlers in logger")

    return logger, console
