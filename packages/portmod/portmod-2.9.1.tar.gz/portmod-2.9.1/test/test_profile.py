# Copyright 2019-2021 Portmod Authors
# Distributed under the terms of the GNU General Public License v3

"""
Tests profile loading
"""

from pathlib import Path

import pytest

from portmod.config import get_config
from portmod.config.profiles import get_profile_path, get_system, profile_parents
from portmod.loader import load_all_installed

from .env import setup_env, tear_down_env, unset_profile, select_profile
from .merge import merge


@pytest.fixture(autouse=True, scope="module")
def setup_repo():
    """sets up and tears down test environment"""
    yield setup_env("test")
    tear_down_env()


def test_profile_parents():
    """Tests that all profile parents are resolved correctly"""
    for parent in profile_parents():
        assert Path(parent).resolve()


def test_profile_nonexistant():
    """
    Tests that portmod behaves as expected when the profile does not exist
    """
    unset_profile()
    with pytest.raises(Exception):
        get_profile_path()
    select_profile("test")


def test_system():
    """
    Tests that the system set behaves as expected
    """
    system = get_system()
    assert "test/test" in system

    assert not list(load_all_installed())
    merge(["@world"], update=True)
    mods = list(load_all_installed())
    assert len(mods) == len(system)
    for mod in mods:
        assert mod.CPN in system
    for name in system:
        assert any(mod.CPN == name for mod in mods)


def test_profile_config():
    assert {"ARCH", "USE_EXPAND", "USE_EXPAND_HIDDEN"} <= get_config()[
        "PROFILE_ONLY_VARIABLES"
    ]
