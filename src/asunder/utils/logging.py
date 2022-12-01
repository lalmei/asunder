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
    
    rich_handler = RichHandler(rich_tracebacks=True, console=console)
    rich_handler.set_name("rich")
    module_logger.addHandler(rich_handler)
    module_logger.setLevel(level=WARNING)

    return module_logger


def get_logger_console(
    console: Optional[Console] = None,
) -> tuple[Logger, Console]:

    if not console:
        console = Console()

    logger = getLogger("asunder")

    if len(logger.handlers) > 0:
        if logger.handlers[0].get_name() == "rich":
            handler: RichHandler = cast(RichHandler, logger.handlers[0])
            console = handler.console
            return logger, console
        
    logger = _set_up_logger(console)
    logger.debug("Setting up rich log handler")

    return logger, console
