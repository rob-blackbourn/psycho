"""Commands for the Psycho CLI."""

from pathlib import Path

import click
from click import Context

from .building import build_project
from .dependencies import add_packages, remove_packages
from .publishing import publish_project


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
def build() -> None:
    """Build the project."""
    click.echo(f"Building")
    build_project()


@cli.command()
def publish() -> None:
    """Build the project."""
    click.echo("Publishing")
    publish_project()
