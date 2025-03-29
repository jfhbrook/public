# -*- coding: utf-8 -*-

import pytest


def test_confirm(confirm) -> None:
    confirm("Confirm this prompt")


def test_deny(confirm) -> None:
    with pytest.raises(AssertionError):
        confirm("Deny this prompt")


def test_take_action(take_action) -> None:
    take_action("Say continue")


def test_abort_action(take_action) -> None:
    with pytest.raises(AssertionError):
        take_action("Abort! Abort! Abort!")


def test_check_yes(check) -> None:
    check("Say yes")


def test_check_no(check) -> None:
    with pytest.raises(AssertionError):
        check("Say no")
