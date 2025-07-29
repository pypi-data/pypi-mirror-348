# Copyright 2019-2021 Portmod Authors
# Distributed under the terms of the GNU General Public License v3

import pytest

from portmod._deps import resolve
from portmod.config.sets import add_set, get_set, remove_set
from portmod.config.use import add_global_use
from portmod.loader import load_installed_pkg
from portmod.transactions import Downgrade, New, Reinstall, Update
from portmodlib.atom import Atom, Version

from .env import setup_env, tear_down_env
from .merge import merge


@pytest.fixture(scope="module", autouse=True)
def setup():
    """
    Sets up and tears down the test environment
    """
    dictionary = setup_env("test")
    yield dictionary
    tear_down_env()


def test_simple(setup):
    """Tests that simple dependency resolution works"""
    selected = {Atom("test/test")}
    transactions = resolve(selected, set(), selected, selected, set())
    assert len(transactions.pkgs) == 1
    assert transactions.pkgs[0].pkg.CPN == "test/test"
    assert isinstance(transactions.pkgs[0], New)

    merge(["test/test"])
    transactions = resolve(selected, set(), selected, selected, set())
    assert len(transactions.pkgs) == 1
    assert transactions.pkgs[0].pkg.CPN == "test/test"
    assert isinstance(transactions.pkgs[0], Reinstall)


def test_rebuild(setup):
    """
    Tests that packages are selected to be rebuilt, even if we don't
    use the Category-PackageName format
    """
    selected = {Atom("~test/test-1.0")}
    merge(selected)
    transactions = resolve(selected, set(), selected, selected, set())
    assert len(transactions.pkgs) == 1
    assert transactions.pkgs[0].pkg.CPN == "test/test"
    assert transactions.pkgs[0].pkg.REPO == "test"
    assert isinstance(transactions.pkgs[0], Reinstall)


def test_upgrade(setup):
    """Tests that upgrades resolve correctly"""
    selected = {Atom("test/test")}
    transactions = resolve(selected, set(), selected, selected, set())
    assert len(transactions.pkgs) == 1
    assert transactions.pkgs[0].pkg.version > Version("1.0")
    assert isinstance(transactions.pkgs[0], Update)


def test_oneshot(setup):
    """Tests that oneshot resolves correctly"""
    selected = {Atom("test/test")}
    merge(selected)
    transactions = resolve(selected, set(), selected, set(), set())
    assert len(transactions.pkgs) == 1
    assert not transactions.pkgs[0].pkg.version > Version("2.0")
    assert not Version("2.0") > transactions.pkgs[0].pkg.version
    assert Version("2.0") == transactions.pkgs[0].pkg.version
    assert isinstance(transactions.pkgs[0], Reinstall)
    assert not transactions.new_selected


def test_downgrade(setup):
    """Tests that downgrades resolve correctly"""
    merge(["=test/test-2.0"])
    selected = {Atom("=test/test-1.0")}
    transactions = resolve(selected, set(), selected, selected, set())
    assert len(transactions.pkgs) == 1
    assert Version("2.0") > transactions.pkgs[0].pkg.version
    assert isinstance(transactions.pkgs[0], Downgrade)


def test_auto_depclean(setup):
    """
    Tests that auto depclean doesn't change configuration to remove packages

    There are two possible changes that it shouldn't make for this test.
    test7-1.0 could be downgraded to test7-0.1 to remove the dependencies
    And test7-1.0's flags could be disabled to remove the dependencies.
    """
    merge(["=test/test7-1.0[baz]"])
    pkg = load_installed_pkg(Atom("test/test5"))
    assert pkg
    transactions = resolve(
        enabled={Atom("test/test7")},
        disabled=set(),
        explicit={Atom("test/test7")},
        selected=set(),
        selected_sets={"world"},
        update=True,
        deep=True,
        depclean=True,
    )
    assert len(transactions.pkgs) == 0


def test_upgrade_configuration(setup):
    """
    Tests that upgrades will pull in new packages and change configuration if necessary
    """
    merge(["@installed"], delete=True)
    merge(
        ["=test/test7-0.1"],
        update=True,
        deep=True,
    )
    add_global_use("baz")
    pkg = load_installed_pkg(Atom("test/test5"))
    assert not pkg
    transactions = resolve(
        enabled=get_set("world"),
        disabled=set(),
        explicit=get_set("world"),
        selected=set(),
        selected_sets={"world"},
        update=True,
        deep=True,
    )
    for change in transactions.config:
        raise Exception(f"Unexpected configuration change {change}")
    assert len(transactions.pkgs) == 3
    for change in transactions.pkgs:
        if isinstance(change, Update):
            assert change.pkg.P == "test7-1.0"
        elif isinstance(change, New):
            assert change.pkg.PN in {"test5", "test4"}
        else:
            raise Exception(f"Unexpected transaction ({change.REPR}) {change.pkg}")

    merge(["test/test7"], depclean=True)


def test_nondeep_depth(setup):
    """
    Tests that, when not using deep mode, packages which are in the world set but
    have not been installed will pull in all their dependencies
    """
    add_set("selected-packages", Atom("=test/test6-1.0"))
    transactions = resolve(
        enabled=set(),
        disabled=set(),
        explicit=set(),
        selected=set(),
        selected_sets=set(),
        update=True,
    )
    # test6 depends on test3 which depends on test4
    packages = ["test6", "test3", "test4"]
    for change in transactions.pkgs:
        assert isinstance(change, New)
        assert change.pkg.PN in packages
        packages.remove(change.pkg.PN)

    assert not packages
    remove_set("selected-packages", Atom("=test/test6-1.0"))
