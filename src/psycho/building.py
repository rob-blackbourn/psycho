from pathlib import Path
import subprocess
import sys
from typing import Literal


def _build(
        *args: str
) -> None:
    subprocess.check_call([
        sys.executable, "-m", "build", *args
    ])


def build_project() -> None:
    """Build the project."""
    _build()
