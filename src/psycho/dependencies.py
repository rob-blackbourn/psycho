"""Code for adding packages"""

from pathlib import Path
import subprocess
import sys
from typing import cast, Literal

from packaging.requirements import Requirement
from tomlkit import table, array
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


def _read_required_dependency_requirements(
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


def _recreate_required_dependency_requirements(
        project: Table,
        requirements: dict[str, Requirement]
) -> None:
    dependencies = array()
    for req in requirements.values():
        dependencies.add_line(str(req))
    project['dependencies'] = dependencies


def _read_optional_dependency_requirements(
        project: Table,
        group: str
) -> dict[str, Requirement]:
    if 'optional-dependencies' not in project:
        project['optional-dependencies'] = table()
    optional_dependencies = project["optional-dependencies"]
    if not isinstance(optional_dependencies, Table):
        raise TypeError("dependencies must be a Table")
    if group not in optional_dependencies:
        optional_dependencies[group] = array()
    dependencies = optional_dependencies[group]
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


def _recreate_optional_dependency_requirements(
        project: Table,
        group: str,
        requirements: dict[str, Requirement]
) -> None:
    dependencies = array()
    for req in requirements.values():
        dependencies.add_line(str(req))
    optional_dependencies = cast(Table, project['optional-dependencies'])
    optional_dependencies[group] = dependencies


def _install_requirements(
        requirements: list[Requirement],
        current_requirements: dict[str, Requirement]
) -> None:
    for req in requirements:
        if req.name in current_requirements:
            _pip('uninstall', req, '-y')

        _pip('install', req)

        current_requirements[req.name] = req


def _add_required_packages(
        project_path: Path,
        packages: tuple[str, ...]
) -> None:
    pyproject = read_pyproject(project_path)
    project = ensure_project(pyproject)
    current_requirements = _read_required_dependency_requirements(project)
    requirements = [Requirement(pkg) for pkg in packages]

    _install_requirements(requirements, current_requirements)

    _recreate_required_dependency_requirements(project, current_requirements)

    write_pyproject(project_path, pyproject)


def _add_optional_packages(
        project_path: Path,
        group: str,
        packages: tuple[str, ...]
) -> None:
    pyproject = read_pyproject(project_path)
    project = ensure_project(pyproject)
    current_requirements = _read_optional_dependency_requirements(
        project,
        group
    )
    requirements = [Requirement(pkg) for pkg in packages]

    _install_requirements(requirements, current_requirements)

    _recreate_optional_dependency_requirements(
        project,
        group,
        current_requirements
    )

    write_pyproject(project_path, pyproject)


def add_packages(
        project_path: Path,
        optional: str | None,
        packages: tuple[str, ...]
) -> None:
    if optional is None:
        _add_required_packages(project_path, packages)
    else:
        _add_optional_packages(project_path, optional, packages)


def _uninstall_requirements(
        requirements: list[Requirement],
        current_requirements: dict[str, Requirement]
) -> None:
    for req in requirements:
        if req.name not in current_requirements:
            raise KeyError(f"Dependency {req} does not exist")

        _pip('uninstall', req, '-y')
        del current_requirements[req.name]


def _remove_required_packages(
        project_path: Path,
        packages: tuple[str, ...]
) -> None:
    pyproject = read_pyproject(project_path)
    project = ensure_project(pyproject)
    current_requirements = _read_required_dependency_requirements(project)
    requirements = [Requirement(pkg) for pkg in packages]

    _uninstall_requirements(requirements, current_requirements)

    _recreate_required_dependency_requirements(project, current_requirements)

    write_pyproject(project_path, pyproject)


def _remove_optional_packages(
        project_path: Path,
        group: str,
        packages: tuple[str, ...]
) -> None:
    pyproject = read_pyproject(project_path)
    project = ensure_project(pyproject)
    current_requirements = _read_optional_dependency_requirements(
        project,
        group
    )
    requirements = [Requirement(pkg) for pkg in packages]

    _uninstall_requirements(requirements, current_requirements)

    _recreate_optional_dependency_requirements(
        project,
        group,
        current_requirements
    )

    write_pyproject(project_path, pyproject)


def remove_packages(
        project_path: Path,
        group: str | None,
        packages: tuple[str, ...]
) -> None:
    if group is None:
        _remove_required_packages(project_path, packages)
    else:
        _remove_optional_packages(project_path, group, packages)
