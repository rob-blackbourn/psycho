from pathlib import Path
import subprocess
import sys


def _build(
        *args: str
) -> None:
    subprocess.check_call([
        sys.executable, "-m", "build", *args
    ])


def build_project(
        version: bool | None,
        verbose: bool | None,
        sdist: bool | None,
        wheel: bool | None,
        skip_dependency_check: bool | None,
        no_isolation: bool | None,
        config_settings: dict[str, str],
        outdir: Path | None,
        installer: str | None
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
