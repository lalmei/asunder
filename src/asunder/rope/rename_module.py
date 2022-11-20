from asunder.rope.project import RopeProject

from rope.base.change import ChangeSet
from rope.refactor.rename import Rename

def rename_module(project:RopeProject, module:str, to_name:str, dry_run=True) -> ChangeSet:
    """
    Rename module: --module <name> --to-name <> [--dry_run True]
    """
    module_resource = project.get_resource(module)

    return Rename(project, module_resource).get_changes(to_name)
    