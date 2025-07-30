# Copyright 2022 - 2025 Ternaris
# SPDX-License-Identifier: Apache-2.0
"""CLI declaration."""

from __future__ import annotations

import importlib.metadata
import sys
from typing import TYPE_CHECKING, TypedDict

from .check import check_package
from .gen import generate_code

if TYPE_CHECKING:
    from argparse import ArgumentParser
    from typing import Annotated


class Kwargs(TypedDict):
    """All keyword arg types."""

    package: str
    version: bool
    write: bool


def command(
    argparser: ArgumentParser,
    *,
    version: Annotated[
        bool,
        {
            'flags': ['--version'],
        },
    ] = False,
    **kwargs: Kwargs,
) -> int:
    """CLI generator for Python.

    Args:
        argparser: Argument parser,
            with mnoew text.
        version: Print version number.
        kwargs: Rest of all CLI params.

    Groups:
        x: SUPPRESS

    Returns:
        0 if success.

    """
    if version:
        print(importlib.metadata.version('declinate'))  # noqa: T201
        sys.exit(0)

    if not kwargs.get('_command'):
        argparser.print_help()
        sys.exit(0)

    return 1


def generate(
    package: str,
    *,
    write: Annotated[
        bool,
        {
            'flags': ['-w', '--write'],
        },
    ] = False,
) -> int:
    """Generate CLI code.

    This command parses the declarative CLI definition from a Python package
    and generates the code for the CLI.

    Args:
        package: Name of the Python package.
        write: Write cli module into package.

    Returns:
        0 if success.

    """
    code = generate_code(package, write=write)
    if not write:
        print(code)  # noqa: T201
    return 0


def check(package: str) -> int:
    """Check if generated cli is up to date.

    Args:
        package: Name of the Python package.

    Returns:
        0 if success.

    """
    if res := check_package(package):
        print(res)  # noqa: T201
        return 1
    return 0


COMMAND = command

SUBCOMMANDS = [
    generate,
    check,
]
