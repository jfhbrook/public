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
                    cleanup=True,
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
                    cleanup=False,
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
                cleanup=True,
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
                cleanup=False,
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
            cleanup=False,
            threshold=1,
            killTime=5,
            minRestartDelay=1,
            maxRestartDelay=3600,
        ),
    )


@pytest.mark.parametrize("state", [LifecycleState.RUNNING, LifecycleState.STOPPING])
@pytest_twisted.ensureDeferred
async def test_procmon_start_active_process(state, logging_protocol_cls, monitor):
    monitor.addProcess("some_process", ["some", "argv"], restart=True)

    monitor._setProcessState("some_process", state)

    monitor.startProcess("some_process")

    logging_protocol_cls.assert_not_called()
    monitor._spawnProcess.assert_not_called()


@pytest_twisted.ensureDeferred
async def test_procmon_connection_lost_unmonitored(monitor):
    monitor.running = 1
    monitor.addProcess("some_process", ["some", "argv"])

    monitor._setProcessState("some_process", LifecycleState.RUNNING)

    monitor.protocols["some_process"] = Mock()

    lost_event = Deferred()

    @monitor.once("connectionLost")
    def on_connection_lost(state):
        assert state == ProcessState(
            name="some_process",
            state=LifecycleState.STOPPED,
            settings=ProcessSettings(
                restart=False,
                cleanup=True,
                threshold=None,
                killTime=None,
                minRestartDelay=None,
                maxRestartDelay=None,
            ),
        )

        lost_event.callback(None)

    monitor.connectionLost("some_process")

    await lost_event.addTimeout(0.1, clock=reactor)

    assert "some_process" not in monitor.protocols
    assert "some_process" not in monitor.restart

    assert not monitor.isRegistered("some_process")


@pytest_twisted.ensureDeferred
async def test_procmon_connection_lost_unmonitored_no_cleanup(monitor):
    monitor.running = 1
    monitor.addProcess("some_process", ["some", "argv"], restart=False, cleanup=False)

    monitor._setProcessState("some_process", LifecycleState.RUNNING)

    monitor.protocols["some_process"] = Mock()

    lost_event = Deferred()

    @monitor.once("connectionLost")
    def on_connection_lost(state):
        assert state == ProcessState(
            name="some_process",
            state=LifecycleState.STOPPED,
            settings=ProcessSettings(
                restart=False,
                cleanup=False,
                threshold=None,
                killTime=None,
                minRestartDelay=None,
                maxRestartDelay=None,
            ),
        )

        lost_event.callback(None)

    monitor.connectionLost("some_process")

    await lost_event.addTimeout(0.1, clock=reactor)

    assert "some_process" not in monitor.protocols
    assert "some_process" not in monitor.restart

    assert monitor.getState("some_process") == ProcessState(
        name="some_process",
        state=LifecycleState.STOPPED,
        settings=ProcessSettings(
            restart=False,
            cleanup=False,
            threshold=None,
            killTime=None,
            minRestartDelay=None,
            maxRestartDelay=None,
        ),
    )


@pytest.mark.parametrize("state", [LifecycleState.STARTING, LifecycleState.RUNNING])
@pytest_twisted.ensureDeferred
async def test_procmon_connection_lost_monitored_active(state, monitor):
    monitor.running = 1
    monitor.addProcess(
        "some_process", ["some", "argv"], restart=True, minRestartDelay=0
    )

    monitor._setProcessState("some_process", state)

    monitor.protocols["some_process"] = Mock()
    monitor.timeStarted["some_process"] = -1000000

    lost_event = Deferred()

    @monitor.once("connectionLost")
    def on_connection_lost(state):
        assert state == ProcessState(
            name="some_process",
            state=LifecycleState.RESTARTING,
            settings=ProcessSettings(
                restart=True,
                cleanup=False,
                threshold=1,
                killTime=5,
                minRestartDelay=0,
                maxRestartDelay=3600,
            ),
        )

        lost_event.callback(None)

    restart_event = Deferred()

    @monitor.once("startProcess")
    def on_start(state):
        assert state == ProcessState(
            name="some_process",
            state=LifecycleState.RESTARTING,
            settings=ProcessSettings(
                restart=True,
                cleanup=False,
                threshold=1,
                killTime=5,
                minRestartDelay=0,
                maxRestartDelay=3600,
            ),
        )

        restart_event.callback(None)

    monitor.connectionLost("some_process")

    await lost_event.addTimeout(0.1, clock=reactor)

    await restart_event.addTimeout(0.1, clock=reactor)


@pytest.mark.parametrize("state", [LifecycleState.STOPPING, LifecycleState.STOPPED])
@pytest_twisted.ensureDeferred
async def test_procmon_connection_lost_monitored_inactive(state, monitor):
    monitor.running = 1
    monitor.addProcess(
        "some_process", ["some", "argv"], restart=True, minRestartDelay=0
    )

    monitor._setProcessState("some_process", state)

    monitor.protocols["some_process"] = Mock()

    lost_event = Deferred()

    @monitor.once("connectionLost")
    def on_connection_lost(state):
        assert state == ProcessState(
            name="some_process",
            state=LifecycleState.STOPPED,
            settings=ProcessSettings(
                restart=True,
                cleanup=False,
                threshold=1,
                killTime=5,
                minRestartDelay=0,
                maxRestartDelay=3600,
            ),
        )

        lost_event.callback(None)

    monitor.connectionLost("some_process")

    await lost_event.addTimeout(0.1, clock=reactor)

    assert "some_process" not in monitor.protocols
    assert "some_process" not in monitor.restart

    assert monitor.getState("some_process") == ProcessState(
        name="some_process",
        state=LifecycleState.STOPPED,
        settings=ProcessSettings(
            restart=True,
            cleanup=False,
            threshold=1,
            killTime=5,
            minRestartDelay=0,
            maxRestartDelay=3600,
        ),
    )
