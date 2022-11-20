"""
A typer CLI application.

It uses rich for object printing format, along with hydra for configuration
"""
import logging
from typing import Optional

import typer
from rich import box
from rich.console import Console
from rich.logging import RichHandler
from rich.panel import Panel

from asunder._version import version_info
from asunder.command.rename import app as refactor

app = typer.Typer(add_completion=False, invoke_without_command=True, no_args_is_help=True)

app.add_typer(refactor,name= "refactor")

def _set_up_logger(console: Console) -> logging.Logger:
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
    module_logger = logging.getLogger("asunder")
    module_logger.addHandler(RichHandler(rich_tracebacks=True, console=console))
    module_logger.setLevel(level=logging.WARNING)

    return module_logger


def _version_callback(value: bool) -> None:
    """
    Print model version information.

    Parameters
    ----------
    value: bool
        Whether to print version information
    """
    if value:
        console = Console()
        console.print(
            Panel(version_info(), highlight=True, box=box.DOUBLE_EDGE, title="asunder version info")
        )
        raise typer.Exit()


@app.callback(invoke_without_command=True, no_args_is_help=True)
def main(
    ctx: typer.Context,
    dry_run : Optional[bool] = typer.Option(False, "--dry-run", help = "Show changes but do not execute them"),
    verbose: Optional[bool] = typer.Option(False, "--verbose", help="verbose mode"),
    version: Optional[bool] = typer.Option(None, "--version", help="check model version", callback=_version_callback),
) -> None:
    """
    Welcome to Asunder App
    
    To help you refactor and break apart your code.
    \f

    Parameters
    ----------
    ctx : typer.Context
        typer context that lives throughtout model command
    verbose : Optional[bool]
        set logging to DEBUG , by default typer.Option(False, "--verbose", help="verbose mode")
        it is also saved in the ctx obj so it can be referred for other noisy output
    version : Optional[bool]
        outputs version information, by default typer.Option(None, "--version",
        help="check model version", callback=_version_callback)

    """
    console = Console()
    logger = _set_up_logger(console)

    if verbose:
        logger.setLevel(logging.DEBUG)
        logger.info("Setting verbose mode ON")

    ctx.obj = {"verbose": verbose, "dry_run": dry_run}
