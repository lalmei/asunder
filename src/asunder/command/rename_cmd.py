import logging
import os
from pathlib import Path

import typer
from typer import Context

from asunder.project import Project
from asunder.rope import rename
from asunder.utils.logging import get_logger_console

app = typer.Typer(add_completion=True, no_args_is_help=True)
logger = logging.getLogger("asunder")


@app.command(no_args_is_help=True)
def module(
    ctx: Context,
    path: Path = typer.Option(Path.cwd() / "src", help="path to package source code"),
    module: str = typer.Argument(
        "", help='full module name to be renamed, e.g. "package.module"'
    ),
    name: str = typer.Argument("", help="new module name only"),
) -> None:

    dry_run = ctx.obj.get("dry_run", True)

    logger, console = get_logger_console()

    project = Project(path=Path.cwd(), console=console)

    # module to folder
    module = os.path.join(*module.split("."))
    name = os.path.join(*name.split("."))

    logger.info("Calculating Changes")
    # compute changes needed
    changes = rename(project.rope_project, module, name)

    if not dry_run:
        logger.info("Perfoming  Changes")
    # perfom changes
    project.perform_changes(changes, dry_run)

    typer.Exit()
