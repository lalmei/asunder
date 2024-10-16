import logging
from pathlib import Path
from typing import Optional

import typer
from typer import Context
from pydriller import Repository

from asunder.utils.logging import get_logger_console
from asunder.utils.checks import is_url
from asunder.repository.extract import extract_repo_data

app = typer.Typer(add_completion=True, no_args_is_help=True)

logger = logging.getLogger("asunder")


@app.command(no_args_is_help=True)
def extract(
    ctx: Context,
    path: Path = typer.Option(Path.cwd(), help="path or url to package source code"),
    repo_token: Optional[str] = typer.Option(
        None,
        "--git-token",
        envvar="GITHUB_TOKEN",
        help="Git personal access token for repository analysis",
    ),
) -> None:
    logger, console = get_logger_console()

    dry_run = ctx.obj.get("dry_run", True)

    logger.info("Analyzing Repository")
    if is_url:
        logger.error("Online Analysis not implemented")
        typer.Exit(code=1)
        # analyze github or gitlab pull/merge requests, issues
        if not repo_token:
            raise ValueError(
                "token required for repository analysis of pull requests and issues, you can define the env variable GITHUB_TOKEN"
            )
    if not path.exists():
        logger.error(f"Error: Path not found: {path}")
        raise typer.Exit(code=1)
    # project = Project(path=path, console=console)

    repo = Repository(path)
    extract_repo_data(repo)
    if not dry_run:
        logger.info("Perfoming  Changes")
    # perfom changes

    typer.Exit()
