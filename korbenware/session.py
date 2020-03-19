import attr

from korbenware.config import BaseConfig
from korbenware.dbus import dbus_attr
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
class SessionState:
    config = dbus_attr(BaseConfig)

    @classmethod
    def from_session(cls, session):
        return cls(
            config=session.config
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

    def dbus_object(self, service):
        obj = service.object('/Session')

        @obj.method([], SessionState)
        def get_state():
            return SessionState.from_session(self)

        return obj
