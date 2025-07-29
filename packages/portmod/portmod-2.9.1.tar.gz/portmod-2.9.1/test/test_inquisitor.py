# Copyright 2019-2021 Portmod Authors
# Distributed under the terms of the GNU General Public License v3

"""
Portmod config tests
"""

import os
import sys
from logging import error

import pytest

from portmod._cli.inquisitor import main, scan_file, scan_path, scan_sources

from .env import TEST_REPO, connected, setup_env, tear_down_env


@pytest.fixture(scope="module", autouse=True)
def setup():
    """
    Sets up and tears down the test environment
    """
    dictionary = setup_env("test")
    yield dictionary
    tear_down_env()


def test_inquisitor():
    """
    Basic inquisitor test on test repo
    """
    has_error = False

    def err(string: str):
        nonlocal has_error
        error(string)
        has_error = True

    scan_path(TEST_REPO.location, TEST_REPO.location, err)
    for path_root, _, filenames in os.walk(TEST_REPO.location):
        scan_path(path_root, TEST_REPO.location, err)
        os.chdir(path_root)
        for filename in filenames:
            scan_file(filename, TEST_REPO.location, err)
            scan_path(filename, TEST_REPO.location, err)
    if has_error:
        raise Exception("Inqusitor failed. See error log for details.")


def test_inquisitor_main():
    """
    Basic inquisitor test on test repo
    """
    sys.argv = ["inquisitor", "scan", TEST_REPO.location]
    main()


@pytest.mark.skipif(not connected(), reason="Requires network access")
def test_scan_sources():
    has_error = False

    def err(string: str):
        nonlocal has_error
        error(string)
        has_error = True

    scan_sources(
        os.path.join(
            TEST_REPO.location,
            "test",
            "quill-of-feyfolken",
            "quill-of-feyfolken-2.0.2.pybuild",
        ),
        err,
    )
    assert not has_error, "Source should be available"


# TODO: Add tests that modify the test repo to be invalid
