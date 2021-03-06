# Copyright 2020 Josh Holbrook
#
# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at https://mozilla.org/MPL/2.0/.

import datetime

import attr
from pyee import TwistedEventEmitter as EventEmitter

from korbenware.config import BaseConfig
from korbenware.dbus import Bool, DateTime, dbus_attr, Int16, Int64, List, Str
from korbenware.executor import ApplicationExecutor, MonitoringExecutor
from korbenware.keys import asdict, keys
from korbenware.open import ApplicationFinder
from korbenware.presentation import representable
from korbenware.presentation.markdown import markdownable
from korbenware.urls import UrlRegistry
from korbenware.xdg.applications import ApplicationsRegistry
from korbenware.xdg.autostart import AutostartRegistry
from korbenware.xdg.mime import MimeRegistry


class AlreadyStartedError(Exception):
    def __init__(self):
        super().__init__("This session is already started and can't be started twice")


class AlreadyStoppedError(Exception):
    def __init__(self):
        super().__init__("This session is already stopped and can't be stopped twice")


@markdownable
@representable
@attr.s
class ProcessState:
    name = dbus_attr(Str(), default="???")
    state = dbus_attr(Str(), default="UNKNOWN")
    restart = dbus_attr(Bool(), default=False)
    threshold = dbus_attr(Int64())
    killTime = dbus_attr(Int64())
    minRestartDelay = dbus_attr(Int64())
    maxRestartDelay = dbus_attr(Int64())

    @classmethod
    def from_procmon_state(cls, state):
        return cls(
            name=state.name,
            state=state.state.value,
            restart=state.settings.restart,
            threshold=state.settings.threshold or -1,
            killTime=state.settings.killTime or -1,
            minRestartDelay=state.settings.minRestartDelay or -1,
            maxRestartDelay=state.settings.maxRestartDelay or -1,
        )


@markdownable
@representable
@attr.s
class ExecutorState:
    running = dbus_attr(Int16())
    processes = dbus_attr(List(ProcessState))

    @classmethod
    def from_executor(cls, executor):
        monitor = executor.monitor.asdict()
        return cls(
            running=monitor.get("running", -1),
            processes=[
                ProcessState.from_procmon_state(state)
                for state in monitor.get("processes", {}).values()
            ],
        )


@markdownable
@representable
@attr.s
class SessionState:
    running = dbus_attr(Bool(), default=False)
    loaded_at = dbus_attr(DateTime())
    started_at = dbus_attr(DateTime())
    stopped_at = dbus_attr(DateTime())
    config = dbus_attr(BaseConfig)
    critical_executor = dbus_attr(ExecutorState)
    primary_executor = dbus_attr(ExecutorState)

    @classmethod
    def from_session(cls, session):
        return cls(
            running=session.running,
            loaded_at=session.loaded_at,
            started_at=session.started_at,
            stopped_at=session.stopped_at,
            config=session.config,
            critical_executor=ExecutorState.from_executor(session.critical_executor),
            primary_executor=ExecutorState.from_executor(session.primary_executor),
        )


@markdownable
@representable
@keys(
    [
        "running",
        "loaded_at",
        "started_at",
        "stopped_at",
        "config",
        "applications",
        "autostart",
        "mime",
        "critical_executor",
        "primary_executor",
    ]
)
class Session(EventEmitter):
    def __init__(self, reactor, config):
        super().__init__()

        self.reactor = reactor
        self.config = config

        self.applications = ApplicationsRegistry(config)
        self.autostart = AutostartRegistry(config)
        self.mime = MimeRegistry(config, self.applications)
        self.urls = UrlRegistry(config, self.applications)
        self.finder = ApplicationFinder(self.urls, self.mime)

        self.critical_executor = MonitoringExecutor(reactor)

        self.primary_executor = ApplicationExecutor(
            reactor=reactor, applications=self.applications
        )

        self.running = False
        self.loaded_at = datetime.datetime.utcnow()
        self.started_at = None
        self.stopped_at = None

    def start(self):
        if self.running:
            raise AlreadyStartedError()

        self.emit("start")

        for process_name, process_config in self.config.executors.critical.items():
            self.critical_executor.run_config(process_name, process_config)

        self.autostart.init_executor(self.primary_executor)

        @self.critical_executor.monitor.on("serviceStarted")
        def start_primary_executor():
            self.primary_executor.start()

        @self.primary_executor.monitor.on("serviceStarted")
        def finish():
            self.emit("started")

        self.critical_executor.start()
        self.primary_executor.start()

        self.running = True
        self.started_at = datetime.datetime.utcnow()

    def stop(self):
        if not self.running:
            raise AlreadyStoppedError()

        self.emit("stop")

        @self.primary_executor.monitor.on("stopped")
        def stop_critical_executor():
            self.critical_executor.stop()

        @self.critical_executor.monitor.on("stopped")
        def finish():
            self.emit("stopped")

        self.primary_executor.stop()
        self.critical_executor.stop()

        self.running = False
        self.stopped_at = datetime.datetime.utcnow()

    def restart_process(self, name):
        self.primary_executor.restart_process(name)

    def restart_critical_process(self, name):
        self.critical_executor.restart_process(name)

    def attach(self, service):
        obj = service.object("/korbenware/Session")

        @obj.method([], SessionState)
        def get_state():
            return SessionState.from_session(self)

        @obj.method([Str()], Bool())
        def run_xdg_application(name):
            self.primary_executor.run_xdg_application_by_name(name)
            return True

        @obj.method([Str()], Bool())
        def stop_xdg_application(name):
            self.primary_executor.stop_process(name)
            return True

        @obj.method([Str()], Bool())
        def start_xdg_application(name):
            self.primary_executor.start_process(name)
            return True

        @obj.method([Str()], Bool())
        def restart_xdg_application(name):
            self.primary_executor.restart_process(name)
            return True

        @obj.method([Str()], Bool())
        def restart_critical_process(name):
            self.critical_executor.restart_process(name)
            return True

        @obj.method([], Bool())
        def shutdown():
            self.stop()
            return True

        return obj
