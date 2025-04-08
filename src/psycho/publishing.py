from glob import glob
import subprocess
import sys
from typing import Literal


def _twine(
        operation: Literal['upload'],
        *args: str,
) -> None:
    subprocess.check_call([
        sys.executable, "-m", "twine", operation, *args
    ])


def publish_project(
        repository: str | None,
        repository_url: str | None,
        attestations: bool | None,
        sign: bool | None,
        sign_with: str | None,
        identity: str | None,
        username: str | None,
        password: str | None,
        non_interactive: bool | None,
        comment: str | None,
        skip_existing: bool | None,
        cert: str | None,
        client_cert: str | None,
        verbose: bool | None,
        disable_progress_bar: bool | None,
) -> None:
    """Build the project."""
    args: list[str] = []
    if repository is not None:
        args.append(f"--repository {repository}")
    if repository_url is not None:
        args.append(f"--repository-url {repository_url}")
    if attestations:
        args.append("--attestations")
    if sign:
        args.append("--sign")
    if sign_with is not None:
        args.append(f"--sign-with {sign_with}")
    if identity is not None:
        args.append(f"--identity {identity}")
    if username is not None:
        args.append(f"--username {username}")
    if password is not None:
        args.append(f"--password {password}")
    if non_interactive:
        args.append("--non-interactive")
    if comment is not None:
        args.append(f"--comment {comment}")
    if skip_existing:
        args.append("--skip-existing")
    if cert is not None:
        args.append(f"--cert {cert}")
    if client_cert is not None:
        args.append(f"--client-cert {client_cert}")
    if verbose:
        args.append("--verbose")
    if disable_progress_bar:
        args.append("--disable-progress-bar")

    _twine('upload', *args, *glob("dist/*"))
