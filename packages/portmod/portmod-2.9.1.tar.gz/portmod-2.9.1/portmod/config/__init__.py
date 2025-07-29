# Copyright 2019-2021 Portmod Authors
# Distributed under the terms of the GNU General Public License v3
"""
Module that interacts with the various portmod config files

Files are stored both in the portmod local directory and in the profile directory tree,
with the user's config file overriding and extending defaults set by the profile
"""

import os
import sys
import warnings
from logging import error
from pathlib import Path
from subprocess import PIPE
from typing import Any, Dict, Optional

from portmod.config.profiles import profile_exists, profile_parents
from portmod.functools import prefix_aware_cache
from portmod.globals import env
from portmod.perms import Permissions
from portmod.win32 import get_personal
from portmodlib.version import Version

from .pyconf import (
    __COLLAPSE_KEYS,
    __OVERRIDE_KEYS,
    _create_config_placeholder,
    read_config,
)


# Note: this method should not be cached as otherwise it may be possible for a package
# to replace var with a symlink and then cause files to be written outside of the prefix
def variable_data_dir() -> str:
    """
    The directory in whch variable data is stored.

    I.e. all portmod information not installed by packages
    This is controlled with the VARIABLE_DATA profile variable and
    must be a path within the prefix ROOT.
    """
    # Resolve in case it includes symlinks outside of the prefix
    path = Path(env.prefix().ROOT, get_config_value("VARIABLE_DATA")).resolve()
    # is_relative_to is python3.9+
    # relative_to will raise a ValueError if the path is not relative to ROOT
    path.relative_to(env.prefix().ROOT)
    return str(path)


def get_config_value(key: str, default: Optional[Any] = None):
    """
    Parses the user's configuration, overriding defaults from their profile

    returns:
        The config value matching key, or default if it was not specified
    """
    return get_config().get(key, default)


def get_arch_version() -> Optional[str]:
    from portmod.execute import sandbox_execute

    script_path = os.path.join(env.prefix().ROOT, ".get_arch_version.py")
    if os.path.exists(script_path):
        # Note: output is piped, but not stderr.
        # This lets the script display information to the user via stderr
        # TODO: this needs to hook into the GUI somehow.
        # Maybe by redirecting stderr to logging?
        proc = sandbox_execute(
            [sys.executable, script_path],
            Permissions(global_read=True),
            profile=False,
            workdir=env.prefix().ROOT,
            stdout=PIPE,
        )
        out, _ = proc.communicate()
        if proc.returncode == 0:
            try:
                # Only return string if it's a valid version
                # Don't return a Version because the profile should only handle it as a string
                string = str(out.strip())
                Version(string, external=True)
                return string
            except ValueError as message:
                error(
                    f"Parsing the version of {env.prefix().ARCH} failed.{os.linesep} {message}"
                )
        else:
            error(
                f"Detection of the version of {env.prefix().ARCH} failed.{os.linesep}"
                f"The version will not be set, which may lead to unexpected behaviour"
            )
    return None


@prefix_aware_cache
def get_config() -> Dict[str, Any]:
    """
    Parses the user's configuration, overriding defaults from their profile
    """
    total_config: Dict[str, Any] = {
        # Default cannot be set in profile due to the value depending on platform
        "PLATFORM": sys.platform,
    }

    for attr in os.environ:
        total_config[attr] = os.environ[attr]

    if env.PREFIX_NAME is not None:
        total_config["ARCH_VERSION"] = get_arch_version()
        total_config["ARCH"] = env.prefix().ARCH
        total_config["ROOT"] = env.prefix().ROOT
        total_config["VARIABLE_DATA"] = "var"
        total_config["PROFILE_ONLY_VARIABLES"] = ["VARIABLE_DATA"]

    if sys.platform == "win32":
        total_config["PERSONAL"] = get_personal()

    if profile_exists():
        for parent in profile_parents():
            path = os.path.join(parent, "defaults.conf")
            if os.path.exists(path):
                total_config = read_config(path, total_config)

    if os.path.exists(env.GLOBAL_PORTMOD_CONFIG):
        total_config = read_config(env.GLOBAL_PORTMOD_CONFIG, total_config, user=True)

    if env.PREFIX_NAME:
        if os.path.exists(env.prefix().CONFIG):
            total_config = read_config(env.prefix().CONFIG, total_config, user=True)
        else:
            _create_config_placeholder()

    # Set defaults and add to os.environ (for use in portmodlib)
    for key in __OVERRIDE_KEYS:
        if not total_config.get(key):
            total_config[key] = ""
        elif isinstance(total_config[key], (str, bool)) and total_config[key]:
            os.environ[key] = str(total_config[key])

    for key in __COLLAPSE_KEYS:
        if not total_config.get(key):
            total_config[key] = set()
        elif isinstance(total_config[key], (str, bool)) and total_config[key]:
            os.environ[key] = str(total_config[key])

    # Note: VARIABLE_DATA needs to be set as an environment variable
    # so that we can access it both in the sandbox and outside with
    # a common interface
    for key in ["TMPDIR", "TEMP", "TMP", "VARIABLE_DATA"]:
        if total_config.get(key):
            os.environ[key] = total_config[key]

    return total_config


def config_to_string(config: Dict) -> str:
    """Prints the given dictionary config as a string"""
    lines = []
    for key in sorted(config):
        if isinstance(config[key], (list, set)):
            lines.append("{} = {}".format(key, " ".join(sorted(config[key]))))
        else:
            lines.append("{} = {}".format(key, config[key]))
    return "\n".join(lines)


def set_config_value(key: str, value: str, path: Optional[str] = None) -> Optional[str]:
    """
    Sets the given key-value pair in portmod.conf

    The previous value is returned, if any
    """
    with warnings.catch_warnings():
        warnings.filterwarnings("ignore")
        from redbaron import RedBaron
        from redbaron.nodes import AssignmentNode, NameNode

    if not path:
        path = env.prefix().CONFIG

    old = None
    string = '"' + value + '"'
    new_line = f"{key} = {string}"
    if os.path.exists(path):
        with open(path, "r") as file:
            node = RedBaron(file.read())

            for elem in node:
                if (
                    isinstance(elem, AssignmentNode)
                    and isinstance(elem.target, NameNode)
                    and elem.target.value == key
                ):
                    old = elem.value
                    elem.value = string

            if not old and node:
                node.append(new_line)
            elif not node:
                node = RedBaron(new_line)

            with open(path, "w") as file:
                file.write(node.dumps())
    else:
        with open(path, "w") as file:
            file.write(new_line)

    get_config.cache_clear()
    return old
