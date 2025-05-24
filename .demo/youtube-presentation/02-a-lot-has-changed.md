---
theme: default
customLayout: .demo/youtube-presentation/layout.html
author: Rob Blackbourn
date: 24 May 2025
---

# A lot has changed

The original packaging solution was based on a set of individual tools produced by the
python packaging authority or pypa [https://github.com/pypa](https://github.com/pypa).

* pip
* virtualenv
* build
* twine
* setuptools

The information needed to pack, and unpack a python package was put in a small
program called `setup.py` (which is where the *setuptools* package enters the
frame). With the exception of *build* and *twine*, all these tools come bundled with
the standard distribution.

I hated `setup.py`. It was configuration in code. It looked bad and it smelt bad.
