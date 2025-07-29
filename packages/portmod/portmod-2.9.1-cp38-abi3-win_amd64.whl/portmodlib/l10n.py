# Copyright 2019-2021 Portmod Authors
# Distributed under the terms of the GNU General Public License v3

"""Module with localization helpers"""

import locale
import os
import sys
from functools import lru_cache
from typing import List

from portmodlib.portmod import l10n_lookup

# Only used in debug builds of the rust library
_DEBUG_L10N_DIR = os.path.join(os.path.dirname(os.path.dirname(__file__)), "l10n")

WIN32_LOOKUP_TABLE = {
    "English_United States": "en_US",
}


@lru_cache()
def _default_locale():
    """Returns the default locale"""
    try:
        locale.setlocale(locale.LC_ALL, "")
        lang, _ = locale.getlocale()
        if lang is None:
            return "en_GB"
        if sys.platform == "win32":
            return WIN32_LOOKUP_TABLE.get(lang, lang)

        return str(lang)
    except locale.Error:
        # If default fails, fall back to the C locale, which should hopefully work
        locale.setlocale(locale.LC_ALL, "C")
        return "en_GB"


def l10n(msg_id: str, **kwargs) -> str:
    """
    Fetches a localised message and formats it with the given arguments

    Wrapper around portmodlib.portmod.l10n_lookup, in the Rust extension,
    which itself is built on top of
    `fluent_templates <https://github.com/XAMPPRocky/fluent-templates>`__

    args:
        msg_id: The message identifier
        kwargs: Arguments passed to the fluent formatter
    """
    # Get locale before formatting numbers so that LC_ALL gets set properly
    default = _default_locale()

    # TODO: Replace this with fluent formatting when fluent-rs better supports floats
    for key, value in kwargs.items():
        if isinstance(value, float):
            kwargs[key] = f"{value:n}"

    result = l10n_lookup(default, msg_id, kwargs)
    if result:
        return result
    raise RuntimeError(f"No Localization exists for id {msg_id}")


@lru_cache()
def get_locales(separator: str = "-") -> List[str]:
    """Returns detected locales in the form suitable for the repository"""
    locales = []
    parts = _default_locale().replace("-", "_").split("_")
    if len(parts) == 2:
        locales.append(parts[0] + separator + parts[1])
    locales.append(parts[0])
    # Default (lowest priority) is en
    locales.append("en")
    return locales
