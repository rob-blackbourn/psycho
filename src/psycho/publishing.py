from pathlib import Path
import subprocess
import sys
from typing import Literal


def _upload(
        *args: str
) -> None:
    subprocess.check_call([
        sys.executable, "-m", "twine", *args
    ])


def publish_project(repository: str | None) -> None:
    """Build the project."""
    args: list[str] = []
    if repository is not None:
        args.append(f"-r {repository}")
    _upload(*args)
