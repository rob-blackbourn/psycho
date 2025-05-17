---
theme: default
layout: default
---

# Let's go psycho!

```bash
pipx install psycho
```

We can create the project using `psycho init`. The information will be prompted for.

```bash
~ $ mkdir my-project
~ $ cd my-project
~/my-project $ psycho init --create local-venv
 Name [my-project]:
 Version [0.1.0]:
 ...
```

This command:

* Creates the folder structure and the `pyproject.toml`.
* Initializes a git repo `.git/` with a `.gitignore`.
* Creates a virtual environment as `.venv/`.
* Installs the project with `pip install -e .` in the virtual environment.