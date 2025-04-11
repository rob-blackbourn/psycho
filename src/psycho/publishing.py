from glob import glob
import subprocess
import sys
from typing import List, Literal, Optional


def _twine(
        operation: Literal['upload'],
        *args: str,
) -> None:
    subprocess.check_call([
        sys.executable, "-m", "twine", operation, *args
    ])


def publish_project(
        repository: Optional[str],
        repository_url: Optional[str],
        attestations: Optional[bool],
        sign: Optional[bool],
        sign_with: Optional[str],
        identity: Optional[str],
        username: Optional[str],
        password: Optional[str],
        non_interactive: Optional[bool],
        comment: Optional[str],
        skip_existing: Optional[bool],
        cert: Optional[str],
        client_cert: Optional[str],
        verbose: Optional[bool],
        disable_progress_bar: Optional[bool],
) -> None:
    """Build the project."""
    args: List[str] = []
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
