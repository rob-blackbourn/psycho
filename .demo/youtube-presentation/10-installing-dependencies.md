---
theme: default
layout: default
---

# Installing dependencies

The next time saver is adding and removing dependencies. This involves editing
the `dependencies` list in the `project` section of `pyproject.toml` and calling
`pip install` on the package. With psycho this looks like this:

```bash
(.venv) ~/my-package $ psycho install polars
```

Installing optional dependencies takes a flag and an option group.

```bash
(.venv) ~/my-package $ psycho install --optional dev 'pytest>=8,<9'
```

There is a complimentary `uninstall` command.
```bash
(.venv) ~/my-package $ psycho uninstall polars
(.venv) ~/my-package $ psycho uninstall --optional dev 'pytest'
```
