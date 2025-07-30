# Copyright 2022 - 2025 Ternaris
# SPDX-License-Identifier: Apache-2.0
"""CLI generators."""

from __future__ import annotations

import importlib
from pathlib import Path

from .gen import generate_code


def check_package(package: str) -> str | None:
    """Check if package CLI is up to date.

    Args:
        package: Name of package to check.

    Returns:
        Instructions how to update package or None.

    """
    code = generate_code(package, write=False)
    module = importlib.import_module(name=package)
    assert module
    assert module.__file__
    clipath = Path(module.__file__).parent / 'cli.py'
    if not clipath.exists() or clipath.read_text() != code:
        return f'CLI is outdated, run "declinate generate -w {package}"'
    return None
