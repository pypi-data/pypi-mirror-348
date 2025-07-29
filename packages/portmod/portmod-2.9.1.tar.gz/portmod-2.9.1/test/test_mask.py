# Copyright 2019-2021 Portmod Authors
# Distributed under the terms of the GNU General Public License v3

import os

import pytest

from portmod._deps import DepError, resolve
from portmod.config.mask import get_masked, get_unmasked, is_masked
from portmod.globals import env
from portmod.loader import load_pkg
from portmod.transactions import New
from portmodlib.atom import Atom, atom_sat

from .env import setup_env, tear_down_env


@pytest.fixture(scope="module", autouse=True)
def setup():
    """
    Sets up and tears down the test environment
    """
    dictionary = setup_env("test")
    yield dictionary
    tear_down_env()


@pytest.fixture(autouse=True)
def clear_cache():
    get_masked.cache_clear()
    get_unmasked.cache_clear()
    is_masked.cache_clear()
    yield
    get_masked.cache_clear()
    get_unmasked.cache_clear()
    is_masked.cache_clear()


def test_mask(setup):
    """Tests that masking packages prevents them from being installed"""
    selected = {Atom("test/test")}
    with open(os.path.join(env.prefix().CONFIG_DIR, "package.mask"), "w") as file:
        print("test/test", file=file)

    with pytest.raises(DepError):
        resolve(selected, set(), selected, selected, set())


def test_unmask(setup):
    """Tests that simple resolution works"""
    selected = {Atom("test/test")}
    with open(os.path.join(env.prefix().CONFIG_DIR, "package.mask"), "w") as file:
        print("test/test", file=file)

    with open(os.path.join(env.prefix().CONFIG_DIR, "package.unmask"), "w") as file:
        print("=test/test-1.0", file=file)

    transactions = resolve(selected, set(), selected, selected, set())
    assert len(transactions.pkgs) == 1
    assert isinstance(transactions.pkgs[0], New)
    assert atom_sat(transactions.pkgs[0].pkg.ATOM, Atom("=test/test-1.0"))


def test_profile_mask(setup):
    """Tests that masked packages in the profile prevents them from being installed"""
    selected = {Atom("=test/masked-1.1")}

    with pytest.raises(DepError):
        resolve(selected, set(), selected, selected, set())


def test_common_mask(setup):
    """Tests that masked common packages prevents installation but not loading"""
    selected = {Atom("=test/masked-1.0")}

    assert load_pkg(Atom("=test/masked-1.0"))

    with pytest.raises(DepError):
        resolve(selected, set(), selected, selected, set())
