# Copyright 2022 - 2025 Ternaris
# SPDX-License-Identifier: Apache-2.0
"""Test minimal CLI."""

from typing import TypedDict


class AddArgs(TypedDict):
    """Default arguments for all commands."""

    arg_foo: int
    arg_bar: str


def addargfn() -> AddArgs:
    """Generate default arguments object."""
    return AddArgs(arg_foo=42, arg_bar='baz')


def command(arg_foo: int, arg_bar: str) -> int:
    """Minimal CLI.

    Args:
        arg_foo: Some value.
        arg_bar: Other value.

    Returns:
        Exit code.

    """
    print(arg_foo, arg_bar)  # noqa: T201
    return 0


def subcommand(arg_foo: int, arg_bar: str) -> int:
    """Minimal CLI.

    Args:
        arg_foo: Some value.
        arg_bar: Other value.

    Returns:
        Exit code.

    """
    print(arg_foo, arg_bar)  # noqa: T201
    return 0


ADDARGFN = addargfn
COMMAND = command
SUBCOMMANDS = [subcommand]
