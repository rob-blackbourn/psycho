"""Code for adding packages"""

from pathlib import Path
import subprocess
import sys
from typing import Literal

from packaging.requirements import Requirement
from tomlkit import array
from tomlkit.items import Table, Array

from .projects import read_pyproject, write_pyproject, ensure_project


def _pip(
        command: Literal['install', 'uninstall'],
        requirement: Requirement,
        *args: str
) -> None:
    subprocess.check_call([
        sys.executable, "-m", "pip", command, *args, str(requirement)
    ])


def _read_dependency_requirements(
        project: Table
) -> dict[str, Requirement]:
    if 'dependencies' not in project:
        project['dependencies'] = array()
    dependencies = project["dependencies"]
    if not isinstance(dependencies, Array):
        raise TypeError("dependencies must be an Array")
    requirements = [
        Requirement(str(dep))
        for dep in dependencies
    ]
    return {
        req.name: req
        for req in requirements
    }


def _recreate_dependency_requirements(
        project: Table,
        requirements: dict[str, Requirement]
) -> None:
    dependencies = array()
    for req in requirements.values():
        dependencies.add_line(str(req))
    project['dependencies'] = dependencies


def add_packages(
        project_path: Path,
        packages: tuple[str, ...]
) -> None:
    pyproject = read_pyproject(project_path)
    project = ensure_project(pyproject)
    current_requirements = _read_dependency_requirements(project)
    requirements = [Requirement(pkg) for pkg in packages]

    for req in requirements:
        if req.name in current_requirements:
            _pip('uninstall', req, '-y')

        _pip('install', req)

        current_requirements[req.name] = req

    _recreate_dependency_requirements(project, current_requirements)

    write_pyproject(project_path, pyproject)


def remove_packages(
        project_path: Path,
        packages: tuple[str, ...]
) -> None:
    pyproject = read_pyproject(project_path)
    project = ensure_project(pyproject)
    current_requirements = _read_dependency_requirements(project)
    requirements = [Requirement(pkg) for pkg in packages]

    for req in requirements:
        if req.name not in current_requirements:
            raise KeyError(f"Dependency {req} does not exist")

        _pip('uninstall', req, '-y')
        del current_requirements[req.name]

    _recreate_dependency_requirements(project, current_requirements)

    write_pyproject(project_path, pyproject)
