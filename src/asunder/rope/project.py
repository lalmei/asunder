
from pathlib import Path
import logging

from rich.console import Console

from rope.base.project import Project
from rope.refactor.occurrences import Finder


logger = logging.getLogger("asunder")

class RopeProject():
    
    project: Project
    console: Console
    
    def __init__(self, path: Path = Path.cwd(), console: Console = None) -> None:
        
        self.project = Project(str(path / "src"))
        self.console = console
    
    def perform_changes(self, changes, dry_run):
        
        if dry_run:
            self.console.print(changes.get_description())
            logger.info("Changes to be applied shown above.") 
           
        else:
            self.project.do(changes)
            logger.info("Change set applied ") 
            