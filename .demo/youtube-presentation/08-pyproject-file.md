---
theme: default
customLayout: .demo/youtube-presentation/layout.html
author: Rob Blackbourn
date: 24 May 2025
---

# pyproject.toml

The project file would look as follows.

```toml
[project]
name = "my-package"
version = "0.1.0"
description = "My package"
authors = [{name = "Jane Doe", email = "jane.doe@placeholder.com"}]
readme = "README.md"

[build-system]
requires = ["setuptools>=61.0"]
build-backend = "setuptools.build_meta"
```