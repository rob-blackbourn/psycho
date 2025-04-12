import tempfile
from pathlib import Path
from typing import Dict, Optional

from .building import build_project
from .uploading import upload_project


def publish_project(
        sdist: Optional[bool],
        wheel: Optional[bool],
        skip_dependency_check: Optional[bool],
        no_isolation: Optional[bool],
        config_settings: Dict[str, str],
        installer: Optional[str],
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
    with tempfile.TemporaryDirectory() as outdir:
        build_project(
            False,
            verbose,
            sdist,
            wheel,
            skip_dependency_check,
            no_isolation,
            config_settings,
            outdir,
            installer
        )
        files = [str(f) for f in Path(outdir).glob('*')]
        if len(files) == 0:
            raise FileNotFoundError("No files found to upload.")
        upload_project(
            repository,
            repository_url,
            attestations,
            sign,
            sign_with,
            identity,
            username,
            password,
            non_interactive,
            comment,
            skip_existing,
            cert,
            client_cert,
            verbose,
            disable_progress_bar,
            *files
        )
