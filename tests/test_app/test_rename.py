from pathlib import Path

from rich.console import Console
from typer.testing import CliRunner

from asunder import app

console = Console()
runner = CliRunner()


def test_refactor(template_def_path: Path) -> None:
    """Test version call."""

    test_package_path = str(template_def_path)
    console.print(test_package_path)
    result = runner.invoke(
        app,
        [
            "--dry-run",
            "refactor",
            "rename",
            "--path",
            test_package_path,
            "--module",
            "test_package/module1",
            "--old-name",
            "submodule1",
            "--new-name",
            "subMOM",
        ],
        input="",
    )
    console.print(result.stdout)
    assert result.exit_code == 0
