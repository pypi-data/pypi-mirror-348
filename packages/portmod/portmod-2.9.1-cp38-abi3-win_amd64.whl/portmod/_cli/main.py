# Copyright 2019-2021 Portmod Authors
# Distributed under the terms of the GNU General Public License v3

import argparse
import logging
import os
import sys
import traceback
from logging import error
from typing import Optional, cast

from portmod.config import config_to_string, get_config
from portmod.config.sets import get_system
from portmod.download import RemoteHashError, SourceUnfetchable
from portmod.globals import env, get_version, refresh_env
from portmod.loader import SandboxedError, load_installed_pkg
from portmod.prefix import get_prefixes
from portmod.transactions import get_usestring
from portmodlib.atom import Atom
from portmodlib.l10n import l10n
from portmodlib.log import add_logging_arguments, init_logger

from .cfg_update import add_cfg_update_parser, add_module_update_parser
from .destroy import add_destroy_parser
from .error import InputException
from .init import add_init_parser
from .merge import add_merge_parser
from .mirror import add_mirror_parser
from .outdated import add_outdated_parser
from .query import add_query_parser
from .run import add_run_parser
from .search import add_search_parser
from .select import add_select_parser
from .sync import add_sync_parser
from .use import add_use_parser
from .validate import validate


def add_info_parser(subparsers, parents):
    def info(args):
        from git import Repo

        # Strip the user's home directory from paths and replace it with ~
        # This command is designed to produce information to be submitted with
        # bug reports, and the user's home directory is not a relevant piece of information.
        def strip_user(string: str) -> str:
            return string.replace(os.path.expanduser("~"), "~")

        print(f"Portmod {get_version()}")
        print(f"Python {sys.version}")
        print()

        print(l10n("info-repositories"))
        for repo in env.prefix().REPOS:
            gitrepo = Repo.init(repo.location)
            print("    ", "\n         ".join(strip_user(str(repo)).split(",")))
            try:
                print(
                    "    ",
                    l10n(
                        "info-repository-date",
                        date=gitrepo.head.commit.committed_datetime,
                    ),
                )
                print(
                    "    ", l10n("info-repository-commit", commit=gitrepo.head.commit)
                )
            except ValueError as error:
                print("    ", error)
            print()

        generator = (
            load_installed_pkg(atom)
            for atom in get_system() | set(map(Atom, get_config()["INFO_PACKAGES"]))
            if load_installed_pkg(atom)
        )
        packages = set(filter(None, generator))
        length = 0
        if len(packages) > 0:
            length = max(len(x.CPN) for x in packages)
        for pkg in sorted(packages, key=lambda x: x.CPN):
            # FIXME: Display date package was installed for live packages
            usestring = get_usestring(
                pkg, pkg.INSTALLED_USE, pkg.INSTALLED_USE, verbose=True
            )
            padding = length - len(str(pkg.CPN))
            print(pkg.CPN + ":", " " * padding, pkg.PVR, usestring)
        print()

        # Print config values
        config = get_config()
        if args.verbose:
            config_string = config_to_string(config)
        else:
            config_string = config_to_string(
                {
                    entry: config[entry]
                    for entry in config
                    if entry in config["INFO_VARS"]
                }
            )

        print(strip_user(config_string))
        # Print hardcoded portmod paths
        print(strip_user(f"TMP_DIR = {env.TMP_DIR}"))
        print(strip_user(f"CACHE_DIR = {env.CACHE_DIR}"))
        print(strip_user(f"CONFIG_DIR = {env.prefix().CONFIG_DIR}"))
        print(strip_user(f"ROOT = {env.prefix().ROOT}"))
        sys.exit(0)

    parser = subparsers.add_parser("info", help=l10n("info-help"), parents=parents)
    parser.set_defaults(func=info)


def get_generic_parser():
    """
    Produces a generic argument parser for use with the documentation generation.

    Does not include specific prefixes, or architectures
    """
    from tempfile import TemporaryDirectory

    from portmod.globals import env, refresh_env
    from portmod.prefix import add_prefix

    OLD = env.__dict__
    with TemporaryDirectory(prefix="portmod") as test_dir:
        try:
            env.CONFIG_DIR = os.path.join(test_dir, "config")
            env.CACHE_DIR = os.path.join(test_dir, "cache")
            env.DATA_DIR = os.path.join(test_dir, "local")
            env.INTERACTIVE = False

            refresh_env()
            add_prefix("<example>", "test")
            refresh_env()

            parser = get_parser("<example>", generic=True)

        finally:
            env.__dict__ = OLD

        return parser


def get_parser(
    subcommand: Optional[str] = None,
    prefix_subcommand: Optional[str] = None,
    generic=False,
):
    common = argparse.ArgumentParser(add_help=False)
    add_logging_arguments(common)
    common.add_argument("--debug", help=argparse.SUPPRESS, action="store_true")
    common.add_argument(
        "--no-confirm", help=l10n("no-confirm-help"), action="store_true"
    )

    parser = argparse.ArgumentParser(description=l10n("description"), parents=[common])
    group = parser.add_mutually_exclusive_group()
    group.add_argument("--version", help=l10n("version-help"), action="store_true")

    # For generic parser, don't repeat common arguments. While technically they
    # can be included everywhere, the docs blow up in size if they are listed
    # by each subcommand.
    parents = [] if generic else [common]

    subparsers = parser.add_subparsers(dest="subcommand_name")

    if (
        subcommand is None or subcommand in get_prefixes() and prefix_subcommand is None
    ) and not generic:
        prefix_parsers_list = []

        def get_help_func(parser):
            func = parser.print_help
            return lambda args: func()

        for prefix in get_prefixes():
            prefix_parser = subparsers.add_parser(
                prefix,
                help=l10n("prefix-help", prefix=prefix),
                description=l10n("prefix-help", prefix=prefix),
                parents=parents,
            )
            prefix_parsers_list.append(
                prefix_parser.add_subparsers(dest="prefix_subcommand_name")
            )
            prefix_parser.set_defaults(func=get_help_func(prefix_parser))

        for subparser in prefix_parsers_list:
            subparser.add_parser("merge", help=l10n("merge-help"), add_help=False)
            subparser.add_parser("search", help=l10n("search-help"), add_help=False)
            subparser.add_parser("select", help=l10n("select-help"), add_help=False)
            subparser.add_parser("query", help=l10n("query-help"), add_help=False)
            subparser.add_parser("use", help=l10n("use-help"), add_help=False)
            subparser.add_parser(
                "conflict-ui", help=l10n("conflict-ui-help"), add_help=False
            )
            subparser.add_parser("info", help=l10n("info-help"), add_help=False)
            subparser.add_parser("validate", help=l10n("validate-help"), add_help=False)
            subparser.add_parser("destroy", help=l10n("destroy-help"), add_help=False)
            subparser.add_parser("run", help=l10n("run-help"), add_help=False)
            subparser.add_parser(
                "cfg-update", help=l10n("cfg-update-help"), add_help=False
            )
            subparser.add_parser(
                "module-update", help=l10n("module-update-help"), add_help=False
            )
            subparser.add_parser("outdated", help=l10n("outdated-help"), add_help=False)
        subparsers.add_parser("mirror", help=l10n("mirror-help"), add_help=False)
    elif subcommand is not None and subcommand in get_prefixes() and not generic:
        prefix = subcommand

        prefix_parser = subparsers.add_parser(
            prefix, help=l10n("prefix-help", prefix=prefix), parents=parents
        )
        prefix_parsers = prefix_parser.add_subparsers(dest="prefix_subcommand_name")
        prefix_parser.set_defaults(func=lambda args: prefix_parser.print_help())
        if prefix_subcommand == "merge":
            add_merge_parser(prefix_parsers, parents)
        elif prefix_subcommand == "search":
            add_search_parser(prefix_parsers, parents)
        elif prefix_subcommand == "select":
            add_select_parser(prefix_parsers, parents)
        elif prefix_subcommand == "query":
            add_query_parser(prefix_parsers, parents)
        elif prefix_subcommand == "use":
            add_use_parser(prefix_parsers, parents)
        elif prefix_subcommand == "info":
            add_info_parser(prefix_parsers, parents)
        elif prefix_subcommand == "validate":
            prefix_parsers.add_parser(
                "validate", help=l10n("validate-help"), parents=parents
            ).set_defaults(func=validate)
        elif prefix_subcommand == "destroy":
            add_destroy_parser(prefix_parsers, parents)
        elif prefix_subcommand == "run":
            add_run_parser(prefix_parsers, parents)
        elif prefix_subcommand == "cfg-update":
            add_cfg_update_parser(prefix_parsers, parents)
        elif prefix_subcommand == "module-update":
            add_module_update_parser(prefix_parsers, parents)
        elif prefix_subcommand == "outdated":
            add_outdated_parser(prefix_parsers, parents)
    elif subcommand == "mirror":
        add_mirror_parser(subparsers, parents)
    elif subcommand is not None and subcommand in get_prefixes() and generic:
        prefix = subcommand
        # Add all the parsers. This is relatively slow, but necessary for sphinx-argparse
        prefix_parser = subparsers.add_parser(
            prefix, help=l10n("prefix-help", prefix=prefix), parents=parents
        )
        prefix_parsers = prefix_parser.add_subparsers(dest="prefix_subcommand_name")
        prefix_parser.set_defaults(func=lambda args: prefix_parser.print_help())
        add_merge_parser(prefix_parsers, parents)
        add_search_parser(prefix_parsers, parents)
        add_select_parser(prefix_parsers, parents)
        add_query_parser(prefix_parsers, parents)
        add_use_parser(prefix_parsers, parents)
        add_info_parser(prefix_parsers, parents)
        prefix_parsers.add_parser(
            "validate", help=l10n("validate-help"), parents=parents
        ).set_defaults(func=validate)
        add_destroy_parser(prefix_parsers, parents)
        add_run_parser(prefix_parsers, parents)
        add_cfg_update_parser(prefix_parsers, parents)
        add_module_update_parser(prefix_parsers, parents)

        add_mirror_parser(subparsers, parents)

    add_init_parser(subparsers, parents=parents)
    add_sync_parser(subparsers, parents=parents)
    return parser


def parse_args(
    subcommand: Optional[str] = None, prefix_subcommand: Optional[str] = None
):
    parser = get_parser(subcommand, prefix_subcommand)

    try:
        import argcomplete  # pylint: disable=import-error

        argcomplete.autocomplete(parser)
    except ModuleNotFoundError:
        pass

    if len(sys.argv) == 1:
        parser.print_help()
        sys.exit(2)

    if "--ignore-default-opts" in sys.argv:
        args = sys.argv[1:]
    else:
        args = sys.argv[1:] + os.environ.get("OMWMERGE_DEFAULT_OPTS", "").split()

    if subcommand is None:
        return parser, parser.parse_known_args(args)[0]
    else:
        return parser, parser.parse_args(args)


def main():
    os.environ["PYTHONUNBUFFERED"] = "1"

    _, args = parse_args()
    init_logger(args)

    if args.subcommand_name in get_prefixes():
        env.set_prefix(args.subcommand_name)

    # Ensure that we read config entries into os.environ
    get_config()

    refresh_env()

    prefix_subcommand_name = None
    if hasattr(args, "prefix_subcommand_name"):
        prefix_subcommand_name = cast(str, args.prefix_subcommand_name)
    parser, args = parse_args(args.subcommand_name, prefix_subcommand_name)

    if args.no_confirm:
        env.INTERACTIVE = False

    init_logger(args)

    if args.version:
        print(f"Portmod {get_version()}")
        sys.exit(0)

    if not args.subcommand_name and not args.version:
        error(l10n("invalid-cli-help"))
        parser.print_help()
        sys.exit(2)

    try:
        args.func(args)
    except (SandboxedError, InputException, SourceUnfetchable, RemoteHashError) as e:
        # Suppress traces for SandboxedErrors when not in debug mode
        if logging.root.level <= logging.DEBUG:
            traceback.print_exc()
        error("{}".format(e))
        sys.exit(1)
    except Exception as e:
        traceback.print_exc()
        error("{}".format(e))
        sys.exit(1)
