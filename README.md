# Let's go psycho!

Python project management automation using standard build tools.

<p align="center">
<a href="https://github.com/rob-blackbourn/psycho/raw/main/psycho-demo.gif">
<img src="https://github.com/rob-blackbourn/psycho/raw/main/psycho-demo.gif"/>
</a>
</p>

## Status

This project is a working prototype.

This package is available from [pypi](https://pypi.org/project/psycho/),
but the best way to install it is with [pipx](https://github.com/pypa/pipx).

```bash
pipx install psycho
```

## Overview

Python projects are migrating away from using `setup.py` to `pyproject.toml`.
While a number of excellent projects provide custom tooling, there is no built
in support for automating project management with just the standard tools:

* [setuptools](https://pypi.org/project/setuptools/)
* [pip](https://pypi.org/project/pip/)
* [build](https://pypi.org/project/build/)
* [twine](https://pypi.org/project/twine/)

## Psychotic Commands

The following are supported.

* init
* install
* uninstall
* build
* upload
* publish

### init

Makes a new `pyproject.toml`. The command prompts for input.

```bash
$ psycho init
Name: my-package
Version [0.1.0]: 
Description: My package
Author: rob
Email: rob@example.com
Initializing my-package
```

Alternatively values can be provided as arguments.

```bash
$ psycho init \
    --name my-package \
    --version 0.1.0 \
    --description "My package" \
    --author "Rob Blackbourn" \
    --email "rob@example.com"
```

Or by passing `-y` to accept the defaults.

```bash
$ psycho init -y
```

This creates the standard project structure, with a local virtual environment.
It will also upgrade pip and install the project in the virtual environment.

The following flags are also supported:

* `--no-venv` to not create a virtual environment.
* `--no-tests` to not create the tests folder.
* `--no-upgrade` to prevent the venv dependencies being upgraded (pip).
* `--venv <venv-name>` to give the venv folder a specific name (the default is ".venv").

### install

When used without specifying packages this command installs the project as editable.

```bash
$ psycho install
```

This is the equivalent of `pip install --editable .`.

When used with a package requirement, the requirement is written to the `pyproject.toml`
and the package is installed into the python environment using `pip`.

```bash
$ psycho install "pandas>=1.5.3"
```

The `-optional` flag can be used (with a group name) to add an optional dependency.

```bash
$ psycho install --optional dev pytest
```

Most the flags used by pip are available to this command.

### uninstall

This command removes a package from the `pyproject.toml` file, and uninstalls
it using `pip`.

```bash
$ psycho uninstall pandas
```

This can be used with the optional flag (with a group name) to uninstall an optional
dependency.

```bash
$ psycho uninstall --optional dev pytest
```

### build

The build command will build a package, prior to publishing it.

```bash
$ psycho build
```

This is the equivalent of `python -m build`.

### upload

The upload command will upload a package with twine.

```bash
$ psycho upload
```

This is the equivalent of `twine upload dist/*`.

### publish

This combines the build and publish in one command.

```bash
$ psycho publish
```
