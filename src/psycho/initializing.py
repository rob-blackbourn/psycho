import getpass
import importlib.resources
from pathlib import Path
import shutil
import socket
import subprocess
from typing import Optional

from tomlkit import document, table, array, inline_table

from .paths import make_venv_bin
from .projects import write_pyproject


def init_get_name() -> str:
    return Path.cwd().name


def init_get_author() -> str:
    try:
        return subprocess.check_output(
            ['git', 'config', '--get', 'user.name'],
            encoding='utf-8'
        ).strip()
    except:
        return getpass.getuser()


def init_get_email() -> str:
    try:
        return subprocess.check_output(
            ['git', 'config', '--get', 'user.email'],
            encoding='utf-8'
        ).strip()
    except:
        return getpass.getuser() + '@' + socket.getfqdn()


def _create_src(name: str) -> None:
    # Create a source directory
    package_name = name.replace('-', '_')
    package_dir = Path('src') / package_name
    package_dir.mkdir(parents=True, exist_ok=True)
    init_file = package_dir / '__init__.py'
    if not init_file.exists():
        init_file.touch()


def _create_tests() -> None:
    # Create a tests directory
    tests_dir = Path('tests')
    tests_dir.mkdir(parents=True, exist_ok=True)
    init_file = tests_dir / '__init__.py'
    if not init_file.exists():
        init_file.touch()


def _create_gitignore() -> None:
    gitignore = Path('.gitignore')
    if not gitignore.exists():
        # Add a .gitignore file
        text = importlib.resources.read_text(
            'psycho.data',
            'gitignore.txt'
        )
        gitignore.write_text(text, encoding='utf-8')


def _initialize_git() -> None:
    if shutil.which('git') is None:
        return

    # Initialize a git repository
    subprocess.run(['git', 'init'], check=True)
    subprocess.run(['git', 'branch', '-M', 'main'], check=True)


def _create_venv(venv_name: str, upgrade_deps: bool) -> Path:
    # Create a virtual environment
    venv = Path('.') / venv_name
    if not venv.exists():
        minor_version = int(subprocess.getoutput(
            "python -c 'import platform; print(platform.python_version_tuple()[1])'"
        ))
        extra_args = (
            ["--upgrade-deps"]
            if upgrade_deps and minor_version >= 9 else
            []
        )
        subprocess.run(
            ['python', '-m', 'venv', str(venv), *extra_args],
            check=True,
            capture_output=True
        )
    venv_bin = make_venv_bin(venv)
    venv_python = venv_bin / 'python'
    return venv_python


def _create_readme(name: str, description: str) -> Path:
    readme = Path('README.md')
    if not readme.exists():
        text = importlib.resources.read_text(
            'psycho.data',
            'README.md'
        )
        readme.write_text(
            text.format(name=name, description=description),
            encoding='utf-8'
        )
    return readme


def _install_project(venv_python: Path) -> None:
    subprocess.run(
        [str(venv_python), '-m', 'pip', 'install', '-e', '.'],
        check=True
    )


def initialize(
        project_file: Path,
        name: str,
        version: str,
        description: Optional[str],
        author: Optional[str],
        email: Optional[str],
        venv_name: str,
        no_upgrade: bool,
        no_venv: bool,
        no_tests: bool,
) -> None:
    if project_file.exists():
        raise FileExistsError(f"File {project_file} already exists.")

    pyproject = document()

    project = table()
    project.add("name", name)
    project.add("version", version)
    if description:
        project.add("description", description)

    if author or email:
        author_table = inline_table()
        if author:
            author_table.add("name", author)
        if email:
            author_table.add("email", email)
        authors_array = array()
        authors_array.append(author_table)
        project.add("authors", authors_array)

    pyproject.add("project", project)

    build_system = table()
    build_system.add("requires", ["setuptools>=61.0"])
    build_system.add("build-backend", "setuptools.build_meta")
    pyproject.add("build-system", build_system)

    _create_src(name)
    if not no_tests:
        _create_tests()

    if no_venv:
        venv_python: Path | None = None
    else:
        _create_gitignore()
        _initialize_git()
        venv_python = _create_venv(venv_name, not no_upgrade)
        readme = _create_readme(name, description)
        project.add("readme", str(readme))

    write_pyproject(project_file, pyproject)

    if venv_python is not None:
        # install the project in editable mode
        _install_project(venv_python)
