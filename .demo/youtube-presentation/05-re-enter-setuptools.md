---
theme: default
customLayout: .demo/youtube-presentation/layout.html
author: Rob Blackbourn
date: 24 May 2025
---

# Re-enter setuptools

However, silently, in the background, things were moving in the standard Python
distribution.

The `setup.py` became optional, and finally was replaced by `pyproject.toml`.

The package source could be installed as editable with `pip install -e .`.

There were places to put dependencies, specify the readme, the license file,
repository urls!

So now I've come full circle and I've converted my projects back to **setuptools**!
