# Copyright 2019-2021 Portmod Authors
# Distributed under the terms of the GNU General Public License v3

"""
Config sorting tests

Note that for the purposes of speed, mods are not removed between tests, and the
removal test occurs at the end. This means that the order of tests may matter,
and you should, when writing tests, assume an arbitrary configuration at the
beginning of the test, and attempt to place the test in such an order as to minimize
the number of changes required to get the desired configuration
"""

import os
from pathlib import Path

import pytest

from portmodlib.fs import _move2, ci_exists, match

from .env import setup_env, tear_down_env


@pytest.fixture(scope="module", autouse=True)
def setup():
    """
    Sets up and tears down the test environment
    """
    setup_env("test")
    yield
    tear_down_env()


def test_ci_exists_nonexistant_file():
    """
    Tests that ci_exists does not recognize a file which does not exist
    """
    assert not ci_exists(os.path.abspath("File.txt"))


def test_ci_exists():
    """
    Tests that ci_exists recognizes files with case differences
    """
    open("File.TXT", "w").close()
    for pattern in ("File.TXT", "file.txt", "FILE.TXT"):
        assert ci_exists(pattern, prefix=os.getcwd())
        assert ci_exists(os.path.abspath(pattern))
        assert ci_exists(pattern)


def test_ci_exists_different_directory():
    """
    Tests that ci_exists recognizes files with case differences
    when the file is not relative to the current working directory
    """
    open("File.TXT", "w").close()
    parent = os.getcwd()
    os.makedirs("test")
    os.chdir("test")
    for pattern in ("File.TXT", "file.txt", "FILE.TXT"):
        assert ci_exists(pattern, prefix=parent)
        assert not ci_exists(pattern)

    os.chdir(parent)
    os.remove("File.TXT")


def test_match():
    """Tests that fs.match matches directories respecting path components"""
    assert match(Path("foo.txt"), "*.txt")
    assert not match(Path("bar/foo.txt"), "*.txt")
    assert match(Path("bar/baz/foo.txt"), "bar/*/*.txt")
    assert not match(Path("bar/baz/foo.txt"), "bar/*")


def test_match_recursive():
    """Tests that fs.match matches directories recursively"""
    assert match(Path("foo.txt"), "**/*.txt")
    assert match(Path("bar/foo.txt"), "**/*.txt")
    assert match(Path("bar/baz/foo.txt"), "**/*.txt")
    assert match(Path("bar/baz/foo.txt"), "**/*")
    assert match(Path("bar"), "**/*")
    assert not match(Path("bar/baz/foo.txt"), "**")
    assert not match(Path("bar"), "**")


def test_move2_symlink():
    os.symlink("foo", "bar")
    for file in os.scandir("."):
        if file.name == "bar":
            _move2(file, "baz")
    assert os.path.islink("baz")
    assert os.readlink("baz") == "foo"
