# -*- coding: utf-8 -*-

from typing import Callable, Never

import pytest
from rich.prompt import Prompt


class AbortError(AssertionError):
    """
    An exception raised when manual testing step has been aborted.
    """

    pass


@pytest.fixture
def abort() -> Callable[[], Never]:
    """
    Abort a GAK test.
    """

    def _abort() -> Never:
        raise AbortError("Aborted.")

    return _abort


@pytest.fixture
def confirm(abort, capsys) -> Callable[[str], None]:
    """
    Manually confirm an expected state.
    """

    def _confirm(text: str) -> None:
        with capsys.disabled():
            print("")
            res = Prompt.ask(text, choices=["confirm", "abort"])

        if res == "abort":
            abort()

    return _confirm


@pytest.fixture
def take_action(abort, capsys) -> Callable[[str], None]:
    """
    Take a manual action before continuing.
    """

    def _take_action(text: str) -> None:
        with capsys.disabled():
            print("")
            res = Prompt.ask(text, choices=["continue", "abort"])

        if res == "abort":
            abort()

    return _take_action


@pytest.fixture
def check(abort, capsys) -> Callable[[str, str], None]:
    """
    Manually check whether or not an expected state is so.
    """

    def _check(text: str, expected: str) -> None:
        with capsys.disabled():
            print("")
            res = Prompt.ask(text, choices=["yes", "no", "abort"])

        if res == "abort":
            abort()

        assert res == "yes", expected

    return _check
