import logging
import os
from pathlib import Path

import typer
from rich.logging import RichHandler
from typer import Context

from asunder.rope import RopeProject
from asunder.rope.rename_module import rename

app = typer.Typer(add_completion=False, no_args_is_help=True)
logger = logging.getLogger("asunder")


@app.command(no_args_is_help=True)
def module(
    ctx: Context,
    path: Path = typer.Option(Path.cwd() / "src", help="path to package source code"),
    module: str = typer.Argument("", help="module to be renamed"),
    name: str = typer.Argument("", help="new module name"),
) -> None:

    dry_run = ctx.obj.get("dry_run", True)

    handler: RichHandler = logger.handlers[0]
    console = handler.console

    ropeProject = RopeProject(path=Path.cwd(), console=console)

    # module to folder
    module = os.path.join(*module.split("."))
    name = os.path.join(*name.split("."))

    changes = rename(ropeProject.project, module, name)
    ropeProject.perform_changes(changes, dry_run)
    typer.Exit(0)
