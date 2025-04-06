"""Example code"""

from tomlkit.items import Table, Array
from tomlkit import load, dump, table, array
from packaging.requirements import Requirement


def main() -> None:
    """Main function"""
    with open("pyproject_ex.toml", "rt", encoding="utf-8") as fp:
        pyproject = load(fp)

    if 'project' not in pyproject:
        pyproject['project'] = table()
    project = pyproject["project"]
    if not isinstance(project, Table):
        raise TypeError("project must be a Table")

    if 'dependencies' not in project:
        project['dependencies'] = array()
    dependencies = project["dependencies"]
    if not isinstance(dependencies, Array):
        raise TypeError("dependencies must be an Array")

    req_to_add = Requirement("bareASGI>=4.2.0,<5.0.0")
    for dep in dependencies:
        req = Requirement(dep)
        if req.name == req_to_add.name:
            raise KeyError(f"Dependency {req_to_add} already exists")

    dependencies.append(str(req_to_add))

    with open("pyproject_ex.toml", "wt", encoding="utf-8") as fp:
        dump(pyproject, fp)

    print(f"Dependencies: {dependencies}")


if __name__ == "__main__":
    main()
