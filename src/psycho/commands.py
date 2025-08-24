"""Commands for the Psycho CLI."""

import os
from pathlib import Path
from typing import Optional, Sequence, Tuple

import click
from click import Context
from click_aliases import ClickAliasedGroup

from psycho.building import build_project
from psycho.click_types import NAME_EQ_VALUE
from psycho.dependencies import add_packages, remove_packages
from psycho.environment import environment, location
from psycho.initializing import (
    initialize,
    init_get_name,
    init_get_author,
    init_get_email
)
from psycho.paths import make_venv_bin
from psycho.publishing import publish_project
from psycho.uploading import upload_project


@click.group(cls=ClickAliasedGroup)
@click.option(
    "--project-file",
    default="pyproject.toml",
    help="The path to the project file.",
    type=click.Path()
)
@click.pass_context
def cli(ctx: Context, project_file: str) -> None:
    """Utilities for manageging pyproject.toml with pip, build and twine."""

    ctx.ensure_object(dict)
    ctx.obj["PROJECT_FILE"] = Path(project_file)

    if 'VIRTUAL_ENV' in os.environ:
        # Ensure the virtual environment wins.
        venv_bin = make_venv_bin(Path(os.environ['VIRTUAL_ENV']))
        os.environ['PATH'] = str(venv_bin) + os.pathsep + os.environ['PATH']


@cli.command(help="Install a package.", aliases=['add'])
@click.argument("packages", nargs=-1)
@click.option(
    "-o",
    "--optional",
    'group',
    default=None,
    type=str,
    help="Add the package as an optional dependency (must specify option group name).",
)
@click.option(
    '--pre',
    'allow_prerelease',
    is_flag=True,
    default=None,
    help="Include pre-release and development versions. By default, pip only finds stable versions.",
)
@click.option(
    '--dry-run',
    is_flag=True,
    default=None,
    help="Don’t actually install anything, just print what would be.",
)
@click.option(
    '-U',
    '--upgrade',
    is_flag=True,
    default=None,
    help="Upgrade all specified packages to the newest available version. The handling of dependencies depends on the upgrade-strategy used.",
)
@click.option(
    "-i",
    "--index-url",
    default=None,
    type=str,
    help="Base URL of the Python Package Index (default https://pypi.org/simple). This should point to a repository compliant with PEP 503 (the simple repository API) or a local directory laid out in the same format.",
)
@click.option(
    "--extra-index-url",
    default=None,
    type=str,
    help="Extra URLs of package indexes to use in addition to --index-url. Should follow the same rules as --index-url.",
)
@click.option(
    '-e',
    '--editable',
    is_flag=True,
    default=None,
    help='Install a project in editable mode (i.e. setuptools "develop mode") from a local project path or a VCS url.',
)
@click.pass_context
def install(
        ctx: Context,
        packages: Sequence[str],
        group: Optional[str],
        allow_prerelease: Optional[bool],
        dry_run: Optional[bool],
        upgrade: Optional[bool],
        index_url: Optional[str],
        extra_index_url: Optional[str],
        editable: Optional[bool],
) -> None:
    """Add a package to the project."""
    click.echo(f"Adding {','.join(packages)}")
    project_file: Path = ctx.obj["PROJECT_FILE"]
    add_packages(
        project_file,
        packages,
        group,
        allow_prerelease,
        dry_run,
        upgrade,
        index_url,
        extra_index_url,
        editable,
    )


@cli.command(help="Uninstall a package.", aliases=['remove'])
@click.option(
    "--optional",
    'group',
    default=None,
    type=str,
    help="Add the package as an optional dependency (must specify option group name)."
)
@click.argument("packages", nargs=-1)
@click.pass_context
def uninstall(
        ctx: Context,
        group: Optional[str],
        packages: Sequence[str]
) -> None:
    """Remove a package from the project."""
    click.echo(f"Removing {','.join(packages)}")
    project_file: Path = ctx.obj["PROJECT_FILE"]
    remove_packages(
        project_file,
        group,
        packages
    )


@cli.command(help="Build the project.")
@click.option(
    '-V', '--version',
    is_flag=True,
    default=None,
    help="show program’s version number and exit"
)
@click.option(
    '-v', '--verbose',
    is_flag=True,
    default=None,
    help="increase verbosity (default: 0)"
)
@click.option(
    '-s', '--sdist',
    is_flag=True,
    default=None,
    help="build a source distribution (disables the default behavior)"
)
@click.option(
    '-w',
    '--wheel',
    is_flag=True,
    default=None
)
@click.option(
    '-x',
    '--skip-dependency-check',
    is_flag=True,
    default=None
)
@click.option(
    '-n',
    '--no-isolation',
    is_flag=True,
    default=None
)
@click.option(
    '-C', '--config-setting', 'config_settings',
    multiple=True,
    type=NAME_EQ_VALUE,
    help="settings to pass to the backend. Multiple settings can be provided. Settings beginning with a hyphen will erroneously be interpreted as options to build if separated by a space character; use --config-setting=--my-setting -C--my-other-setting (default: None)"
)
@click.option(
    "--installer",
    default=None,
    type=str,
    help="Python package installer to use (defaults to pip)"
)
@click.option(
    "-o", "--outdir",
    default=None,
    type=click.Path(exists=True),
    help="The path to the project file.",
)
def build(
    version: Optional[bool],
    verbose: Optional[bool],
    sdist: Optional[bool],
    wheel: Optional[bool],
    skip_dependency_check: Optional[bool],
    no_isolation: Optional[bool],
    config_settings: Sequence[Tuple[str, str]],
    outdir: Optional[str],
    installer: Optional[str]
) -> None:
    """Build the project."""
    click.echo("Building")
    config_vars = {
        name: value
        for name, value in config_settings
    }
    build_project(
        version,
        verbose,
        sdist,
        wheel,
        skip_dependency_check,
        no_isolation,
        config_vars,
        outdir,
        installer
    )


@cli.command(help="Upload the project.")
@click.argument("files", nargs=-1)
@click.option(
    "-r",
    "--repository",
    default=None,
    type=str,
    help="The repository (package index) to upload the package to. Should be a section in the config file [default: pypi]. (Can also be set via TWINE_REPOSITORY environment variable.)"
)
@click.option(
    "--repository-url",
    default=None,
    type=str,
    help="The repository (package index) URL to upload the package to. This overrides --repository. (Can also be set via TWINE_REPOSITORY_URL environment variable.)"
)
@click.option(
    '--attestations',
    is_flag=True,
    default=None,
    help="Upload each file's associated attestations."
)
@click.option(
    '-s',
    '--sign',
    is_flag=True,
    default=None,
    help="Sign files to upload using GPG."
)
@click.option(
    "--sign-with",
    default=None,
    type=str,
    help="GPG program used to sign uploads [default: gpg]."
)
@click.option(
    "-i",
    "--identity",
    default=None,
    type=str,
    help="GPG identity used to sign files."
)
@click.option(
    "-u",
    "--username",
    default=None,
    type=str,
    help="The username to authenticate to the repository (package index) as. Has no effect on PyPI or TestPyPI. (Can also be set via TWINE_USERNAME environment variable.)"
)
@click.option(
    "-p",
    "--password",
    default=None,
    type=str,
    help="The password to authenticate to the repository (package index) with. (Can also be set via TWINE_PASSWORD environment variable.)"
)
@click.option(
    '--non-interactive',
    is_flag=True,
    default=None,
    help="Do not interactively prompt for username/password if the required credentials are missing. (Can also be set via TWINE_NON_INTERACTIVE environment variable.)"
)
@click.option(
    "-c",
    "--comment",
    default=None,
    type=str,
    help="The comment to include with the distribution file."
)
@click.option(
    '--skip-existing',
    is_flag=True,
    default=None,
    help="Do not interactively prompt for username/password if the required credentials are missing. (Can also be set via TWINE_NON_INTERACTIVE environment variable.)"
)
@click.option(
    "--cert",
    type=click.Path(exists=True),
    help="Path to alternate CA bundle (can also be set via TWINE_CERT environment variable).",
)
@click.option(
    "--client-cert",
    type=click.Path(exists=True),
    help="Path to SSL client certificate, a single file containing the private key and the certificate in PEM format.",
)
@click.option(
    '--verbose',
    is_flag=True,
    default=None,
    help="Show verbose output."
)
@click.option(
    '--disable-progress-bar',
    is_flag=True,
    default=None,
    help="Disable the progress bar."
)
def upload(
        files: Sequence[str],
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


@cli.command(help="Publish the project.")
@click.option(
    '-s', '--sdist',
    is_flag=True,
    default=None,
    help="build a source distribution (disables the default behavior)"
)
@click.option(
    '-w',
    '--wheel',
    is_flag=True,
    default=None
)
@click.option(
    '-x',
    '--skip-dependency-check',
    is_flag=True,
    default=None
)
@click.option(
    '-n',
    '--no-isolation',
    is_flag=True,
    default=None
)
@click.option(
    '-C', '--config-setting', 'config_settings',
    multiple=True,
    type=NAME_EQ_VALUE,
    help="settings to pass to the backend. Multiple settings can be provided. Settings beginning with a hyphen will erroneously be interpreted as options to build if separated by a space character; use --config-setting=--my-setting -C--my-other-setting (default: None)"
)
@click.option(
    "--installer",
    default=None,
    type=str,
    help="Python package installer to use (defaults to pip)"
)
@click.option(
    "-r",
    "--repository",
    default=None,
    type=str,
    help="The repository (package index) to upload the package to. Should be a section in the config file [default: pypi]. (Can also be set via TWINE_REPOSITORY environment variable.)"
)
@click.option(
    "--repository-url",
    default=None,
    type=str,
    help="The repository (package index) URL to upload the package to. This overrides --repository. (Can also be set via TWINE_REPOSITORY_URL environment variable.)"
)
@click.option(
    '--attestations',
    is_flag=True,
    default=None,
    help="Upload each file's associated attestations."
)
@click.option(
    '-s',
    '--sign',
    is_flag=True,
    default=None,
    help="Sign files to upload using GPG."
)
@click.option(
    "--sign-with",
    default=None,
    type=str,
    help="GPG program used to sign uploads [default: gpg]."
)
@click.option(
    "-i",
    "--identity",
    default=None,
    type=str,
    help="GPG identity used to sign files."
)
@click.option(
    "-u",
    "--username",
    default=None,
    type=str,
    help="The username to authenticate to the repository (package index) as. Has no effect on PyPI or TestPyPI. (Can also be set via TWINE_USERNAME environment variable.)"
)
@click.option(
    "-p",
    "--password",
    default=None,
    type=str,
    help="The password to authenticate to the repository (package index) with. (Can also be set via TWINE_PASSWORD environment variable.)"
)
@click.option(
    '--non-interactive',
    is_flag=True,
    default=None,
    help="Do not interactively prompt for username/password if the required credentials are missing. (Can also be set via TWINE_NON_INTERACTIVE environment variable.)"
)
@click.option(
    "-c",
    "--comment",
    default=None,
    type=str,
    help="The comment to include with the distribution file."
)
@click.option(
    '--skip-existing',
    is_flag=True,
    default=None,
    help="Do not interactively prompt for username/password if the required credentials are missing. (Can also be set via TWINE_NON_INTERACTIVE environment variable.)"
)
@click.option(
    "--cert",
    type=click.Path(exists=True),
    help="Path to alternate CA bundle (can also be set via TWINE_CERT environment variable).",
)
@click.option(
    "--client-cert",
    type=click.Path(exists=True),
    help="Path to SSL client certificate, a single file containing the private key and the certificate in PEM format.",
)
@click.option(
    '--verbose',
    is_flag=True,
    default=None,
    help="Show verbose output."
)
@click.option(
    '--disable-progress-bar',
    is_flag=True,
    default=None,
    help="Disable the progress bar."
)
def publish(
        sdist: Optional[bool],
        wheel: Optional[bool],
        skip_dependency_check: Optional[bool],
        no_isolation: Optional[bool],
        config_settings: Sequence[Tuple[str, str]],
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
    """Build the project."""
    click.echo("Publishing")
    config_vars = {
        name: value
        for name, value in config_settings
    }
    publish_project(
        sdist,
        wheel,
        skip_dependency_check,
        no_isolation,
        config_vars,
        installer,
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
    )


@cli.command(help="Initialise a package.")
@click.option(
    "--name",
    type=str,
    required=True,
    default=init_get_name,
    help="Name"
)
@click.option(
    "--version",
    type=str,
    default="0.1.0",
    required=True,
    help="Version"
)
@click.option(
    "--description",
    type=str,
    default="Let's go psycho!",
    help="Description"
)
@click.option(
    "--author",
    type=str,
    default=init_get_author,
    help="Author"
)
@click.option(
    "--email",
    type=str,
    default=init_get_email,
    help="Email"
)
@click.option(
    "--venv-name",
    type=str,
    default=".venv",
    help="Name of the folder for the virtual environment"
)
@click.option(
    "--no-upgrade",
    is_flag=True,
    default=False,
    help="Do not upgrade the venv dependencies."
)
@click.option(
    "--no-venv",
    is_flag=True,
    default=False,
    help="Do not create a virtual environment."
)
@click.option(
    "--no-tests",
    is_flag=True,
    default=False,
    help="Do not create a tests folder."
)
@click.option(
    '-y',
    "--yes",
    is_flag=True,
    default=False,
    help="Accept all defaults."
)
@click.pass_context
def init(
        ctx: Context,
        name: str,
        version: str,
        description: str,
        author: str,
        email: str,
        venv_name: str,
        no_upgrade: bool,
        no_venv: bool,
        no_tests: bool,
        yes: bool,
) -> None:
    """Remove a package from the project."""

    if not yes:
        name = click.prompt("Name", default=name, type=str)
        version = click.prompt("Version", default=version, type=str)
        description = click.prompt(
            "Description", default=description, type=str)
        author = click.prompt("Author", default=author, type=str)
        email = click.prompt("Email", default=email, type=str)

    click.echo(f"Initializing {name}")
    project_file: Path = ctx.obj["PROJECT_FILE"]
    initialize(
        project_file,
        name,
        version,
        description,
        author,
        email,
        venv_name,
        no_upgrade,
        no_venv,
        no_tests
    )


@cli.command(help="Show the environment variables.")
def env() -> None:
    """Remove a package from the project."""
    dct = environment()
    for name, value in dct.items():
        click.echo(f"{name}='{value}'")


@cli.command(help="Show the path to an executable.")
@click.argument("exe", required=True)
def which(exe: str) -> None:
    """Remove a package from the project."""
    path = location(exe)
    if path is None:
        click.echo(f"{exe} not found")
    else:
        click.echo(f"{exe}: {path}")


if __name__ == "__main__":
    cli()  # pylint: disable=no-value-for-parameter
