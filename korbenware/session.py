import attr

from korbenware.config import BaseConfig
from korbenware.dbus import Bool, dbus_attr, Int16, Int64, List, Str
from korbenware.executor import ApplicationExecutor, MonitoringExecutor
from korbenware.keys import keys
from korbenware.open import ApplicationFinder
from korbenware.presentation import representable
from korbenware.presentation.markdown import markdownable
from korbenware.urls import UrlRegistry
from korbenware.xdg.applications import ApplicationsRegistry
from korbenware.xdg.autostart import AutostartRegistry
from korbenware.xdg.mime import MimeRegistry


@markdownable
@representable
@attr.s
class ProcessState:
    name = dbus_attr(Str(), default='???')
    state = dbus_attr(Str(), default='UNKNOWN')
    restart = dbus_attr(Bool(), default=False)
    threshold = dbus_attr(Int64(), default=-1)
    killTime = dbus_attr(Int64(), default=-1)
    minRestartDelay = dbus_attr(Int64(), default=-1)
    maxRestartDelay = dbus_attr(Int64(), default=-1)

    @classmethod
    def from_procmon_state(cls, state):
        return cls(
            name=state.name,
            state=state.state.value,
            restart=state.settings.restart,
            threshold=state.settings.threshold or -1,
            killTime=state.settings.killTime or -1,
            minRestartDelay=state.settings.minRestartDelay or -1,
            maxRestartDelay=state.settings.maxRestartDelay or -1
        )


@markdownable
@representable
@attr.s
class ExecutorState:
    running = dbus_attr(Int16(), default=-1)
    processes = dbus_attr(List(ProcessState), default=[])

    @classmethod
    def from_executor(cls, executor):
        monitor = executor.monitor.asdict()
        return cls(
            running=monitor.get('running', -1),
            processes=[
                ProcessState.from_procmon_state(state)
                for state in monitor.get('processes', {}).values()
            ]
        )


@markdownable
@representable
@attr.s
class SessionState:
    config = dbus_attr(BaseConfig)
    critical_executor = dbus_attr(ExecutorState)
    primary_executor = dbus_attr(ExecutorState)

    @classmethod
    def from_session(cls, session):
        return cls(
            config=session.config,
            critical_executor=ExecutorState.from_executor(
                session.critical_executor
            ),
            primary_executor=ExecutorState.from_executor(
                session.primary_executor
            )
        )


@markdownable
@representable
@keys([
    'config',
    'applications',
    'autostart',
    'mime',
    'urls',
    'finder',
    'critical_executor',
    'primary_executor'
])
class Session:
    def __init__(self, reactor, config):
        self.reactor = reactor
        self.config = config

        self.applications = ApplicationsRegistry(config)
        self.autostart = AutostartRegistry(config)
        self.mime = MimeRegistry(config, self.applications)
        self.urls = UrlRegistry(config, self.applications)
        self.finder = ApplicationFinder(self.urls, self.mime)

        self.critical_executor = MonitoringExecutor(reactor)
        self.primary_executor = ApplicationExecutor(
            reactor=reactor,
            applications=self.applications
        )

    def start(self):
        self.critical_executor.start()
        self.primary_executor.start()

    def stop(self):
        self.primary_executor.stop()
        self.critical_executor.stop()

    def attach(self, service):
        obj = service.object('/Session')

        @obj.method([], SessionState)
        def get_state():
            return SessionState.from_session(self)

        return obj
