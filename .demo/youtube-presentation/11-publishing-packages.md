---
theme: default
customLayout: .demo/youtube-presentation/layout.html
author: Rob Blackbourn
date: 24 May 2025
---

# Publishing packages

To publish a package, it needs to be built (`python -m build`) and then uploaded
to the pie store (`twine upload dist/*`).

With **psycho** this gets automated into one step.

```bash
(.venv) ~/my-package $ psycho publish
```

To handle authentication I put my credentials in `~/.pypirc`.

```ini
[pypi]
  username = __token__
  password = pypi-ABCDEFGHIJKLMNOPQRSTUVWXYZ
```
