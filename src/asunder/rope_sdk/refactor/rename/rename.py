import logging

from rope.base.change import ChangeSet
from rope.base.project import Project as RopeProject
from rope.refactor.rename import Rename

from asunder.rope_sdk.find import find_definition_in_resource

logger = logging.getLogger("asunder")


def rename_module(rope_project: RopeProject, module: str, to_name: str) -> ChangeSet:
    module_resource = rope_project.get_resource(module)
    return Rename(rope_project, module_resource).get_changes(to_name)


def rename(
    rope_project: RopeProject, module: str, from_name: str, to_name: str
) -> ChangeSet:
    module_resource = rope_project.get_resource(module)
    definition_occurrence = find_definition_in_resource(
        rope_project, from_name, module_resource
    )
    return Rename(
        rope_project, module_resource, definition_occurrence.offset
    ).get_changes(to_name)
