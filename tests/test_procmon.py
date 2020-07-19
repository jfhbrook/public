import pytest
import pytest_twisted

from twisted.internet import reactor
from twisted.internet.defer import Deferred
from unittest.mock import Mock

from korbenware.twisted.procmon import (
    LifecycleState,
    ProcessMonitor,
    ProcessSettings,
    ProcessState,
)


@pytest.fixture
def monitor():
    monitor = ProcessMonitor(reactor=reactor)

    monitor._spawnProcess = Mock(name="_spawnProcess")

    return monitor


@pytest.fixture
def logging_protocol_cls(monkeypatch):
    cls = Mock(name="logging_protocol_cls")

    monkeypatch.setattr("korbenware.twisted.procmon.LoggingProtocol", cls)

    return cls


def test_procmon_is_registered(monitor):
    assert not monitor.isRegistered("unregistered_process")

    with pytest.raises(KeyError):
        monitor.assertRegistered("unregistered_process")

    monitor.addProcess("registered_process", ["registered_process"])

    assert monitor.isRegistered("registered_process")
    monitor.assertRegistered("registered_process")


@pytest.mark.parametrize(
    "name,argv,kwargs,expected",
    [
        (
            "some_process",
            ["some", "argv"],
            dict(),
            ProcessState(
                name="some_process",
                state=LifecycleState.STOPPED,
                settings=ProcessSettings(
                    restart=False,
                    threshold=None,
                    killTime=None,
                    minRestartDelay=None,
                    maxRestartDelay=None,
                ),
            ),
        ),
        (
            "some_process",
            ["some", "argv"],
            dict(restart=True),
            ProcessState(
                name="some_process",
                state=LifecycleState.STOPPED,
                settings=ProcessSettings(
                    restart=True,
                    threshold=1,
                    killTime=5,
                    minRestartDelay=1,
                    maxRestartDelay=3600,
                ),
            ),
        ),
    ],
)
@pytest_twisted.ensureDeferred
async def test_procmon_add_process(name, argv, kwargs, expected, monitor):
    add_event = Deferred()

    @monitor.once("addProcess")
    def on_add_process(state):
        assert state == expected
        add_event.callback(None)

    monitor.addProcess(name, argv, **kwargs)

    assert monitor.settings["some_process"] == expected.settings

    monitor.getState("some_process") == expected

    await add_event.addTimeout(0.1, clock=reactor)


@pytest_twisted.ensureDeferred
async def test_procmon_remove_process(monitor):
    monitor.addProcess("some_process", ["some", "argv"])

    remove_event = Deferred()

    @monitor.once("removeProcess")
    def on_remove_process(state):
        assert state == ProcessState(
            name="some_process",
            state=LifecycleState.STOPPED,
            settings=ProcessSettings(
                restart=False,
                threshold=None,
                killTime=None,
                minRestartDelay=None,
                maxRestartDelay=None,
            ),
        )

        remove_event.callback(None)

    monitor.removeProcess("some_process")

    await remove_event.addTimeout(0.1, clock=reactor)

    assert "some_process" not in monitor.settings
    assert "some_name" not in monitor.states


@pytest_twisted.ensureDeferred
async def test_procmon_start_process_happy_path(logging_protocol_cls, monitor):
    start_event = Deferred()

    @monitor.once("startProcess")
    def on_start_process(state):
        assert state == ProcessState(
            name="some_process",
            state=LifecycleState.STOPPED,
            settings=ProcessSettings(
                restart=True,
                threshold=1,
                killTime=5,
                minRestartDelay=1,
                maxRestartDelay=3600,
            ),
        )

        start_event.callback(None)

    monitor.addProcess("some_process", ["some", "argv"], restart=True)

    monitor.startProcess("some_process")

    await start_event.addTimeout(0.1, clock=reactor)

    assert monitor.protocols["some_process"] == logging_protocol_cls.return_value
    assert monitor.protocols["some_process"].name == "some_process"
    assert monitor.protocols["some_process"].service == monitor
    assert isinstance(monitor.timeStarted["some_process"], float)
    monitor._spawnProcess.assert_called_once_with(
        monitor.protocols["some_process"],
        "some",
        ["some", "argv"],
        uid=None,
        gid=None,
        env=dict(),
        path=None,
    )

    assert monitor.getState("some_process") == ProcessState(
        name="some_process",
        state=LifecycleState.RUNNING,
        settings=ProcessSettings(
            restart=True,
            threshold=1,
            killTime=5,
            minRestartDelay=1,
            maxRestartDelay=3600,
        ),
    )
