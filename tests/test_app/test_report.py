from pathlib import Path

from rich.console import Console
from typer.testing import CliRunner

from asunder import app

console = Console()
runner = CliRunner()


def test_report(template_def_path: Path) -> None:
    """Test version call."""

    test_package_path = str(template_def_path)
    console.print(test_package_path)
    result = runner.invoke(
        app,
        [
            "--dry-run",
            "report",
            test_package_path,
        ],
        input="",
    )
    console.print(result.stdout)
    assert result.exit_code == 0
