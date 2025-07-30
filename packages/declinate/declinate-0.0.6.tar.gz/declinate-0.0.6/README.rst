.. image:: https://gitlab.com/ternaris/declinate/badges/master/pipeline.svg
   :target: https://gitlab.com/ternaris/declinate/-/commits/master
   :alt: pipeline status

.. image:: https://gitlab.com/ternaris/declinate/badges/master/coverage.svg
   :target: https://gitlab.com/ternaris/declinate/-/commits/master
   :alt: coverage report

.. image:: https://img.shields.io/pypi/pyversions/declinate
   :alt: python versions

=========
Declinate
=========

Declinate is a command line interface generator. It is a development tool that parses function type annotations and docstrings to generate Python CLIs:

- It uses **builtin language features** to describe CLIs.
- Declinate is **not a runtime dependency**, it compiles to vanilla Python argparse calls during development.
- Generated CLIs use lazy imports, resulting in **extremely fast startup time**.
- **Command completion** for Bash and Zsh are added by default.


Getting started
===============

Declinate is published on PyPI and does not have any special dependencies. Simply install with pip::

   pip install declinate


The package installs the ``declinate`` command to generate a CLI for a python package::

   # Print python code to stdout.
   declinate generate example_pkg

   # Write cli.py module in example_pkg package.
   declinate generate -w example_pkg


Of course, declinate's own CLI is "self-hosting" and can recreate itself::

   declinate generate declinate


Declinate expects the python package to declare its command and subcommands in a module named ``declinate.py``. Here is how declinate's own "check" subcommand is declared:

.. code-block:: python

   def check(package: str) -> int:
       """Check if generated cli is up to date.

       Args:
           package: Name of the Python package.

       Returns:
           0 if success.

       """
       if res := check_package(package):
           print(res)
           return 1
       return 0


Take a closer look at the different example CLIs in the tests package that demonstrate the various features.


Documentation
=============

Read the `documentation <https://ternaris.gitlab.io/declinate/>`_ for further information.

.. end documentation


Contributing
============

Thank you for considering to contribute to declinate.

To submit issues or create merge requests please follow the instructions provided in the `contribution guide <https://gitlab.com/ternaris/declinate/-/blob/master/CONTRIBUTING.rst>`_.

By contributing to declinate you accept and agree to the terms and conditions laid out in there.


Development
===========

Clone the repository and setup your local checkout::

   git clone https://gitlab.com/ternaris/declinate.git

   cd declinate
   python -m venv venv
   . venv/bin/activate

   pip install -r requirements-dev.txt
   pip install -e .


This creates a new virtual environment with the necessary python dependencies and installs declinate in editable mode. The declinate code base uses pytest as its test runner, run the test suite by simply invoking::

   pytest


To build the documentation from its source run sphinx-build::

   sphinx-build -a docs public


The entry point to the local documentation build should be available under ``public/index.html``.


Support
=======

Professional support is available from `Ternaris <https://ternaris.com>`_.
