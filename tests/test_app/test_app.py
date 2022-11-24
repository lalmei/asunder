import re

from rich.console import Console
from typer.testing import CliRunner

from asunder import app

console = Console()
runner = CliRunner()


def test_version() -> None:
    """Test version call."""
    result = runner.invoke(app, ["--version"], input="")
    console.print(result.stdout)
    assert "asunder version info" in result.stdout.split("\n")[0]
    assert result.exit_code == 0


def test_parse_args() -> None:
    """
    test verbose mode
    """
    verbose_check = re.compile(r"\[[\w*\S*\s*]*\] (INFO     Setting verbose mode ON)")

    result = runner.invoke(app, ["--verbose"], input="")
    console.print(result.stdout)
    assert result.exit_code == 0
    assert verbose_check.search(result.stdout, 0)


def test_unknown_command() -> None:
    """
    test a wrong command
    """

    argv = ["supercalifragilisticexpialidocious"]
    result = runner.invoke(app, argv, input="")
    default_help = "No such command 'supercalifragilisticexpialidocious'"
    console.print(result.stdout)
    assert result.exit_code == 2
    assert default_help in result.stdout
