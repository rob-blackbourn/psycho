# psycho

Python project management automation using standard build tools.

## Status

This project is a working prototype.

It can be installed from pypi:

```bash
pip install psycho
```

## Overview

Python projects are migrating away from using `setup.py` to `pyproject.toml`.
While a number of excellent projects provide custom tooling, there is no built
in support for automating project management with the standard tools:

* [pip](https://pypi.org/project/pip/)
* [build](https://pypi.org/project/build/)
* [twine](https://pypi.org/project/twine/)

## Psychotic Commands

The following are supported.

* install
* uninstall
* build
* publish

### install

When used without specifying packages this command installs the project as editable.

```bash
# equivalent to: pip install --editable .
psycho install
```

When used with a package requirement, the requirement is written to the `pyproject.toml`
and the package is installed into the python environment using `pip`.

```bash
psycho install "pandas>=1.5.3"
```

The `-optional` flag can be used (with a group name) to add an optional dependency.

```bash
psycho install --optional dev pytest
```

### uninstall

This command removes a package from the `pyproject.toml` file, and uninstalls
it using `pip`.

```bash
psycho uninstall pandas
```

This can be used with the optional flag (with a group name) to uninstall an optional
dependency.

```bash
psycho install --optional dev pytest
```

### build

The build command will build a package, prior to publishing it.

```bash
# The equivalent of: python -m build
psycho build
```

### publish

The publish command will upload a package with twine.

```bash
# The equivalent of: twine upload dist/*
psycho publish
```
