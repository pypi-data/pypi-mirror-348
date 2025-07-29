# Copyright 2019-2021 Portmod Authors
# Distributed under the terms of the GNU General Public License v3

"""
CLI prompt functions
"""

import sys
from textwrap import fill
from typing import AbstractSet, Any, List, Optional, Sequence, Tuple

from portmodlib.colour import bright, lblue, lgreen, lred
from portmodlib.l10n import l10n


def display_num_list(
    items: Sequence[str],
    notes: Optional[Sequence[str]] = None,
    selected: AbstractSet[int] = frozenset(),
    *,
    start: int = 0,
):
    """
    Displays a numbered list to stdout

    args:
        items: The primary elements to be displayed
        notes: A secondary note which, if provided, will be displayed in parentheses after the item
        selected: Selected indices will be followed by an asterisk
        start: The index to begin the list
    """
    padding = len(str(len(items)))

    def print_item(index: int, item: str, note: Optional[str]):
        selected_str = ""
        note_str = ""
        if index in selected:
            selected_str = lblue("*")
        index_str = bright("[" + str(index) + "]")
        if note:
            note_str = f" ({note})"
        print(
            f'  {index_str} {" " * (padding - len(str(index))) + item}',
            note_str,
            selected_str,
        )

    if notes:
        for index, (item, note) in enumerate(zip(items, notes)):
            print_item(index + start, item, note)
    else:
        for index, item in enumerate(items):
            print_item(index + start, item, None)


def strtobool(value: str) -> bool:
    """
    Returns true if the value is a string with contents representing true
    and false if the value is a string with contents representing false

    True options include: yes, y, true, t, 1
    False options include: no, n, false, f, 1

    This function is localized.
    """
    _true = {
        l10n("yes-short"),
        l10n("yes").lower(),
        l10n("true").lower(),
        l10n("true-short"),
        "1",
    }
    _false = {
        l10n("no-short"),
        l10n("no").lower(),
        l10n("false").lower(),
        l10n("false-short"),
        "0",
    }

    if value.lower() in _true:
        return True
    if value.lower() in _false:
        return False
    raise ValueError(f"Invalid boolean value {value}")


def prompt_bool(question) -> bool:
    """
    Prompts the user for yes or no

    See :func:`strtobool` for details of how the response is parsed

    args:
        question: The question to display prior to the prompt

    raises:
        EOFError: If the user enters -1 or EOF

    returns:
        True if the user answered yes, or false if the user answered no
    """

    sys.stdout.write(
        "{} [{}/{}]: ".format(
            question, bright(lgreen(l10n("yes"))), bright(lred(l10n("no")))
        )
    )
    while True:
        try:
            return strtobool(input().strip().lower())
        except ValueError:
            sys.stdout.write(
                l10n(
                    "prompt-invalid-response",
                    yes=bright(lgreen(l10n("yes"))),
                    no=bright(lred(l10n("no"))),
                )
            )


def prompt_options(question: str, options: List[Tuple[str, str]]) -> str:
    """
    Prompts the user for one of a given set of options

    args:
        question: The question to display prior to the prompt
        options: The list of possible option and description pairs

    raises:
        EOFError: If the user enters an EOF

    returns:
        The string entered by the user, which will correspond exactly to one of the options
    """
    print(question)
    # extra 2 for colon and an extra space
    max_option_width = max(len(option) for option, _ in options) + 2
    for option, desc in options:
        print(
            option + ":",
            fill(
                desc,
                width=80,
                initial_indent=" " * (max_option_width - len(option) - 2),
                subsequent_indent=" " * max_option_width,
            ),
        )
    sys.stdout.write("[{}]: ".format("/".join([option for option, _ in options])))
    option_set = {option for option, _ in options}
    while True:
        result = input().strip()
        if result in option_set:
            return result

        sys.stdout.write(
            l10n(
                "prompt-invalid-response-multiple",
                options="/".join([option for option, _ in options]),
            )
        )


def prompt_num(question: str, max_val: int, cancel: bool = False) -> int:
    """
    Prompts the user for exactly one number

    The input number must be positive

    args:
        question: The question to display prior to the prompt
        max_val: The maximum valid number that will be accepted
        cancel: If true, the user has the option to enter -1 to raise an EOFError

    raises:
        EOFError: If the user enters -1 (and cancel is True) or EOF

    returns:
        The number the user entered
    """

    print("{}: ".format(question))
    while True:
        try:
            result = int(input().strip())
            if result > max_val or result < 0:
                if result == -1 and cancel:
                    raise EOFError()

                print(l10n("prompt-range-too-large", max=max_val))
            else:
                return result
        except ValueError:
            print(l10n("prompt-invalid-range", max=max_val))


def multi_select_prompt(
    question: str, options: List[Any], *, help_message: Optional[str] = None
) -> List[Any]:
    from portmodlib.portmod import multi_select_prompt

    return multi_select_prompt(
        question,
        options,
        help_message
        or "Select with space and accept with enter. "
        "Typing filters the list; Escape to quit",
    )
