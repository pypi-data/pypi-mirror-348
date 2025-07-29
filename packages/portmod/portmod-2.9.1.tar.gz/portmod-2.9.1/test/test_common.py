# Copyright 2019-2021 Portmod Authors
# Distributed under the terms of the GNU General Public License v3

"""
Tests common/* packages
"""

import pytest

from .env import setup_env, tear_down_env
from .merge import merge


@pytest.fixture(scope="module", autouse=True)
def setup():
    yield setup_env("test")
    tear_down_env()


def test_common_install():
    """Tests that packages with common dependencies install correctly"""
    merge(["test/test-new"])
    merge(["test/test-new"], depclean=True)
