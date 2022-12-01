from logging import WARNING, Logger, getLogger
from typing import Optional, cast

from rich.console import Console
from rich.logging import RichHandler


def _set_up_logger(console: Optional[Console] = None) -> Logger:
    """
    Log to console with a simple formatter; used by CLI

    Parameters
    ----------
    console : Console
        rich console with style and colored

    Returns
    -------
    logging.Logger
        logger with the CLI name

    """
    if not console:
        console = Console()
    module_logger = getLogger("asunder")
    module_logger.addHandler(RichHandler(rich_tracebacks=True, console=console))
    module_logger.setLevel(level=WARNING)

    return module_logger


def get_logger_console(
    console: Optional[Console] = None,
) -> tuple[Logger, Console]:

    if not console:
        console = Console()

    logger = getLogger("asunder")

    if len(logger.handlers) > 0:
        handler: RichHandler = cast(RichHandler, logger.handlers[0])
        console = handler.console
        print(
            "handler names = ", [handle.__dict__ for handle in logger.handlers]
        )
    else:
        logger = _set_up_logger(console)
        logger.debug("Setting up rich log handler")

    return logger, console
