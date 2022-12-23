from pathlib import Path

from rich.console import Console
from typer.testing import CliRunner

from asunder import app

console = Console()
runner = CliRunner()


def test_refactor(template_def_path: Path) -> None:
    """Test version call."""

    old_path = Path("test_package", "module1", "submodule1.py")
    Path("test_package", "module1", "subMOM.py")
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
    old_full_path: Path = test_package_path / old_path
    new_full_path: Path = test_package_path / old_path
    assert not old_full_path.exists()
    assert new_full_path.exists()
