import subprocess
from typing import Dict, Optional


def _build(
        *args: str
) -> None:
    subprocess.check_call([
        'python', "-m", "build", *args
    ])


def build_project(
        version: Optional[bool],
        verbose: Optional[bool],
        sdist: Optional[bool],
        wheel: Optional[bool],
        skip_dependency_check: Optional[bool],
        no_isolation: Optional[bool],
        config_settings: Dict[str, str],
        outdir: Optional[str],
        installer: Optional[str]
) -> None:
    """Build the project."""
    args: list[str] = []
    if version:
        args += ["--version"]
    if verbose:
        args += ["--verbose"]
    if sdist:
        args += ["--sdist"]
    if wheel:
        args += ["--wheel"]
    if skip_dependency_check:
        args += ["--skip-dependency-check"]
    if no_isolation:
        args += ["--no-isolation"]
    for name, value in config_settings.items():
        if value is not None:
            args += ["--config-setting", f"{name}={value}"]
        else:
            args += ["--config-setting", name]
    if outdir is not None:
        args += ["--outdir", outdir]
    if installer is not None:
        args += ["--installer", installer]

    _build(*args)
