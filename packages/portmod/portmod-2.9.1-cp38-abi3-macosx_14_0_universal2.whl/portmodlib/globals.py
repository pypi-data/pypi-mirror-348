# Copyright 2019-2021 Portmod Authors
# Distributed under the terms of the GNU General Public License v3

import os
from typing import Optional

from .portmod import directories


def vdb_path() -> str:
    return os.path.join(root(), os.environ["VARIABLE_DATA"], "db")


def prefix_name() -> Optional[str]:
    return os.environ.get("PORTMOD_PREFIX_NAME")


def download_dir() -> str:
    return os.path.join(directories.cache_dir, "downloads")


def messages_dir() -> str:
    return os.environ["PORTMOD_MESSAGES_DIR"]


def warnings_dir() -> str:
    return os.environ["PORTMOD_WARNINGS_DIR"]


def root() -> str:
    return os.environ["PORTMOD_ROOT"]


def config_protect_dir() -> str:
    return os.environ["PORTMOD_CONFIG_PROTECT_DIR"]


def tmp_vdb() -> str:
    return os.environ["PORTMOD_TMP_VDB"]


def local_mods() -> str:
    return os.environ["PORTMOD_LOCAL_MODS"]
