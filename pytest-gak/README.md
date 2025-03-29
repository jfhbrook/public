# pytest-gak

GAK is a plugin and CLI for using [pytest](https://docs.pytest.org/en/stable/) to run interactive test suites, using prompts.

## Motivation

Pytest is typically intended for running fully automated tests. However, some tests aren't *possible* to fully automate. A particular use case is testing drivers for live hardware - for instance, executing a driver API and manually inspecting the hardware to confirm its state. This library helps solve that use case.

## Install

GAK is available on PyPI, and can be installed like so:

```bash
pip install pytest-gak
```

This will automatically register as a plugin to Pytest, and expose a script called `gaktest`.

## Usage

### Plugin

The plugin exposes some new fixtures:

- `confirm`: Confirm that a state is as expected
- `take_action`: Prompt the developer to take a physical action before continuing
- `check`: Check that a state is as expected

For example, the [plusdeck](https://github.com/jfhbrook/plusdeck) project has a test which looks like this:

```py
async def test_manual_no_events(check, confirm, take_action) -> None:
    """
    Plus Deck plays tapes manually without state subscription.
    """

    confirm("There is NO tape in the deck")

    client = await create_connection(CONFIG.port)

    @client.events.on("state")
    def unexpected_state(state: State):
        assert not state, "Should not receive state before enabling"

    take_action("Put a tape in the deck")

    check("Press Rewind. Has the tape rewound?", "Deck rewound")
    check("Press Play Side A. Is the deck playing side A?", "Deck is playing side A")
    check("Press Pause. Is the tape paused?", "Deck is paused")
    check("Press Pause. Is the tape playing?", "Deck is playing")
    check("Press Fast-Forward. Has the tape fast-forwarded?", "Deck fast-forwarded")
    check("Press Play Side B. Is the deck playing side B?", "Deck is playing side B")
    check("Press Stop. Has the tape has stopped playing?", "Deck is stopped")
    check("Press Eject. Did the tape eject?", "Deck has ejected")

    client.events.remove_listener("state", unexpected_state)

    client.close()
```

### Command Line

Pytest allows you to disable capturing of output [using the `capsys` fixture](https://docs.pytest.org/en/7.1.x/how-to/capture-stdout-stderr.html). However, this fixture [does *not* allow for disabling the capture of *stdin*](https://github.com/pytest-dev/pytest/issues/2189). Therefore, in order to run tests requiring prompts, you need to run `pytest` with the `--capture=no` setting (or with the `-s` short flag).

GAK comes with a wrapper script that will add this flag to Pytest's arguments. So instead of running:

```bash
pytest -s ./tests/test_interactive.py
```

you may run:

```bash
gaktest ./tests/test_interactive.py
```

## A Note on Naming

GAK is named after the [Geek At Keyboard testing concept, as popularized by Geepaw Hill](https://www.geepawhill.org/2018/04/14/tdd-the-lump-of-coding-fallacy/). Though, it's worth noting that the actual use of this library is distinct from Geepaw Hill's GAK concept.

GAK testing is what Geepaw calls interactive, ad-hoc testing of a program - "running the program to see how it works right now". This is the sort of testing that most developers do on-the-fly, without thinking about it. `pytest-gak`, on the other hand, partially automates these sort of tests into an automated "runbook", making them less ad-hoc - but still interactive.

Even so, the use cases are similar. For instance, Geepaw will often GAK test UIs, which are notoriously difficult to automate. In theory, `pytest-gak` would work here as well.

## Changelog

See [`CHANGELOG.md`](./CHANGELOG.md).

## License

Apache-2.0, see [`LICENSE`](./LICENSE).
