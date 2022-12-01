from rope.base.project import Project as RopeProject
from rope.refactor.occurrences import Finder


def find_definition_in_resource(
    repo_project: RopeProject, name: str, resource: str
):
    FINDER = partial(Finder, repo_project)
    finder = FINDER(name)
    return next(
        occ
        for occ in finder.find_occurrences(resource=resource)
        if occ.is_defined() or occ.is_written()
    )
