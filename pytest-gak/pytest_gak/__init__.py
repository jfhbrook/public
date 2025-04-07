# -*- coding: utf-8 -*-

from typing import Callable

import pytest
from rich.prompt import Prompt


@pytest.fixture
def confirm(capsys) -> Callable[[str], None]:
    """
    Manually confirm an expected state.
    """

    def _confirm(text: str) -> None:
        with capsys.disabled():
            print("")
            res = Prompt.ask(text, choices=["confirm", "deny"])

        assert res == "confirm", "State was confirmed"

    return _confirm


@pytest.fixture
def take_action(capsys) -> Callable[[str], None]:
    """
    Take a manual action before continuing.
    """

    def _take_action(text: str) -> None:
        with capsys.disabled():
            print("")
            res = Prompt.ask(text, choices=["continue", "abort"])

        assert res == "continue", "Action was completed"

    return _take_action


@pytest.fixture
def check(capsys) -> Callable[[str, str], None]:
    """
    Manually check whether or not an expected state is so.
    """

    def _check(text: str, expected: str = "Everything is as expected") -> None:
        with capsys.disabled():
            print("")
            res = Prompt.ask(text, choices=["yes", "no"])

        assert res == "yes", expected

    return _check
