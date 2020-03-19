import attr

from korbenware.config import BaseConfig
from korbenware.dbus import Bool, dbus_attr, from_attrs, List, Nested
from korbenware.executor import ApplicationExecutor, MonitoringExecutor
from korbenware.open import ApplicationFinder
from korbenware.presentation import representable
from korbenware.presentation.markdown import markdownable
from korbenware.urls import UrlRegistry
from korbenware.xdg.applications import ApplicationsRegistry
from korbenware.xdg.mime import MimeRegistry


@markdownable
@representable
@attr.s
class ProcessState:
    restart = dbus_attr(Bool(), default=False)

    @classmethod
    def from_procmon(cls, setting, state):
        return cls()


def executor_state(executor):
    monitor = executor.monitor

    return [
        ProcessState.from_procmon(
            monitor.settings.get(key, None),
            monitor.states.get(key, None)
        )
        for key in (
            set(monitor.settings.keys()).union(set(monitor.states.keys()))
        )
    ]


@markdownable
@representable
@attr.s
class SessionState:
    config = dbus_attr(BaseConfig)
    critical_executor = dbus_attr(List(Nested(from_attrs(ProcessState))))

    @classmethod
    def from_session(cls, session):
        return cls(
            config=session.config,
            critical_executor=[]
        )


class Session:
    def __init__(self, reactor, config):
        self.reactor = reactor
        self.config = config

        self.applications = ApplicationsRegistry(config)
        self.mime = MimeRegistry(config, self.applications)
        self.urls = UrlRegistry(config, self.applications)
        self.finder = ApplicationFinder(self.urls, self.mime)

        self.critical_executor = MonitoringExecutor(reactor)
        self.primary_executor = ApplicationExecutor(
            reactor=reactor,
            applications=self.applications
        )

    def attach(self, service):
        obj = service.object('/Session')

        @obj.method([], SessionState)
        def get_state():
            return SessionState.from_session(self)

        return obj
