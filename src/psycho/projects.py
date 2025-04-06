from pathlib import Path
from typing import cast
from tomlkit import load, dump, table, TOMLDocument
from tomlkit.items import Table


def read_pyproject(
    project_path: Path,
) -> TOMLDocument:
    """Open a pyproject.toml file and ensure the project and dependencies exist."""
    with open(project_path, "rt", encoding="utf-8") as fp:
        pyproject = load(fp)

    return pyproject


def write_pyproject(
    project_path: Path,
    pyproject: TOMLDocument,
) -> None:
    """Save the pyproject.toml file."""
    with open(project_path, "wt", encoding="utf-8") as fp:
        dump(pyproject, fp)


def ensure_project(pyproject: TOMLDocument) -> Table:
    if "project" not in pyproject:
        pyproject["project"] = table()
    project = pyproject["project"]
    if not isinstance(project, Table):
        raise TypeError(f"Invalid project type {type(project)}")

    return cast(Table, project)
