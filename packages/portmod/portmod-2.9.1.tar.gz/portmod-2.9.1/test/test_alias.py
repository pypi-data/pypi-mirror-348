# Copyright 2019-2021 Portmod Authors
# Distributed under the terms of the GNU General Public License v3

"""
Tests for use flag aliases
"""

import pytest

from portmod.config.use import remove_use
from portmod.globals import env
from portmod.loader import SandboxedError, load_installed_pkg
from portmod.repos import get_repos
from portmodlib.atom import Atom

from .env import setup_env, tear_down_env
from .merge import merge


@pytest.fixture(scope="module", autouse=True)
def setup():
    """sets up and tears down test environment"""
    dictionary = setup_env("test")
    env.REPOS = get_repos()
    yield dictionary
    tear_down_env()


def test_simple_alias(setup):
    """Tests that use flag aliases match the installed state of the aliased package"""
    merge(["test/test2"])

    pkg = load_installed_pkg(Atom("test/test2"))
    assert pkg
    assert "alias1" not in pkg.INSTALLED_USE
    assert "alias2" not in pkg.INSTALLED_USE

    merge(
        ["test/test2", "test/test7"],
        deep=True,
        update=True,
        verbose=True,
    )

    pkg = load_installed_pkg(Atom("test/test2"))
    assert pkg
    assert "alias1" in pkg.INSTALLED_USE
    assert "alias2" not in pkg.INSTALLED_USE

    merge(["test/test2", "test/test7"], delete=True)


def test_alias_with_use_flag(setup):
    """Tests that use flag aliases with use flag dependencies behave correctly"""
    merge(["test/test2"])

    pkg = load_installed_pkg(Atom("test/test2"))
    assert pkg
    assert "alias1" not in pkg.INSTALLED_USE
    assert "alias2" not in pkg.INSTALLED_USE

    merge(
        ["test/test2", "test/test4"],
        deep=True,
        update=True,
    )

    pkg = load_installed_pkg(Atom("test/test2"))
    assert pkg
    assert "alias1" not in pkg.INSTALLED_USE
    assert "alias2" not in pkg.INSTALLED_USE

    merge(
        ["test/test2", "test/test4[foo]"],
        deep=True,
        update=True,
    )

    pkg = load_installed_pkg(Atom("test/test2"))
    assert pkg
    assert "alias1" not in pkg.INSTALLED_USE
    assert "alias2" in pkg.INSTALLED_USE

    merge(["test/test2", "test/test4"], delete=True)
    remove_use("foo", Atom("test/test4"))


def test_alias_nofetch(setup):
    """Tests that use flag aliases work correctly in the scope of pkg_nofetch"""
    # Should raise an exception if
    with pytest.raises(SandboxedError):
        merge(
            ["test/test-nofetch", "test/test4[foo]"],
            deep=True,
            update=True,
        )
