import logging
from datetime import datetime
from pathlib import Path
from typing import Dict, List

import typer
from rich.logging import RichHandler

from asunder.rope import RopeProject
from asunder.rope.rename_module import rename_module

app = typer.Typer(add_completion=False,no_args_is_help=True)
logger = logging.getLogger("asunder")

@app.command(no_args_is_help=True)
def module(module : str = typer.Argument("", help="module to be renamed"), 
           name : str = typer.Argument("",help="new module name")) -> None:
    
    dry_run = ctx.obj["dry-run"]
    handler : RichHandler =  logger.handlers[0]
    console =handler.console 
    ropeProject= RopeProject(console=console)
    changes = rename_module(module, name)
    ropeProject.perform_changes(changes, dry_run)
    typer.Exit(0)