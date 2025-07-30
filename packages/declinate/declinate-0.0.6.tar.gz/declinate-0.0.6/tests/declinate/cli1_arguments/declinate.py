# Copyright 2022 - 2025 Ternaris
# SPDX-License-Identifier: Apache-2.0
"""Test minimal CLI."""

from __future__ import annotations

from pathlib import Path
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from argparse import ArgumentParser
    from typing import Annotated


def command(
    argparser: ArgumentParser,
    decimal: int,
    fraction: Annotated[float, ()],
    string: str,
    path: Path,
    boolean: Annotated[
        bool,
        {
            'flags': ['--bool'],
        },
    ],
    *,
    deffalse_boolean: Annotated[
        bool,
        {
            'flags': ['--deffalse'],
        },
    ] = False,
    deftrue_boolean: Annotated[
        bool,
        {
            'flags': ['--deftrue'],
        },
    ] = True,
    optional_number: Annotated[int, (('flags', ('--opt',)),)] | None = 42,
    helpover: Annotated[
        int,
        {
            'help': 'Overridden help.',
        },
    ] = 43,
) -> int:
    """Minimal CLI.

    Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod
    tempor incididunt ut labore et dolore magna aliqua.

    Args:
        argparser: ArgParser.
        decimal: An int.
        fraction: A float.
        string: A string.
        path: A path.
        boolean: A bool.
        deffalse_boolean: A bool usually false.
        deftrue_boolean: A bool usually true.
        optional_number: An optional int.
        helpover: Original help.

    Returns:
        Exit code.

    """
    # pylint:disable=too-many-arguments
    assert hasattr(argparser, 'parse_args')
    assert isinstance(decimal, int)
    assert isinstance(fraction, float)
    assert isinstance(string, str)
    assert isinstance(path, Path)
    assert isinstance(boolean, bool)
    assert isinstance(deffalse_boolean, bool)
    assert isinstance(deftrue_boolean, bool)
    assert isinstance(optional_number, int)
    assert isinstance(helpover, int)
    return 0


COMMAND = command
