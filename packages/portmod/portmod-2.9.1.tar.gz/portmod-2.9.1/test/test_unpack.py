# Copyright 2022 Portmod Authors
# Distributed under the terms of the GNU General Public License v3

"""
Tests file master detection
"""

import pytest

from portmod._cli.merge import CLIInstall
from portmod.loader import load_pkg
from portmod.package import install_pkg
from portmodlib.atom import Atom

from .env import connected, setup_env, tear_down_env


@pytest.fixture(scope="module", autouse=True)
def setup_repo():
    """sets up and tears down test environment"""
    yield setup_env("test")
    tear_down_env()


@pytest.mark.skipif(not connected(), reason="Requires network access")
def test_unpack():
    """
    Tests that src_unpack works as expected for Pybuild2

    Checks are inside the package
    """
    pkg = load_pkg(Atom("=test/quill-of-feyfolken-2.0.2-r1"))[0]
    install_pkg(pkg, set(), io=CLIInstall(pkg.ATOM))
