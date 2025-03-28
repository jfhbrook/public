# -*- coding: utf-8 -*-

from inspect import getmembers, isfunction
import sys

import click

from gaktest import marked_with


async def _run_tests(__name__: str) -> None:
    for name, test in getmembers(sys.modules[__name__], isfunction):
        if not name.startswith("test_"):
            continue

        if marked_with("skip", test):
            print(f"=== {name} SKIPPED ===")
            continue

        print(f"=== {name} ===")
        try:
            await test()
        except Exception as exc:
            print(f"{name} FAILED")
            print(exc)
        else:
            print(f"=== {name} PASSED ===")


@click.command()
def main():
    click.echo("hello world!")


if __name__ == "__main__":
    main()
