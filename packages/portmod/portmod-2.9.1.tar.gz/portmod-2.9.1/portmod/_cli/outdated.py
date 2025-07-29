# Copyright 2019-2021 Portmod Authors
# Distributed under the terms of the GNU General Public License v3

import logging
import sys
from itertools import repeat
from multiprocessing import Pool
from typing import List, Sequence

from portmod._deps import DepError, resolve
from portmod.config.sets import is_selected
from portmod.loader import load_all_installed, load_pkg
from portmod.transactions import Transactions
from portmod.util import select_package
from portmodlib.atom import FQAtom
from portmodlib.colour import bright, green, lblue
from portmodlib.l10n import l10n


def tabulate(
    header: Sequence[str],
    rows: Sequence[Sequence[str]],
    lengths: Sequence[Sequence[int]],
):
    assert rows, "Rows must be nonempty!"
    print()
    cols = len(header)
    gap = 4
    # Add one space between each column
    maxlengths = [max(row[col] + gap for row in lengths) for col in range(cols)]

    for col in range(cols):
        print(header[col] + " " * (maxlengths[col] - len(header[col])), end="")
    print()
    # Dividing line is the width of each column, minus the gap since the width of each column
    # includes an extra gap at the end
    print("—" * (sum(maxlengths) - gap))

    for index, row in enumerate(rows):
        for col in range(cols):
            print(row[col] + " " * (maxlengths[col] - lengths[index][col]), end="")
        print()
    print()


def is_outdated(pkg, world_update: List[FQAtom], ignore_keywords: bool):
    pkgs = load_pkg(pkg.CPN)
    if not pkgs:
        # Package is installed but not available in the repos
        return (pkg, "None", l10n("outdated-not-available"))
    if ignore_keywords:
        newest = max(pkgs, key=lambda x: x.version)
    else:
        newest, keywords = select_package(pkgs)
    if newest.version > pkg.version:
        if any(atom == newest.ATOM for atom in world_update):
            updateable = l10n("outdated-world-update")
        else:
            try:
                transactions = resolve([newest.ATOM], [], {newest.ATOM}, set(), set())
                if any(
                    transaction.pkg.ATOM == newest.ATOM
                    for transaction in transactions.pkgs
                ):
                    updateable = l10n("outdated-manual-update")
                else:
                    updateable = l10n("outdated-manual-update-impossible")
            except DepError:
                updateable = l10n("unable-to-satisfy-dependencies")
        return (pkg, str(newest.version), updateable)
    return None


def outdated(args):
    """Displays outdated packages"""

    # Suppress logger to avoid dependency calculation messages
    logger = logging.getLogger()
    logger.disabled = True
    try:
        world_update = resolve(
            [], [], set(), set(), set("world"), deep=True, update=True
        )
    except DepError:
        world_update = Transactions()

    # Multiprocessing only works if we can fork (default on Linux),
    # as otherwise the other processes don't inherit the correct prefix information
    # Forking is unstable on macos and not supported on Windows
    # Unfortunately, this can be somewhat slow on macos/Windows as a result
    if sys.platform == "linux":
        with Pool() as pool:
            outdated = [
                x
                for x in pool.starmap(
                    is_outdated,
                    zip(
                        [
                            pkg
                            for pkg in load_all_installed()
                            if "local" not in pkg.PROPERTIES
                        ],
                        repeat(
                            [transaction.pkg.ATOM for transaction in world_update.pkgs]
                        ),
                        repeat(args.ignore_keywords),
                    ),
                )
                if x is not None
            ]
    else:
        outdated = []
        world_pkgs = [transaction.pkg.ATOM for transaction in world_update.pkgs]
        for pkg in load_all_installed():
            if "local" not in pkg.PROPERTIES:
                result = is_outdated(pkg, world_pkgs, args.ignore_keywords)
                if result is not None:
                    outdated.append(result)

    if not outdated:
        print(l10n("outdated-up-to-date"))
        return

    longest = 0
    for installed, _, _ in outdated:
        length = len(installed.PN)
        if length > longest:
            longest = length

    strings = []
    lengths = []
    for installed, newest, updateable in outdated:
        lengths.append(
            (len(installed.CPN), len(installed.PVR), len(newest), len(updateable))
        )
        if is_selected(installed.ATOM):
            strings.append(
                (
                    bright(green(installed.CPN)),
                    lblue(installed.version),
                    lblue(newest),
                    updateable,
                )
            )
        else:
            strings.append(
                (
                    green(installed.CPN),
                    lblue(installed.version),
                    lblue(newest),
                    updateable,
                )
            )
    tabulate(
        (
            l10n("outdated-heading-package"),
            l10n("outdated-heading-installed"),
            l10n("outdated-heading-available"),
            l10n("outdated-heading-update-status"),
        ),
        strings,
        lengths,
    )
    logger.disabled = False


def add_outdated_parser(subparsers, parents):
    parser = subparsers.add_parser(
        "outdated", help=l10n("outdated-help"), parents=parents
    )
    parser.add_argument(
        "--ignore-keywords", action="store_true", help=l10n("outdated-ignore-keywords")
    )
    parser.set_defaults(func=outdated)
