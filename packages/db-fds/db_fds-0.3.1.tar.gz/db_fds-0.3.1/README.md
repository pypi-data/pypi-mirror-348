# DB-FDs

[![CodeQL](https://github.com/mmaimer33/DB-FDs/actions/workflows/github-code-scanning/codeql/badge.svg)](https://github.com/mmaimer33/DB-FDs/actions/workflows/github-code-scanning/codeql)

DB-FDs is a simple package containing utility functions to work with [**Functional Dependencies**](https://en.wikipedia.org/wiki/Functional_dependency) for Database design.

## Installation

You can install the package from [PyPI](https://pypi.org/project/db-fds/) using [pip](https://pypi.org/project/pip/):

    python -m pip install db-fds

or simply,

    pip install db-fds

Note: If your system does not use Python 3 by default, you may need to replace the command with `python3` or `pip3`, respectively.

The package is supported on Python 3.0 and above.

## How to use

After installation, import it into a Python program with

```py
from db_fds import fdfuncs
```

and use it like

```py
fdfuncs.Symbol("")
```

or

```py
from db_fds.fdfuncs import *

Symbol("")
```

### Classes

The package comes with 2 classes to create objects to work with: `Symbol` and `FunctionalDependency`. Use `Symbol` to represent an attribute in a relation, and create `FunctionalDependency` objects between 2 or more `Symbol`s. See the class and constructor docstrings for details.

## Documentation

Read the documentation in [one place](https://db-fds.readthedocs.io/en/latest/) to see the available functionality.

## Planned future additions

- BCNF and 3NF checks
- Normalization functions
- Checking for lossless decompositions

## How to Contribute

Fork the repository from [https://github.com/mmaimer33/DB-FDs](https://github.com/mmaimer33/DB-FDs) and submit a pull request. Also read the [Code of Conduct](CODE_OF_CONDUCT.md).
