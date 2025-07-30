# Copyright 2022 - 2025 Ternaris
# SPDX-License-Identifier: Apache-2.0
"""Test minimal CLI."""

from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from typing import Annotated


def command(
    grpa_int: Annotated[
        int,
        {
            'group': 'a',
            'flags': ('--grpai',),
        },
    ],
    grpa_float: Annotated[
        float,
        {
            'group': 'a',
            'flags': ('--grpaf',),
        },
    ],
    grpb_int: Annotated[
        int,
        {
            'group': 'b',
            'flags': ('--grpbi',),
        },
    ],
    grpb_float: Annotated[
        int,
        {
            'group': 'b',
            'flags': ('--grpbf',),
        },
    ],
    excc_int: Annotated[
        int,
        tuple(
            {
                'group': 'c',
                'flags': ('--grpci',),
            }.items(),
        ),
    ]
    | None = None,
    excc_float: Annotated[
        float,
        tuple(
            {
                'group': 'c',
                'flags': ('--grpcf',),
            }.items(),
        ),
    ]
    | None = None,
    excd_int: Annotated[
        int,
        tuple(
            {
                'group': 'd',
                'flags': ('--grpdi',),
            }.items(),
        ),
    ]
    | None = None,
    excd_float: Annotated[
        int,
        tuple(
            {
                'group': 'd',
                'flags': ('--grpdf',),
            }.items(),
        ),
    ]
    | None = None,
) -> int:
    """Minimal CLI.

    Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod
    tempor incididunt ut labore et dolore magna aliqua.

    Args:
        grpa_int: Int in group a.
        grpa_float: Float in group a.
        grpb_int: Int in group b.
        grpb_float: Float in group b.
        excc_int: Int in group c.
        excc_float: Float in group c.
        excd_int: Int in group d.
        excd_float: Float in group d.

    Groups:
        a: Group A.
        b: SUPPRESS.

    ExcGroups:
        c: Group C.
        d: SUPPRESS.

    Returns:
        Exit code.

    """
    # pylint:disable=too-many-arguments
    assert grpa_int
    assert grpa_float
    assert grpb_int
    assert grpb_float
    assert excc_int
    assert excc_float
    assert excd_int
    assert excd_float
    return 0


COMMAND = command
