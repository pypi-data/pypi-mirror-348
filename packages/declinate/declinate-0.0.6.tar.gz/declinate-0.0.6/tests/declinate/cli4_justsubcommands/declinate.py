# Copyright 2022 - 2025 Ternaris
# SPDX-License-Identifier: Apache-2.0
"""Test minimal CLI."""

from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from typing import NoReturn


def command(**kwargs: int) -> NoReturn:
    """Minimal CLI.

    Args:
        kwargs: Allargs.

    """
    assert kwargs
    while True:
        pass


async def subcommand(number: int) -> int:
    """Execute subcommand.

    Args:
        number: A number.

    Returns:
        Exit code.

    """
    assert isinstance(number, int)
    await subcommand(0)
    return 0


COMMAND = command
SUBCOMMANDS = [subcommand]
