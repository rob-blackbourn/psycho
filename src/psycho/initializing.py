from pathlib import Path

from tomlkit import document, table, array, inline_table

from .projects import write_pyproject


def initialize(
        project_file: Path,
        name: str,
        version: str,
        description: str | None,
        author: str | None = None,
        email: str | None = None,
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
