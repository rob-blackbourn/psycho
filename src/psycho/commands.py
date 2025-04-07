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


@cli.command()
@click.argument("packages", nargs=-1)
@click.pass_context
def add(ctx: Context, packages: tuple[str, ...]) -> None:
    """Add a package to the project."""
    click.echo(f"Adding {packages}")
    project_file: Path = ctx.obj["PROJECT_FILE"]
    add_packages(project_file, packages)


@cli.command()
@click.argument("packages", nargs=-1)
@click.pass_context
def remove(ctx: Context, packages: tuple[str, ...]):
    """Remove a package from the project."""
    click.echo(f"Removing {packages}")
    project_file: Path = ctx.obj["PROJECT_FILE"]
    remove_packages(project_file, packages)


@cli.command()
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


@cli.command()
@click.option(
    "-r",
    "repository",
    default=None,
    type=str
)
def publish(repository: str | None) -> None:
    """Build the project."""
    click.echo("Publishing")
    publish_project(repository)


if __name__ == "__main__":
    cli()  # pylint: disable=no-value-for-parameter
