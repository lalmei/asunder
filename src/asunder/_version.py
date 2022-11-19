"""Version."""
import platform
import sys
from pathlib import Path
from typing import List

__version__ = "0.1.0"


def version_info() -> str:
    """
    Version information

    Outputs version and other local information for debugging.

    Returns:
        str: Returns the version
    """
    optional_deps: List[str] = []

    info = {
        "asunder version": __version__,  # package version information
        "install path": Path(__file__).resolve().parent,  # path where package is installed
        "python version": sys.version,  # python version
        "platform": platform.platform(),  # OS info
        "optional deps. installed": optional_deps,
    }
    return "\n".join("{0:>30} {1}".format(k + ":", str(v).replace("\n", " ")) for k, v in info.items())
