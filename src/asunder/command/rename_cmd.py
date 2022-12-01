import logging
import os
from pathlib import Path
from typing import Optional

import typer
from typer import Context

from asunder.project import Project
from asunder.rope_sdk import rename as rename_changes
from asunder.utils.logging import get_logger_console

app = typer.Typer(add_completion=True, no_args_is_help=True)

logger = logging.getLogger("asunder")


@app.command(no_args_is_help=True)
def rename(
    ctx: Context,
    path: Path = typer.Option(Path.cwd() / "src", help="path to package source code"),
    module: str = typer.Argument(
        "", help='module where renaming will take placed, e.g. "package.module"'
    ),
    old_name: Optional[str] = typer.Option("", help= "old name of module/class/attribute"),
    name: str = typer.Argument("", help="new module/class/attribute name"),
) -> None:

    if not old_name:
        old_name = module
    dry_run = ctx.obj.get("dry_run", True)

    logger, console = get_logger_console()

    project = Project(path=Path.cwd(), console=console)

    # module to folder
    module = os.path.join(*module.split("."))
    name = os.path.join(*name.split("."))

    logger.info("Calculating Changes")
    # compute changes needed
    changes = rename_changes(project.rope_project, module, old_name, name)

    if not dry_run:
        logger.info("Perfoming  Changes")
    # perfom changes
    project.perform_changes(changes, dry_run)

    typer.Exit()
