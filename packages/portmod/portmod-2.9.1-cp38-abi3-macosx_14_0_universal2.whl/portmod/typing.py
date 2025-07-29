# Copyright 2024 Portmod Authors
# Distributed under the terms of the GNU General Public License v3

"""
Backport of a typing functions to work with python 3.8
"""

from typing import Any

try:
    from typing import assert_never  # type: ignore
except ImportError:

    def assert_never(value: Any):
        raise AssertionError(f"Expected code to be unreachable, but got: {value}")
