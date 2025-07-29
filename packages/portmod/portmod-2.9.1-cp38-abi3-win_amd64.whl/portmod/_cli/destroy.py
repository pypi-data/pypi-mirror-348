# Copyright 2019-2021 Portmod Authors
# Distributed under the terms of the GNU General Public License v3

import os
import shutil
from logging import info, warning
from typing import List

from portmod.config import variable_data_dir
from portmod.config.sets import get_set
from portmod.globals import env
from portmod.loader import load_installed_pkg
from portmod.package import remove_pkg
from portmod.prefix import remove_prefix
from portmod.prompt import multi_select_prompt, prompt_bool
from portmodlib.fs import get_tree_size, onerror
from portmodlib.l10n import l10n

from .merge import CLIRemove


class Directory:
    path: str

    def __init__(self, path: str):
        self.path = path

    def __str__(self) -> str:
        return self.path + " (" + l10n("size", size=self.get_size()) + ")"

    def get_size(self):
        return get_tree_size(self.path) / 1024**2

    def remove(self):
        shutil.rmtree(self.path, onerror=onerror)


def destroy(args):
    assert env.PREFIX_NAME
    to_remove: List[Directory] = []

    if args.remove_config and os.path.lexists(env.prefix().CONFIG_DIR):
        to_remove.append(Directory(env.prefix().CONFIG_DIR))

    if env.INTERACTIVE:
        if to_remove:
            print(l10n("destroy-directories"))

            try:
                skip = multi_select_prompt(l10n("destroy-exclude-prompt"), to_remove)
            except (EOFError, KeyboardInterrupt):
                return

            for dir in skip:
                to_remove.remove(dir)
        else:
            print(l10n("no-directories-to-remove"))

        if not args.preserve_root:
            print(l10n("destroy-preserve-original", path=env.prefix().ROOT))

        print()
        if not prompt_bool(l10n("destroy-prompt", prefix=env.PREFIX_NAME)):
            return

    for dir in to_remove:
        print(l10n("removing-directory", path=dir.path))
        dir.remove()

    if not args.preserve_root:
        # Remove files installed by portmod
        # This only occurs for prefixes which were installed into an existing directory
        for atom in get_set("installed"):
            pkg = load_installed_pkg(atom)
            if pkg:
                remove_pkg(pkg, io=CLIRemove(pkg.ATOM))
            else:
                # This should not occur
                warning(f"Unable to load installed package {atom} during destruction")
        variable_data = variable_data_dir()
        info(l10n("removing-directory", path=variable_data))
        shutil.rmtree(variable_data, onerror=onerror)

    remove_prefix(env.PREFIX_NAME)


def add_destroy_parser(subparsers, parents):
    parser = subparsers.add_parser(
        "destroy", help=l10n("destroy-help"), parents=parents
    )
    parser.add_argument(
        "--preserve-root",
        help=l10n("destroy-preserve-root-help"),
        action="store_true",
    )
    parser.add_argument(
        "--remove-config",
        help=l10n("destroy-remove-config-help"),
        action="store_true",
    )
    parser.set_defaults(func=destroy)
