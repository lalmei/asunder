from functools import partial
from typing import Optional

from rope.base.project import Project as RopeProject
from rope.refactor.occurrences import Finder, Occurrence

from asunder.utils.logging import get_logger_console


def find_definition_in_resource(
    repo_project: RopeProject, name: Optional[str], resource: Optional[str]
) -> Occurrence:
    FINDER = partial(Finder, repo_project)
    finder = FINDER(name)
    logger, console = get_logger_console()
    console.print(finder.find_occurrences(resource=resource))
    for occ in finder.find_occurrences(resource=resource):
        console.print(occ)
        if occ.is_defined():
            return occ
