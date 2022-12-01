"""Configuration to point to pytest fixtures."""
import shutil
from pathlib import Path

import pytest


@pytest.fixture()
def template_def_path(tmp_path: Path) -> Path:
    """Return path to original template files.

    Returns
    -------
    Path
        path to original template files
    """

    current_path = Path(__file__).parent.parent / "test_data" / "test_package"
    shutil.copytree(current_path, tmp_path / "test_package")
    print(tmp_path / "test_package")
    return tmp_path
