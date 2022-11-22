import logging

from rope.base.change import ChangeSet
from rope.base.project import Project as RopeProject
from rope.refactor.rename import Rename

logger = logging.getLogger("asunder")


def rename(rope_project: RopeProject, module: str, to_name: str) -> ChangeSet:
    """Rename"""
    module_resource = rope_project.get_resource(module)
    return Rename(rope_project, module_resource).get_changes(to_name)
