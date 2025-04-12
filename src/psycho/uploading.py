import subprocess
from typing import List, Literal, Optional


def _twine(
        operation: Literal['upload'],
        *args: str,
) -> None:
    subprocess.check_call([
        'python', "-m", "twine", operation, *args
    ])


def upload_project(
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
        *files: str,
) -> None:
    """Build the project."""
    args: List[str] = []
    if repository is not None:
        args += ["--repository", repository]
    if repository_url is not None:
        args += ["--repository-url", repository_url]
    if attestations:
        args += ["--attestations"]
    if sign:
        args += ["--sign"]
    if sign_with is not None:
        args += ["--sign-with", sign_with]
    if identity is not None:
        args += ["--identity", identity]
    if username is not None:
        args += ["--username", username]
    if password is not None:
        args += ["--password", password]
    if non_interactive:
        args += ["--non-interactive"]
    if comment is not None:
        args += ["--comment", comment]
    if skip_existing:
        args += ["--skip-existing"]
    if cert is not None:
        args += ["--cert", cert]
    if client_cert is not None:
        args += ["--client-cert", client_cert]
    if verbose:
        args += ["--verbose"]
    if disable_progress_bar:
        args += ["--disable-progress-bar"]

    _twine('upload', *args, *files)
