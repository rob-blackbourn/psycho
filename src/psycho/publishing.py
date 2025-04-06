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


def publish_project() -> None:
    """Build the project."""
    _upload()
