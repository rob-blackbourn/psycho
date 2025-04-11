from pathlib import Path
import subprocess
import sys
from typing import Dict, Union, Optional


def _build(
        *args: str
) -> None:
    subprocess.check_call([
        sys.executable, "-m", "build", *args
    ])


def build_project(
        version: Optional[bool],
        verbose: Optional[bool],
        sdist: Optional[bool],
        wheel: Optional[bool],
        skip_dependency_check: Optional[bool],
        no_isolation: Optional[bool],
        config_settings: Dict[str, str],
        outdir: Optional[Path],
        installer: Optional[str]
) -> None:
    """Build the project."""
    args: list[str] = []
    if version:
        args.append("--version")
    if verbose:
        args.append("--verbose")
    if sdist:
        args.append("--sdist")
    if wheel:
        args.append("--wheel")
    if skip_dependency_check:
        args.append("--skip-dependency-check")
    if no_isolation:
        args.append("--no-isolation")
    for name, value in config_settings.items():
        if value is not None:
            args.append(f"--config-setting {name}={value}")
        else:
            args.append(f"--config-setting {name}")
    if outdir is not None:
        args.append(f"--outdir {outdir}")
    if installer is not None:
        args.append(f"--installer {installer}")

    _build(*args)
