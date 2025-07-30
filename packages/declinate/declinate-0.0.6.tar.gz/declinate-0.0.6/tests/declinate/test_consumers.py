# Copyright 2022 - 2025 Ternaris
# SPDX-License-Identifier: Apache-2.0
"""Consumer Tests."""

import pytest

from declinate.check import check_package


@pytest.mark.parametrize(
    'package',
    [
        'cli0_minimal',
        'cli1_arguments',
        'cli2_groups',
        'cli3_withsubcommands',
        'cli4_justsubcommands',
        'cli5_addargfn',
    ],
)
def test_consumers(package: str) -> None:
    """Test different CLIs."""
    assert check_package(f'tests.declinate.{package}') is None
