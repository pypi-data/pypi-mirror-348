# Copyright 2019-2021 Portmod Authors
# Distributed under the terms of the GNU General Public License v3

"""
Various utility functions
"""

from __future__ import annotations

from typing import TYPE_CHECKING, Any, Iterable, List, NamedTuple, Optional, Tuple

from portmod.config.license import has_eula, is_license_accepted
from portmod.repo.keywords import (
    Keyword,
    NamedKeyword,
    Stability,
    WildcardKeyword,
    get_stability,
)
from portmodlib.atom import QualifiedAtom

from .globals import env
from .pybuild import Pybuild

if TYPE_CHECKING:
    from portmod.query import FlagDesc


class UseDep(NamedTuple):
    atom: QualifiedAtom
    flag: str
    description: Optional[FlagDesc]
    oldvalue: Optional[str]
    comment: Tuple[str, ...]

    def __repr__(self):
        if self.oldvalue:
            return f"UseDep({self.atom}, {self.oldvalue} -> {self.flag})"
        else:
            return f"UseDep({self.atom}, {self.flag})"


def is_keyword_masked(arch: str, keywords: Iterable[str]):
    return "-" + arch in keywords or (
        "-*" in keywords and arch not in keywords and "~" + arch not in keywords
    )


class KeywordDep(NamedTuple):
    """A requirement that a keyword be accepted before the package can be installed"""

    atom: QualifiedAtom
    keyword: Keyword
    masked: bool
    # Keyword which made this dependency necessary
    masking_keyword: Optional[Keyword] = None


class LicenseDep(NamedTuple):
    """A requirement that a license be accepted before the package can be installed"""

    atom: QualifiedAtom
    license: str
    is_eula: bool
    repo: str


def select_package(packages: Iterable[Pybuild]) -> Tuple[Pybuild, Any]:
    """
    Chooses a mod version based on keywords and accepts it if the license is accepted
    """
    if not packages:
        raise Exception("Cannot select mod from empty modlist")

    stable = []
    testing = []
    untested = []
    masked = []

    for package in packages:
        stability, masking_keyword = get_stability(package)
        if stability == Stability.STABLE:
            stable.append((package, masking_keyword))
        elif stability == Stability.TESTING:
            testing.append((package, masking_keyword))
        elif stability == Stability.MASKED:
            masked.append((package, masking_keyword))
        elif stability is Stability.UNTESTED:
            untested.append((package, masking_keyword))

    is_masked = False
    keyword: Optional[Keyword] = None
    masking_keyword = None

    if stable:
        package, _ = max(stable, key=lambda pkg: pkg[0].version)
    elif testing:
        # No packages were accepted. Choose the best version and add the keyword
        # as a requirement for it to be installed
        package, _ = max(testing, key=lambda pkg: pkg[0].version)
        keyword = NamedKeyword(env.prefix().ARCH, Stability.TESTING, None)
    elif untested:
        package, _ = max(untested, key=lambda pkg: pkg[0].version)
        keyword = WildcardKeyword.ALWAYS
    elif masked:
        package, masking_keyword = max(masked, key=lambda pkg: pkg[0].version)
        keyword = WildcardKeyword.ALWAYS
        is_masked = True

    deps: List[Any] = []
    if not is_license_accepted(package, package.get_use()):
        deps.append(
            LicenseDep(package.CPN, package.LICENSE, has_eula(package), package.REPO)
        )
    if keyword is not None:
        deps.append(
            KeywordDep(
                QualifiedAtom("=" + package.ATOM.CPF),
                keyword,
                is_masked,
                masking_keyword,
            )
        )

    return (package, deps or None)
