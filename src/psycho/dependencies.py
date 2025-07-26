"""Code for adding packages"""

from pathlib import Path
import subprocess
import re
from typing import cast, Dict, List, Literal, Optional, Sequence, Union

from packaging.requirements import Requirement
from tomlkit import table, array
from tomlkit.items import Table, Array

from .projects import read_pyproject, write_pyproject, ensure_project


def _pip(
        command: Literal['install', 'uninstall'],
        dependency: Union[Requirement, Path],
        *args: str
) -> None:
    subprocess.check_call([
        'python', "-m", "pip", command, *args, str(dependency)
    ])


def _pip_install_editable(name: str, args: List[str]) -> None:
    subprocess.check_call([
        'python', "-m", "pip", 'install', '--editable', name, *args
    ])


def _parse_dependency(value: str) -> Union[Requirement, Path]:
    """Convert a string to a Requirement or Path."""
    if value.startswith(".") or value.startswith('/'):
        return Path(value)
    elif value.startswith('file://'):
        return Path(value[7:])
    try:
        return Requirement(value)
    except ValueError:
        return Path(value)


def _read_required_dependencies(
        project: Table
) -> Dict[str, Union[Requirement, Path]]:
    if 'dependencies' not in project:
        project['dependencies'] = array()
    unparsed_dependencies = project["dependencies"]
    if not isinstance(unparsed_dependencies, Array):
        raise TypeError("dependencies must be an Array")
    parsed_dependencies = [
        _parse_dependency(str(item))
        for item in unparsed_dependencies
    ]
    return {
        dependency.name: dependency
        for dependency in parsed_dependencies
    }


def _recreate_required_dependencies(
        project: Table,
        dependencies: Dict[str, Union[Requirement, Path]]
) -> None:
    dependency_array = array()
    for dependency in dependencies.values():
        dependency_array.append(str(dependency))
    project['dependencies'] = dependency_array.multiline(True)


def _read_optional_dependencies(
        project: Table,
        group: str
) -> Dict[str, Union[Requirement, Path]]:
    if 'optional-dependencies' not in project:
        project['optional-dependencies'] = table()
    optional_dependencies = project["optional-dependencies"]
    if not isinstance(optional_dependencies, Table):
        raise TypeError("dependencies must be a Table")
    if group not in optional_dependencies:
        optional_dependencies[group] = array()
    unparsed_dependencies = optional_dependencies[group]
    if not isinstance(unparsed_dependencies, Array):
        raise TypeError("dependencies must be an Array")
    parsed_dependencies = [
        _parse_dependency(str(item))
        for item in unparsed_dependencies
    ]
    return {
        dependency.name: dependency
        for dependency in parsed_dependencies
    }


def _recreate_optional_dependencies(
        project: Table,
        group: str,
        dependencies: Dict[str, Union[Requirement, Path]]
) -> None:
    dependency_array = array()
    for dependency in dependencies.values():
        dependency_array.append(str(dependency))
    optional_dependencies = cast(Table, project['optional-dependencies'])
    if len(dependency_array) > 0:
        optional_dependencies[group] = dependency_array.multiline(True)
    else:
        del optional_dependencies[group]
        if len(optional_dependencies) == 0:
            del project['optional-dependencies']


def add_packages(
        project_path: Path,
        packages: Sequence[str],
        group: Optional[str],
        allow_prerelease: Optional[bool],
        dry_run: Optional[bool],
        upgrade: Optional[bool],
        index_url: Optional[str],
        extra_index_url: Optional[str],
        editable: Optional[bool],
) -> None:
    args: List[str] = []
    if allow_prerelease:
        args += ['--pre']
    if dry_run:
        args += ['--dry-run']
    if upgrade:
        args += ['--upgrade']
    if index_url:
        args += ['--index-url', index_url]
    if extra_index_url:
        args += ['--extra-index-url', extra_index_url]
    if editable:
        args += ['--editable']

    # Special case for no packages - install the project as editable.
    if len(packages) == 0:
        _pip_install_editable(".", args)
        return

    if editable:
        if len(packages) > 1:
            raise ValueError(
                "Cannot install multiple packages in editable mode"
            )
        pkg = packages[0].strip()
        if re.match(r"\.\s*(\[[^\]]*\])?$", pkg):
            _pip_install_editable(pkg, args)
            return

    pyproject = read_pyproject(project_path)
    project = ensure_project(pyproject)
    current_dependencies = _read_required_dependencies(
        project
    ) if not group else _read_optional_dependencies(
        project,
        group
    )

    requested_dependencies = [_parse_dependency(pkg) for pkg in packages]

    for dependency in requested_dependencies:
        if dependency.name in current_dependencies:
            _pip('uninstall', dependency, '-y')

        _pip('install', dependency, *args)

        current_dependencies[dependency.name] = dependency

    if group is None:
        _recreate_required_dependencies(
            project,
            current_dependencies
        )
    else:
        _recreate_optional_dependencies(
            project,
            group,
            current_dependencies
        )

    write_pyproject(project_path, pyproject)


def remove_packages(
        project_path: Path,
        group: Optional[str],
        packages: Sequence[str]
) -> None:
    pyproject = read_pyproject(project_path)
    project = ensure_project(pyproject)
    current_dependencies = _read_required_dependencies(
        project
    ) if not group else _read_optional_dependencies(
        project,
        group
    )

    unwanted_dependencies = [_parse_dependency(pkg) for pkg in packages]

    for dependency in unwanted_dependencies:
        if dependency.name not in current_dependencies:
            raise KeyError(f"Dependency {dependency} does not exist")

        _pip('uninstall', dependency, '-y')
        del current_dependencies[dependency.name]

    if group is None:
        _recreate_required_dependencies(project, current_dependencies)
    else:
        _recreate_optional_dependencies(
            project,
            group,
            current_dependencies
        )

    write_pyproject(project_path, pyproject)
