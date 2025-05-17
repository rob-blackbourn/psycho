---
theme: default
layout: default
---

# A lot has changed

The original solution was based on a set of independent tools produced by the
python packaging authority or pypa [https://github.com/pypa](https://github.com/pypa).

* pip
* virtualenv
* build
* twine
* setuptools

The information need to pack, and unpack a python package was put in a small
program called `setup.py` (which is where the *setuptools* package enters the
frame). With the exception of *build* and *twine*, these tools come bundled with
the standard distribution.

I hated `setup.py`. It was configuration in code. It looked bad and it smelt bad.
