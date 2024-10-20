"""
A typer CLI application.

It uses rich for object printing format, along with hydra for configuration
"""

import logging
from typing import Optional

import typer
from rich import box
from rich.console import Console
from rich.panel import Panel

from asunder._version import version_info
from asunder.command.analyze import app as analyze
from asunder.command.report import app as report
from asunder.command.extract import app as extract

from asunder.utils.logging import get_logger_console

app = typer.Typer(add_completion=True, invoke_without_command=True, no_args_is_help=True)

app.add_typer(analyze, name="analyze")
app.add_typer(report, name="report")
app.add_typer(extract, name="extract")


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
            Panel(
                version_info(),
                highlight=True,
                box=box.DOUBLE_EDGE,
                title="asunder version info",
            )
        )
        raise typer.Exit()


@app.callback(invoke_without_command=True, no_args_is_help=True)
def main(
    ctx: typer.Context,
    dry_run: Optional[bool] = typer.Option(False, "--dry-run", help="Show changes but do not execute them"),
    verbose: Optional[bool] = typer.Option(False, "--verbose", help="verbose mode"),
    version: Optional[bool] = typer.Option(
        None,
        "--version",
        help="check model version",
        callback=_version_callback,
    ),
) -> None:
    """
    Welcome to Asunder App

    To help you refactor and break apart your code.
    \f

    Parameters
    ----------
    ctx : typer.Context
        typer context that lives throughout model command
    verbose : Optional[bool]
        set logging to DEBUG , by default typer.Option(False, "--verbose", help="verbose mode")
        it is also saved in the ctx obj so it can be referred for other noisy output
    version : Optional[bool]
        outputs version information, by default typer.Option(None, "--version",
        help="check model version", callback=_version_callback)

    """

    logger, console = get_logger_console()

    if verbose:
        logger.setLevel(logging.DEBUG)
        logger.info("Setting verbose mode ON")

    ctx.obj = {"verbose": verbose, "dry_run": dry_run}
