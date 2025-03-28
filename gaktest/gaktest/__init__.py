# -*- coding: utf-8 -*-

from collections.abc import Awaitable
from inspect import getmembers, isfunction
import sys
from typing import Callable, cast, Protocol, Set, Union

from rich.prompt import Prompt

"""
Tools for manual testing with real hardware.
"""


class AbortError(Exception):
    """A manual testing step has been aborted."""

    pass


def confirm(text: str) -> None:
    """Manually confirm an expected state."""

    res = Prompt.ask(text, choices=["confirm", "abort"])

    if res == "abort":
        raise AbortError("Aborted.")


def take_action(text: str) -> None:
    """Take a manual action before continuing."""

    res = Prompt.ask(text, choices=["continue", "abort"])

    if res == "abort":
        raise AbortError("Aborted.")


def check(text: str, expected: str) -> None:
    """Manually check whether or not an expected state is so."""

    res = Prompt.ask(text, choices=["yes", "no", "abort"])

    if res == "abort":
        raise AbortError("Aborted.")

    assert res == "yes", expected


class MarkedTest(Protocol):
    marks: Set[str]

    def __call__(self) -> Awaitable[None]: ...


UnmarkedTest = Callable[[], Awaitable[None]]

Test = Union[UnmarkedTest, MarkedTest]


def mark(tag: str) -> Callable[[Test], MarkedTest]:
    def decorator(test: Test) -> MarkedTest:
        marked = cast(MarkedTest, test)

        if not hasattr(test, "marks"):
            marked.marks = set()

        marked.marks.add(tag)

        return marked

    return decorator


def skip(test: Test) -> MarkedTest:
    """Skip a test."""

    return mark("skip")(test)


def marked_with(tag: str, test: Test) -> bool:
    """Check if a test has a mark."""

    if not hasattr(test, "marks"):
        return False

    return tag in cast(MarkedTest, test).marks
