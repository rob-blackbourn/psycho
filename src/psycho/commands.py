"""Commands for the Psycho CLI."""

from pathlib import Path

import click
from click import Context

from psycho.building import build_project
from psycho.click_types import NAME_EQ_VALUE
from psycho.dependencies import add_packages, remove_packages
from psycho.publishing import publish_project


@click.group()
@click.option(
    "--project-file",
    default="pyproject.toml",
    help="The path to the project file.",
    type=click.Path(exists=True)
)
@click.pass_context
def cli(ctx: Context, project_file: str) -> None:
    """The route command."""
    ctx.ensure_object(dict)
    ctx.obj["PROJECT_FILE"] = project_file


@cli.command(help="Add a package to the project.")
@click.argument("packages", nargs=-1)
@click.option(
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
@click.pass_context
def add(
        ctx: Context,
        packages: tuple[str, ...],
        group: str | None,
        allow_prerelease: bool | None,
        dry_run: bool | None,
        upgrade: bool | None,
        index_url: str | None,
        extra_index_url: str | None,
) -> None:
    """Add a package to the project."""
    click.echo(f"Adding {packages}")
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
    )


@cli.command(help="Remove a package from the project.")
@click.option(
    "--optional",
    'group',
    default=None,
    type=str,
    help="Add the package as an optional dependency (must specify option group name)."
)
@click.argument("packages", nargs=-1)
@click.pass_context
def remove(
        ctx: Context,
        group: str | None,
        packages: tuple[str, ...]
) -> None:
    """Remove a package from the project."""
    click.echo(f"Removing {packages}")
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
    version: bool | None,
    verbose: bool | None,
    sdist: bool | None,
    wheel: bool | None,
    skip_dependency_check: bool | None,
    no_isolation: bool | None,
    config_settings: tuple[tuple[str, str], ...],
    outdir: str | None,
    installer: str | None
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
        Path(outdir) if outdir else None,
        installer
    )


@cli.command(help="Publish the project.")
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
    click.echo("Publishing")
    publish_project(
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


if __name__ == "__main__":
    cli()  # pylint: disable=no-value-for-parameter
