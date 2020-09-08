[![pypi](https://img.shields.io/pypi/v/pytest-eradicate.svg)](https://pypi.python.org/pypi/pytest-eradicate/)

pytest-eradicate
===============================================================

[Pytest](http://pytest.org/) plugin for detecting commented out code in python files.

Changes
-------

- **0.0.5** added compatability for Pytest 5.4 and higher
- **0.0.4** made eradicate 1.0 compatible, added `--agressive` (thanks to @avallbona)

Usage
---------

install via::

    pip install pytest-eradicate

if you then type::

    pytest --eradicate

every file ending in ``.py`` will be discovered and checked
for commented out code.

There is also the option::

    pytest --eradicate --aggressive

make more aggressive changes. This may result in false positives.
Added in order to update to the last version of eradicate like it seems to be the default mode.

Eradicate
---------

Eradicate is a tool to detect commented out code in Python files.

[Eradicate Github](https://github.com/myint/eradicate)

As the developer states commented out code has no place in your repository.

Besides that, commented out code is often an indicator for debug statements left behind or
code moved out of the way during development.
