# Copyright 2019-2021 Portmod Authors
# Distributed under the terms of the GNU General Public License v3

import os
from typing import Dict

from portmod.globals import env
from portmod.lock import exclusive_lock
from portmod.merge import merge
from portmod.query import SearchResult, query
from portmod.repo import get_repo
from portmodlib.colour import lblue
from portmodlib.l10n import l10n
from portmodlib.portmod import multi_select_prompt

from .merge import CLIMerge


def search_main(args):
    pkgs = list(
        query(
            " ".join(args.query),
            limit=0,
        )
    )

    if not pkgs:
        print(l10n("packages-found", num=len(pkgs)))
        return

    footnotes: Dict[str, str] = {}
    footnotenum = "a"

    def footnote(repo: str):
        nonlocal footnotenum
        if repo not in footnotes:
            footnotes[repo] = str(footnotenum)
            footnotenum = chr(ord(footnotenum) + 1)
        return lblue(f"[{footnotes[repo]}]")

    formatted = [SearchResult(package, footnote) for package in pkgs]
    footer_string = f"Select packages to install with space, then install them with Enter.{os.linesep}Typing filters the list; Escape to quit"
    if footnotes:
        footer_string += os.linesep + os.linesep.join(
            f"{footnote(repo)} {repo} {get_repo(repo).location}" for repo in footnotes
        )

    if env.INTERACTIVE:
        try:
            selection = multi_select_prompt(
                "Packages to install:", formatted, footer_string
            )
        except (EOFError, KeyboardInterrupt):
            return
        if selection:
            with exclusive_lock():
                merge([result.pkg.cpn for result in selection], io=CLIMerge())
    else:
        for pkg in formatted:
            print(pkg)
        print(footer_string)
        print(l10n("packages-found", num=len(formatted)))


def add_search_parser(subparsers, parents):
    parser = subparsers.add_parser("search", help=l10n("search-help"), parents=parents)

    parser.add_argument(
        "query",
        nargs="+",
        metavar=l10n("query-placeholder"),
        help=l10n("search-query-help"),
    )
    parser.set_defaults(func=search_main)
