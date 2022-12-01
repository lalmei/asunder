import logging
from pathlib import Path
from typing import Optional

from rope.base.change import ChangeSet
from rope.base.project import Project as RopeProject
from rope.refactor.rename import Rename

from asunder.rope_sdk.find import find_definition_in_resource
from asunder.utils.logging import get_logger_console

logger = logging.getLogger("asunder")


def rename_module(
    rope_project: RopeProject, module: Optional[str], to_name: Optional[str]
) -> ChangeSet:
    module_resource = rope_project.get_resource(module)
    return Rename(rope_project, module_resource).get_changes(to_name)


def rename(
    rope_project: RopeProject,
    resource: Path,
    from_name: Optional[str],
    to_name: Optional[str],
) -> ChangeSet:
    module_resource = rope_project.get_resource(str(resource))
    logger, console = get_logger_console()
    # console.print(dir(module_resource))
    if module_resource.is_folder():
        if from_name in [
            Path(x._path).stem for x in module_resource.get_files()
        ]:
            new_resource = resource / Path(from_name + ".py")
            changes = rename_module(rope_project, str(new_resource), to_name)
            return changes

    else:
        definition_occurrence = find_definition_in_resource(
            rope_project, from_name, module_resource
        )
        return Rename(
            rope_project, module_resource, definition_occurrence.offset
        ).get_changes(to_name)
