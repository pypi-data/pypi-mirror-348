# Copyright 2019-2021 Portmod Authors
# Distributed under the terms of the GNU General Public License v3

"""
Quality assurance for the mod repo
"""

import argparse
import glob
import os
import re
import sys
import traceback
from itertools import combinations
from logging import debug, error
from typing import Callable

from portmod.config.use import add_use, remove_use
from portmod.download import (
    RemoteHashError,
    SourceUnfetchable,
    download_source,
    fetchable,
)
from portmod.globals import env
from portmod.loader import load_file
from portmod.merge import merge
from portmod.news import validate_news
from portmod.pybuild import Pybuild, ValidationError
from portmod.query import get_flag_string
from portmod.repo import LocalRepo, get_repo, get_repo_name, get_repo_root, has_repo
from portmod.repo.loader import _iterate_pybuilds, get_atom_from_path, is_package
from portmod.repo.metadata import (
    get_categories,
    get_use_flag_atom_aliases,
    license_exists,
)
from portmodlib.atom import Atom, InvalidAtom, UnqualifiedAtom
from portmodlib.colour import green
from portmodlib.l10n import l10n
from portmodlib.log import add_logging_arguments, init_logger
from portmodlib.parsers.list import read_list
from portmodlib.portmod import (
    parse_category_metadata,
    parse_groups,
    parse_yaml_dict,
    parse_yaml_dict_dict,
)
from portmodlib.usestr import check_required_use

from .merge import CLIMerge
from .pybuild import pybuild_manifest, pybuild_validate


def scan_package_dir(path: str, err: Callable[[str], None]):
    root = os.path.dirname(os.path.dirname(path))
    cpn = os.path.join(os.path.basename(os.path.dirname(path)), os.path.basename(path))
    if Atom(os.path.basename(cpn)).version is not None:
        err(f"Package name {cpn} must not end in a version")

    for file in _iterate_pybuilds(path):
        # iterate_pybuilds may sometimes produce files which aren't package files
        if not is_package(file):
            continue
        relative_path = os.path.relpath(file, start=root)
        debug(f"Scanning {relative_path}")
        dir_name = os.path.basename(path)
        file_name = Atom(os.path.splitext(os.path.basename(file))[0]).PN
        if dir_name != file_name:
            err(
                f"The package name in filename {relative_path} should match its parent directory's name!"
            )

        try:
            pybuild_validate(file)
        except ValidationError as e:
            err(f"Validation failed for file {green(relative_path)}: {e}")
        except Exception as e:
            traceback.print_exc()
            err(f"Error validating file {green(relative_path)}: {e}")


def scan_category_metadata(path: str, err: Callable[[str], None]):
    # Note: Package metadata is already validated as part of pybuild_validate
    try:
        parse_category_metadata(path)
    except Exception as e:
        traceback.print_exc()
        err("{}".format(e))


def scan_category(path: str, err: Callable[[str], None]):
    for directory in glob.glob(os.path.join(path, "*")):
        if os.path.isdir(directory) and any(
            is_package(os.path.join(directory, file)) for file in os.listdir(directory)
        ):
            scan_package_dir(directory, err)
    metadata_path = os.path.join(path, "metadata.yaml")
    if os.path.exists(metadata_path):
        scan_category_metadata(metadata_path, err)


def scan_arch_list(repo_root: str, err: Callable[[str], None]):
    # Check profiles/arch.list
    path = os.path.join(repo_root, "profiles", "arch.list")
    if os.path.exists(path):
        archs = read_list(path)
        for arch in archs:
            if " " in arch:
                err(
                    f'arch.list: in entry "{arch}". '
                    "Architectures cannot contain spaces"
                )


def scan_categories(repo_root: str, err: Callable[[str], None]):
    # Check profiles/categories
    path = os.path.join(repo_root, "profiles", "categories")
    if os.path.exists(path):
        lines = read_list(path)
        for category in lines:
            if " " in category:
                err(
                    f'categories.list: in category "{category}". '
                    "Categories cannot contain spaces"
                )


def scan_groups(repo_root: str, err: Callable[[str], None]):
    # Check metadata/groups.yaml
    path = os.path.join(repo_root, "metadata", "groups.yaml")
    if os.path.exists(path):
        parse_groups(path)


def scan_license_groups(repo_root: str, err: Callable[[str], None]):
    # Check metadata/license_groups.yaml
    # All licenses should exist in licenses/LICENSE_NAME
    path = os.path.join(repo_root, "profiles", "license_groups.yaml")
    if os.path.exists(path):
        license_groups = parse_yaml_dict(path)
        for key, value in license_groups.items():
            if value is not None:
                for license in value.split():
                    if not license_exists(repo_root, license) and not (
                        license.startswith("@")
                    ):
                        err(
                            f'license_groups.yaml: License "{license}" in group {key} '
                            "does not exist in licenses directory"
                        )


def scan_repo_name(repo_root: str, err: Callable[[str], None]):
    # Check profiles/repo_name
    path = os.path.join(repo_root, "profiles", "repo_name")
    if os.path.exists(path):
        lines = read_list(path)
        if len(lines) == 0:
            err("repo_name: profiles/repo_name cannot be empty")
        elif len(lines) > 1:
            err(
                "repo_name: Extra lines detected. "
                "File must contain just the repo name."
            )
        elif " " in lines[0]:
            err("repo_name: Repo name must not contain spaces.")


def scan_use(repo_root: str, err: Callable[[str], None]):
    # Check profiles/use.yaml
    path = os.path.join(repo_root, "profiles", "use.yaml")
    if os.path.exists(path):
        flags = parse_yaml_dict(path)
        for desc in flags.values():
            if not isinstance(desc, str):
                err(f'use.yaml: Description "{desc}" is not a string')


def scan_profiles(repo_root: str, err: Callable[[str], None]):
    # Check profiles/profiles.yaml
    path = os.path.join(repo_root, "profiles", "profiles.yaml")
    archs_path = os.path.join(repo_root, "profiles", "arch.list")
    archs = []
    if os.path.exists(archs_path):
        archs = read_list(archs_path)
    if os.path.exists(path):
        keywords = parse_yaml_dict_dict(path)
        for keyword, profiles in keywords.items():
            if keyword not in archs:
                err(
                    f"profiles.yaml: keyword {keyword} " "was not declared in arch.list"
                )
            for profile in profiles:
                if not isinstance(profile, str):
                    err('profiles.yaml: Profile "{profile}" is not a string')
                path = os.path.join(repo_root, "profiles", profile)
                if not os.path.exists(path):
                    err(f"profiles.yaml: Profile {path} does not exist")


def scan_use_expand(filename: str, err: Callable[[str], None]):
    entries = parse_yaml_dict(filename)
    for entry in dict(entries):
        if not re.match("[A-Za-z0-9][A-Za-z0-9+_-]*", entry):
            err(f"USE_EXPAND flag {entry} in {filename} contains invalid characters")


def scan_root(repo_root: str, err: Callable[[str], None]):
    # Run pybuild validate on every pybuild in repo
    for category in get_categories(repo_root):
        scan_category(os.path.join(repo_root, category), err)

    # Check files in metadata and profiles.
    # These may not exist, as they might be inherited from another repo instead
    scan_arch_list(repo_root, err)
    scan_categories(repo_root, err)
    scan_groups(repo_root, err)
    scan_license_groups(repo_root, err)
    scan_repo_name(repo_root, err)
    scan_use(repo_root, err)
    scan_profiles(repo_root, err)
    for filename in glob.glob(os.path.join(repo_root, "profiles", "desc", "*.yaml")):
        scan_use_expand(filename, err)
    # Check news
    validate_news(repo_root, err)
    scan_use_alias(repo_root, err)


def scan_use_alias(repo_root: str, err: Callable[[str], None]):
    # Check profiles/use.alias.yaml
    try:
        aliases = get_use_flag_atom_aliases(repo_root)
    except (RuntimeError, UnqualifiedAtom, InvalidAtom) as _e:
        err(str(_e))
    for flag, alias in aliases.items():
        # Check that alias is a valid package in the repository
        packages = _iterate_pybuilds(os.path.join(repo_root, alias.C, alias.PN))
        if not packages:
            err(
                f"Use flag alias package {alias} for flag {flag} "
                f"does not exist in this repository"
            )

        # If alias has a use flag requirement, it must be a valid use flag for at least
        # one version of that package
        if alias.USE:
            if not any(
                alias.USE <= set(load_file(package).IUSE_EFFECTIVE)
                for package in packages
            ):
                err(
                    "No package has the required use flag dependencies "
                    f"for use flag {flag}'s alias {alias}"
                )


def scan_file(filename: str, repo_root: str, err: Callable[[str], None]):
    absolute = os.path.abspath(filename)
    relative = os.path.normpath(os.path.relpath(absolute, start=repo_root))
    if is_package(filename):
        scan_package_dir(os.path.dirname(absolute), err)
    else:
        news_dir = os.path.join("metadata", "news")
        if relative == os.path.join("profiles", "arch.list"):
            scan_arch_list(repo_root, err)
        elif relative == os.path.join("profiles", "categories"):
            scan_categories(repo_root, err)
        elif relative == os.path.join("metadata", "groups.yaml"):
            scan_groups(repo_root, err)
        elif relative == os.path.join("profiles", "license_groups.yaml"):
            scan_license_groups(repo_root, err)
        elif relative == os.path.join("profiles", "repo_name"):
            scan_repo_name(repo_root, err)
        elif relative == os.path.join("profiles", "use.yaml"):
            scan_use(repo_root, err)
        elif relative == os.path.join("profiles", "use.alias.yaml"):
            scan_use_alias(repo_root, err)
        elif os.path.dirname(relative) == os.path.join(
            "profiles", "desc"
        ) and relative.endswith(".yaml"):
            scan_use_expand(filename, err)
        elif os.path.commonprefix([relative, news_dir]) == news_dir:
            validate_news(repo_root, err)
        elif os.path.basename(filename) == "metadata.yaml":
            path, _ = os.path.split(relative)
            if os.path.split(path)[0] is None:
                scan_category_metadata(filename, err)
            else:
                scan_package_dir(os.path.dirname(absolute), err)


def scan_commit(commit, err):
    import git

    _git = git.Git()

    files = _git.show(commit, name_only=True, oneline=True).splitlines()[1:]
    message = _git.log(commit, format="%B", n=1)
    if message:
        header_line = message.splitlines()[0]
        packages_modified = [file for file in files if is_package(file)]
        if len(packages_modified) == 1:
            atom = get_atom_from_path(packages_modified[0]).CPN
            if not message.startswith(atom + ":"):
                err(f'Commit "{header_line}" should start with "{atom}: <short desc>"')
    else:
        err(f"Message for commit {commit} should not be empty!")


def commit_message(args, repo_root: str, _err: Callable[[str], None]):
    import git

    gitrepo = git.Repo.init(repo_root)

    initial_message = None
    message = ""
    if args.initial_message:
        with open(args.initial_message, encoding="utf-8") as file:
            initial_message = file.read()

    changes = gitrepo.head.commit.diff(git.Diffable.Index)

    pybuild_diffs = [
        diff for diff in changes if diff.b_path and is_package(diff.b_path)
    ]

    def check_initial_message(message, initial_message):
        return (
            initial_message
            and initial_message.strip() != message
            and not initial_message.startswith("fixup!")
        )

    if len(pybuild_diffs) == 1:
        diff = pybuild_diffs[0]

        if diff.a_path and is_package(diff.a_path):
            new = None
            old = get_atom_from_path(diff.a_path)
            if diff.b_path:
                new = get_atom_from_path(diff.b_path)

            if diff.deleted_file:
                message = f"{old.CPN}: Removed version {old.version}"
                if check_initial_message(message, initial_message):
                    message += f"\n\n{initial_message}"
            elif diff.new_file:
                assert new
                message = f"{new.CPN}: Added version {new.version}"
                if check_initial_message(message, initial_message):
                    message += f"\n\n{initial_message}"
            elif diff.renamed_file and new is not None and old.version != new.version:
                message = f"{new.CPN}: Updated to version {new.version}"
                if check_initial_message(message, initial_message):
                    message += f"\n\n{initial_message}"
            else:
                assert new, "Only deleted files should lack a destination path"
                # Either a change to the package without bump, or just a revision bump.
                # We can't autogenerate a meaningful message
                if initial_message:
                    if initial_message.startswith(
                        new.CPN + ":"
                    ) or initial_message.startswith("fixup!"):
                        message = initial_message
                    else:
                        message = f"{new.CPN}: {initial_message}"
                else:
                    message = f"{new.CPN}: "

        if args.initial_message:
            with open(args.initial_message, "w", encoding="utf-8") as file:
                file.write(message)
        else:
            print(message)


def scan_sources(file: str, err: Callable[[str], None]):
    pkg = load_file(file)
    debug(f"Scanning sources for file {file}")

    for source in fetchable(pkg, matchall=True):
        try:
            download_source(pkg, source, check_remote=True)
        except (SourceUnfetchable, RemoteHashError) as e:
            err(f"In file {file}: {e}")


def scan_path(path: str, repo_root: str, err: Callable[[str], None]):
    if os.path.exists(os.path.join(path, "profiles", "repo_name")):
        scan_root(path, err)
    elif os.path.isdir(path):
        if next(_iterate_pybuilds(os.path.join(path, "*")), None) is not None:
            scan_category(path, err)
        elif next(_iterate_pybuilds(path), None) is not None:
            scan_package_dir(path, err)
        else:
            # Try to scan all files in directory tree
            for path_root, _, filenames in os.walk(path):
                for filename in filenames:
                    scan_file(os.path.join(path_root, filename), repo_root, err)
    elif os.path.isfile(path):
        scan_file(os.path.abspath(path), repo_root, err)


def scan(args, repo_root: str, err: Callable[[str], None]):
    if args.diff:
        import git

        for file in git.Git().diff(args.diff, name_only=True).splitlines():
            scan_file(os.path.join(repo_root, file), repo_root, err)
            if is_package(file) and os.path.exists(file):
                scan_sources(file, err)

        if os.getenv("INQUISITOR_SCAN_COMMIT_MESSAGE"):
            for commit in (
                git.Git().log("HEAD", "^" + args.diff, pretty="%H").splitlines()
            ):
                scan_commit(commit, err)

    else:
        for root in args.paths or [os.getcwd()]:
            scan_path(root, repo_root, err)


def manifest(args, _repo_root: str, err: Callable[[str], None]):
    def try_manifest(file: str):
        try:
            pybuild_manifest(file)
        except Exception as e:
            traceback.print_exc()
            err(f"{e}")

    for root in args.paths or [os.getcwd()]:
        root = os.path.abspath(root)
        if os.path.isdir(root):
            # Run pybuild manifest on every pybuild in repo
            for file in _iterate_pybuilds(os.path.join(root, "**"), recursive=True):
                try_manifest(file)
        else:
            if is_package(root):
                try_manifest(root)
            else:
                err(
                    f"{root} is not a valid package file! "
                    "Package files must begin with the name of their parent directory, "
                    "followed by a hyphen and a valid version, and ending in either .pybuild or .yaml"
                )


def test_install(package: Pybuild):
    try:
        all_combinations = set()
        for i in range(len(package.IUSE_EFFECTIVE) + 1):
            all_combinations |= set(combinations(package.IUSE_EFFECTIVE, i))
        configurations = list(
            filter(
                lambda flags: check_required_use(
                    package.REQUIRED_USE_EFFECTIVE, set(flags), package.valid_use
                ),
                all_combinations,
            )
        )
        for configuration in configurations:
            print(
                "Testing configuration",
                get_flag_string(
                    "USE",
                    configuration,
                    set(package.IUSE_EFFECTIVE) - set(configuration),
                ),
            )
            for flag in package.IUSE_EFFECTIVE:
                if flag in configuration:
                    add_use(flag, package.ATOM)
                else:
                    add_use(flag, package.ATOM, disable=True)
            merge([package.ATOM], select=False, io=CLIMerge())

    finally:
        for flag in package.IUSE_EFFECTIVE:
            remove_use(flag, package.ATOM)


def test_install_cli(args, repo_root, _err):
    from types import SimpleNamespace

    from portmod._cli.select import add_prefix_repo, list_profiles
    from portmod.config.profiles import set_profile
    from portmod.functools import clear_system_cache
    from portmod.loader import load_file
    from portmod.prefix import add_prefix, get_prefixes

    from .destroy import destroy

    # Enable special testing behaviour like auto-applying configuration changes
    env.TESTING = True

    if args.no_confirm:
        env.INTERACTIVE = False

    try:
        prefixes = get_prefixes()
        if args.prefix not in prefixes:
            test_prefix = "test0"
            i = 0
            while test_prefix in prefixes:
                i += 1
                test_prefix = "test" + str(i)

            add_prefix(test_prefix, args.arch)
            # FIXME: Should all profiles be tested?
            # we can only feasibly do it if creating a prefix from scratch.
            # If using an existing prefix, we should just use the existing profile

            repo_name = get_repo_name(repo_root)
            if not has_repo(repo_name) or get_repo(repo_name).location != repo_root:
                env.REPOS.insert(0, LocalRepo(repo_name, repo_root))
                clear_system_cache()
            env.set_prefix(test_prefix)
            add_prefix_repo(repo_name)
            profiles = list_profiles(args.arch)
            print(f"Using profile {profiles[0]}")
            set_profile(profiles[0])
            clear_system_cache()
        elif args.prefix is not None:
            if not prefixes[args.prefix].arch == args.arch:
                raise Exception(
                    f"Architecture of prefix {args.prefix} does not match the test architecture"
                )
            test_prefix = args.prefix
            env.set_prefix(test_prefix)

        for file in args.files:
            test_install(load_file(file))

    finally:
        # Make sure destruction is done in non-interactive mode
        # User didn't create the test prefix, so they don't care about preserving
        # configuration
        env.INTERACTIVE = False
        if args.prefix is None and not env.DEBUG:
            destroy(SimpleNamespace(remove_config=True, preserve_root=False))


def get_doc_parser():
    return get_parser(True)


def get_parser(doc=False):
    common = argparse.ArgumentParser(add_help=False)
    add_logging_arguments(common)
    common.add_argument("--debug", help=l10n("merge-debug-help"), action="store_true")

    parser = argparse.ArgumentParser(
        description="Quality assurance program for the package repository",
        parents=[common],
    )

    parents = [] if doc else [common]

    subparsers = parser.add_subparsers()
    manifest_parser = subparsers.add_parser(
        "manifest", help="Produces Manifest files", parents=parents
    )
    scan_parser = subparsers.add_parser(
        "scan", help="QA Checks package repositories", parents=parents
    )
    commit_msg_parser = subparsers.add_parser(
        "commit-msg",
        help="Produces a commit message using the working directory. "
        "Designed to be used as a git commit-msg hook",
        parents=parents,
    )
    commit_msg_parser.add_argument(
        "initial_message",
        help="Path to a file containing a user-supplied message to start from",
        nargs="?",
    )
    commit_msg_parser.add_argument(
        "--paths",
        help="Location of the repository to process. "
        "If omitted, the current working directory will be used",
        nargs="?",
    )
    scan_parser.add_argument(
        "--diff",
        nargs="?",
        help="Scan files changed since the given git target (branch, commit, etc.)",
    )
    manifest_parser.add_argument(
        "paths",
        metavar="PATH",
        help="scope to process. If not provided defaults to the current working directory",
        nargs="*",
    )
    scan_parser.add_argument(
        "paths",
        metavar="PATH",
        help="scope to process. If not provided defaults to the current working directory",
        nargs="*",
    )
    test_install_parser = subparsers.add_parser(
        "test-install", help="Tests package installation", parents=parents
    )
    test_install_parser.add_argument("arch", help="Architecture to test")
    test_install_parser.add_argument(
        "files", metavar="FILE", help="Package files to test", nargs="*"
    )
    test_install_parser.add_argument("--prefix", help="Optional existing prefix to use")
    test_install_parser.add_argument(
        "--no-confirm", help="If set, run in non-interactive mode", action="store_true"
    )

    scan_parser.set_defaults(func=scan)
    manifest_parser.set_defaults(func=manifest)
    commit_msg_parser.set_defaults(func=commit_message)
    test_install_parser.set_defaults(func=test_install_cli)

    return parser


def main():
    """
    Main function for the inquisitor executable
    """

    parser = get_parser()

    args = parser.parse_args()
    init_logger(args)

    if hasattr(args, "paths") and args.paths:
        repo_root = get_repo_root(args.paths[0])
    else:
        repo_root = get_repo_root(os.getcwd())

    has_errored = False
    env.STRICT = True

    def err(string: str):
        nonlocal has_errored
        error(string)
        has_errored = True

    if repo_root is None:
        err(
            "Cannot find repository for the current directory. "
            "Please run from within the repository you wish to inspect"
        )
        sys.exit(1)

    # Register repo in case it's not already in repos.cfg
    real_root = os.path.realpath(repo_root)
    if not any([real_root == os.path.realpath(repo.location) for repo in env.REPOS]):
        sys.path.insert(0, os.path.join(repo_root))
        env.REPOS.insert(0, LocalRepo(get_repo_name(repo_root), repo_root))

    if args.debug:
        env.DEBUG = True

    if len(sys.argv) == 1:
        parser.print_help()
        sys.exit(2)

    args.func(args, repo_root, err)

    if has_errored:
        sys.exit(1)
