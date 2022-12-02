import logging
from pathlib import Path

from rich.console import Console
from rope.base.change import ChangeSet
from rope.base.project import Project as RopeProject

logger = logging.getLogger("asunder")


class Project:
    def __init__(
        self, path: Path = Path.cwd(), console: Console = Console()
    ) -> None:

        self.rope_project = RopeProject(str(path))
        self.console = console

    def perform_changes(self, changes: ChangeSet, dry_run: bool) -> None:

        if dry_run:
            self.console.print(changes.get_description())
            logger.info("Changes to be applied shown above.")

        else:
            self.rope_project.do(changes)
            logger.info("Change set applied ")
