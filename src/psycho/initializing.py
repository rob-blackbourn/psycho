from pathlib import Path
import shutil
import subprocess
from typing import Literal, Optional

import pkg_resources
from tomlkit import document, table, array, inline_table

from .paths import make_venv_bin
from .projects import write_pyproject


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

    write_pyproject(project_file, pyproject)

    if not create:
        return

    # Create a source directory
    package_name = name.replace('-', '_')
    package_dir = Path('src') / package_name
    package_dir.mkdir(parents=True, exist_ok=True)
    init_file = package_dir / '__init__.py'
    if not init_file.exists():
        init_file.touch()

    gitignore = Path('.gitignore')
    if not gitignore.exists():
        # Add a .gitignore file
        infile = pkg_resources.resource_filename(
            'psycho', 'data/gitignore.txt')
        with gitignore.open('wt', encoding='utf-8') as fout:
            with open(infile, 'rt', encoding='utf-8') as fin:
                fout.write(fin.read())

    if shutil.which('git') is not None:
        # Initialize a git repository
        subprocess.run(['git', 'init'], check=True)

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

    # install the project in editable mode
    subprocess.run(
        [str(venv_python), '-m', 'pip', 'install', '-e', '.'],
        check=True
    )
