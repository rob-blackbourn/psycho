import getpass
from pathlib import Path
import shutil
import socket
import subprocess
from typing import Literal, Optional

import pkg_resources
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


def _create_gitignore() -> None:
    gitignore = Path('.gitignore')
    if not gitignore.exists():
        # Add a .gitignore file
        infile = pkg_resources.resource_filename(
            'psycho',
            'data/gitignore.txt'
        )
        with gitignore.open('wt', encoding='utf-8') as fout:
            with open(infile, 'rt', encoding='utf-8') as fin:
                fout.write(fin.read())


def _initialize_git() -> None:
    if shutil.which('git') is None:
        return

    # Initialize a git repository
    subprocess.run(['git', 'init'], check=True)
    subprocess.run(['git', 'branch', '-M', 'main'], check=True)


def _create_venv() -> Path:
    # Create a virtual environment
    venv = Path('.') / '.venv'
    if not venv.exists():
        subprocess.run(['python', '-m', 'venv', str(venv)], check=True)
    venv_bin = make_venv_bin(venv)
    venv_python = venv_bin / 'python'
    # Upgrade pip
    subprocess.run(
        [str(venv_python), '-m', 'pip', 'install', '--upgrade', 'pip'],
        check=True
    )
    return venv_python


def _create_readme(name: str, description: str) -> Path:
    readme = Path('README.md')
    if not readme.exists():
        infile = pkg_resources.resource_filename(
            'psycho',
            'data/README.md'
        )
        with readme.open('wt', encoding='utf-8') as fout:
            with open(infile, 'rt', encoding='utf-8') as fin:
                fout.write(
                    fin.read().format(
                        name=name,
                        description=description
                    )
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
        create: Optional[Literal['local', 'local-venv']],
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

    if not create:
        venv_python: Path | None = None
    else:
        _create_src(name)
        _create_gitignore()
        _initialize_git()
        venv_python = _create_venv()
        readme = _create_readme(name, description)
        project.add("readme", str(readme))

    write_pyproject(project_file, pyproject)

    if create and venv_python is not None:
        # install the project in editable mode
        _install_project(venv_python)
