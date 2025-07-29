# Copyright 2019-2021 Portmod Authors
# Distributed under the terms of the GNU General Public License v3

import os
import sys
import tempfile
from functools import lru_cache
from typing import Any, List, Optional

import portmod
from portmodlib.globals import download_dir
from portmodlib.l10n import l10n
from portmodlib.portmod import directories


@lru_cache()
def get_version() -> str:
    """Returns portmod version"""
    try:
        from ._version import version

        return str(version)
    except ImportError:
        osp = os.path
        possible_root = osp.dirname(osp.dirname(osp.realpath(__file__)))
        if osp.isfile(osp.join(possible_root, ".portmod_not_installed")):
            # Only a dev dependency and is otherwise unneeded at runtime
            import setuptools_scm

            return str(setuptools_scm.get_version(possible_root))
        else:
            if sys.version_info[1] >= 8:
                from importlib.metadata import version as version_func
            else:
                from importlib_metadata import version as version_func

            return str(version_func("portmod"))


def get_authors() -> List[str]:
    import git

    repo = os.path.dirname(os.path.dirname(__file__))
    if os.path.exists(os.path.join(repo, ".git")):
        gitrepo = git.Repo.init(repo)
        results = []
        for line in gitrepo.git.shortlog(
            "v1.0.1..", numbered=True, summary=True
        ).splitlines():
            _commits, author = line.strip().split("\t")
            results.append(author)
        return results

    return ["Portmod Authors"]


class Env:
    STRICT = False
    DEBUG = False
    DATA_DIR: str = str(directories.data_dir)
    CONFIG_DIR: str = str(directories.config_dir)
    CACHE_DIR: str = str(directories.cache_dir)
    INTERACTIVE = True
    TESTING = False
    PREFIX_NAME: Optional[str] = None
    REPOS: List["portmod.repo.LocalRepo"]

    # The following variables are none if a prefix has not been selected
    class Prefix:
        REPOS: List["portmod.repo.LocalRepo"]

        def __init__(self, prefix_name: str):
            from portmod.prefix import get_prefixes

            if prefix_name not in get_prefixes():
                raise Exception(l10n("invalid-prefix", prefix=prefix_name))

            prefix = get_prefixes()[prefix_name]

            self.ARCH: str = prefix.arch
            self.CONFIG_DIR: str = os.path.join(env.CONFIG_DIR, prefix_name)
            self.SET_DIR: str = os.path.join(self.CONFIG_DIR, "sets")
            self.CONFIG: str = os.path.join(self.CONFIG_DIR, "portmod.conf")

            self.ROOT: str = os.path.realpath(
                prefix.path or os.path.join(env.DATA_DIR, prefix_name)
            )
            self.CACHE_DIR = os.path.join(env.CACHE_DIR, "prefix", prefix_name)
            self.PYBUILD_INSTALLED_CACHE = os.path.join(
                self.CACHE_DIR, "installed-pybuilds"
            )
            self.PYBUILD_CACHE = os.path.join(self.CACHE_DIR, "pybuild")
            self.CONFIG_PROTECT_DIR = os.path.join(self.CACHE_DIR, "cfg_protect")
            self.LOCAL_MODS = os.path.join(self.ROOT, "local")
            self.REPOS = []

        def __setattr__(self, name: str, value: Any):
            if isinstance(value, str):
                os.environ["PORTMOD_" + name] = value
            super().__setattr__(name, value)

    def prefix(self) -> Prefix:
        if self.PREFIX_NAME is not None:
            return self._prefix
        raise Exception("Internal error: Prefix has not been initialized!")

    def set_prefix(self, prefix: Optional[str]) -> Optional[str]:
        from portmod.lock import has_prefix_exclusive_lock, has_prefix_lock
        from portmod.repos import get_repos

        OLD_PREFIX_NAME = self.PREFIX_NAME
        if self.PREFIX_NAME:
            if has_prefix_exclusive_lock() or has_prefix_lock():
                raise Exception("Cannot change prefix while a lock is acquired!")

        if prefix:
            self._prefix = Env.Prefix(prefix)
            self.PREFIX_NAME = prefix
            self._prefix.REPOS = get_repos()
        else:
            self.PREFIX_NAME = None
        return OLD_PREFIX_NAME

    def __init__(self):
        self.PREFIX_FILE = os.path.join(self.DATA_DIR, "prefix")
        self.REPOS_DIR = os.path.join(self.DATA_DIR, "repos")
        self.PYBUILD_CACHE_DIR = os.path.join(self.CACHE_DIR, "pybuild")
        self.DOWNLOAD_DIR = download_dir()
        self.GLOBAL_PORTMOD_CONFIG = os.path.join(self.CONFIG_DIR, "portmod.conf")
        self.REPOS_FILE = os.path.join(self.CONFIG_DIR, "repos.cfg")
        self.REPOS = []

        tempfile.tempdir = None
        self.TMP_DIR = os.path.join(tempfile.gettempdir(), "portmod")
        self.PYBUILD_TMP_DIR = os.path.join(self.TMP_DIR, "pybuild")
        self.WARNINGS_DIR = os.path.join(self.PYBUILD_TMP_DIR, "messages")
        self.MESSAGES_DIR = os.path.join(self.PYBUILD_TMP_DIR, "warnings")
        self.TMP_VDB = os.path.join(self.TMP_DIR, "tmpdb")
        self.INDEX = os.path.join(self.CACHE_DIR, "index")

    def __setattr__(self, name: str, value: Any):
        if isinstance(value, str):
            os.environ["PORTMOD_" + name] = value
        super().__setattr__(name, value)


env = Env()

# Must be imported after env has been defined
from portmod.repos import get_local_repos  # noqa: E402


def refresh_env():
    env.__init__()  # type: ignore
    env.REPOS = list(get_local_repos().values())


env.REPOS = list(get_local_repos().values())
