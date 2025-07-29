# Copyright 2019-2021 Portmod Authors
# Distributed under the terms of the GNU General Public License v3

"""
Tests some otherwise untested parts of the interface
"""

import io
import os
import sys

import pytest

from portmod._cli.main import main
from portmod._cli.merge import CLIMerge
from portmod.globals import env
from portmod.loader import load_installed_pkg
from portmod.merge import merge
from portmodlib.atom import Atom

from .env import connected, setup_env, tear_down_env


@pytest.fixture(scope="module", autouse=True)
def setup():
    data = setup_env("test")
    merge(["@world"], update=True, io=CLIMerge())
    yield data
    tear_down_env()


def test_validate():
    """Tests that validate works correctly"""
    sys.argv = ["portmod", "test", "merge", "test", "test2", "--no-confirm"]
    main()
    sys.argv = ["portmod", "test", "validate"]
    main()


@pytest.mark.skipif(not connected(), reason="Requires network access")
def test_sync():
    """Tests that portmod sync works correctly"""
    sys.argv = ["portmod", "sync"]
    main()


@pytest.mark.parametrize("verbose", [True, False])
def test_info(verbose):
    """Tests that portmod info works correctly"""
    sys.argv = ["portmod", "test", "info"]
    if verbose:
        sys.argv.append("--verbose")
    with pytest.raises(SystemExit) as exc_info:
        main()
        assert exc_info.value.returncode == 0


def test_search(monkeypatch):
    """Tests that portmod search works correctly"""
    sys.argv = ["portmod", "test", "search", "test"]
    monkeypatch.setattr("sys.stdin", io.StringIO("\n"))
    main()


def test_use():
    """Tests that portmod use works correctly"""
    sys.argv = ["portmod", "test", "use", "-E", "foo"]
    main()
    sys.argv = ["portmod", "test", "merge", "test4", "--no-confirm"]
    main()
    pkg = load_installed_pkg(Atom("test/test4"))
    assert pkg
    assert "foo" in pkg.get_use()


def test_mirror():
    """Tests that `portmod mirror` works correctly"""
    sys.argv = ["portmod", "mirror", os.path.join(env.TMP_DIR, "mirror"), "test"]
    main()


def test_outdated(capsys):
    """Tests that `portmod <prefix> outdated` works correctly"""
    sys.argv = ["portmod", "test", "outdated"]
    main()
    captured = capsys.readouterr().out
    assert "All packages are up to date!\n" == captured
    merge(["test/test-1.0"], io=CLIMerge())
    # Clear output
    capsys.readouterr()
    sys.argv = ["portmod", "test", "outdated"]
    main()
    captured = capsys.readouterr().out
    print(captured)
    assert "All packages are up to date!" not in captured
    assert "1.0-r2" in captured
    assert "2.0" in captured
    assert "Ready for world update" in captured
