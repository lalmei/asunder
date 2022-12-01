# @app.command()
# def move(ctx: Context,
#     path: Path = typer.Option(Path.cwd() / "src",
#               help="path to package source code"),
#     module: str = typer.Argument(
#         "", help='full module name to be renamed, e.g. "package.module"'):

#     """
#     Move module: --source <module> --target <module> [--do False]
#     """
#     source_resource = PROJECT.get_resource(source)
#     target_resource = PROJECT.get_resource(target)
#     mover = create_move(PROJECT, source_resource)
#     changes = mover.get_changes(target_resource)
#     execute_changes(changes, do)
