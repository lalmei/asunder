
from pathlib import Path
from logging import Logger

from rich.console import Console

from rope.base.project import Project
from rope.refactor.occurrences import Finder



class RopeProject():
    
    project: Project
    console: Console
    
    def __init__(self, path: Path = Path.cwd(), console: Console = None) -> None:
        self.project = Project(str(path))
        self.console = console
    
    
    def perform_changes(self, changes, dry_run):
        
        if dry_run:
            self.console.print(changes.get_description())
            if verbose:
                console.print("Change set is shown above.") 
           
        else:
            self.project.do(changes)
            if verbose:
                console.print("Changes set applied.")
            