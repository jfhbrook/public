# -*- coding: utf-8 -*-

from typing import Callable

import pytest
from rich.prompt import Prompt


@pytest.fixture
def confirm(check) -> Callable[[str], None]:
    """
    Manually confirm an expected state.
    """

    def _confirm(text: str) -> None:
        check(text, "Confirmed!")

    return _confirm


@pytest.fixture
def take_action(capsys) -> Callable[[str], None]:
    """
    Take a manual action before continuing.
    """

    def _take_action(text: str) -> None:
        with capsys.disabled():
            print("")
            res = Prompt.ask(text, choices=["continue", "abort"], default="continue")

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
            res = Prompt.ask(text, choices=["y", "n"], default="y")

        assert res == "y", expected

    return _check
