from collections import defaultdict
import os
import sys
from subprocess import Popen, DEVNULL

import attr
from twisted.internet import reactor
from twisted.internet.error import ReactorNotRunning

from pyxsession.dbus import dbus_attr, Str, Bool, DBusField
from pyxsession.detach import spawn as spawn_detached
from pyxsession.twisted.procmon import ProcessMonitor
from pyxsession.xdg.applications import Application
from pyxsession.xdg.exec_key import ExecKey
from pyxsession.xdg.executable import Executable
from pyxsession.util import Symbol


class Executor:
    def __init__(self, *, log=None, reactor=None, applications=None):
        self.applications = applications
        self.monitor = ProcessMonitor(log, reactor)

    def start(self):
        self.monitor.startService()

    def stop(self):
        self.monitor.stopService()

    def run_exec_key(
        self,
        exec_key,
        *,
        monitor=False,
        restart=False,
        cleanup=True,
        monitor_params=None,
        exec_key_fields=None,
        env=None,
        cwd=None
    ):
        argv = exec_key.build_argv(exec_key_fields)

        if not monitor:
            spawn_detached(argv, env=env, cwd=cwd)
        else:
            monitor_params = monitor_params or dict()

            self.monitor.addProcess(
                executable.filename,
                argv,
                env=env,  # TODO: Parent env
                cwd=cwd,  # TODO: default to ./
                restart=restart,
                cleanup=cleanup,
                **monitor_params
            )

    def run_command(
        self,
        raw,
        **kwargs
    ):
        return self.run_exec_key(
            ExecKey(raw),
            **kwargs
        )

    def run_xdg_executable(
        self,
        executable,
        **kwargs
    ):
        return self.run_exec_key(executable.exec_key, **kwargs)

    def run_xdg_desktop_entry(
        self,
        entry,
        **kwargs
    ):
        return self.run_xdg_executable(
            Executable.from_desktop_entry(entry),
            **kwargs
        )

    def run_xdg_application(
        self,
        app,
        **kwargs
    ):
        return self.run_xdg_executable(app.executable, **kwargs)

    def run_xdg_application_by_name(
        self,
        filename,
        **kwargs
    ):
        app = self.applications.entries[filename]
        return self.run_xdg_application(app, **kwargs)


@attr.s
class DBusApplication:
    filename = dbus_attr(type=Str(), default='')
    exec_key_fields = dbus_attr(type=DBusField('a{ss}'), default=attr.Factory(dict))
    monitor = dbus_attr(type=Bool(), default=False)
    restart = dbus_attr(type=Bool(), default=False)
    cleanup = dbus_attr(type=Bool(), default=True)
    monitor_params = dbus_attr(type=DBusField('a{sv}'), default=attr.Factory(dict))
    env = dbus_attr(type=DBusField('a{ss}'), default=attr.Factory(dict))
    cwd = dbus_attr(type=Str(), default='')


class DBusExecutor(Executor):
    def __init__(self, service, **kwargs):
        super().__init__(**kwargs)

        self.service = service
        self.obj = service.object('/pyxsession/Executor')

        @self.obj.method([DBusApplication], returns=None)
        async def run_dbus_application(dbus_app):
            if dbus_app.env == dict():
                dbus_app.env = None
            if dbus_app.cwd == '':
                dbus_app.cwd = None

            self.underlying.run_xdg_application_by_name(
                **attr.asdict(dbus_app)
            )

    async def start_client(self, connection):
        self.client = await self.service.client(connection)

    async def start_server(self, connection, underlying):
        self.underlying = underlying
        self.server = await self.service.server(connection)

    async def run_xdg_application(self, app, **kwargs):
        dbus_app = DBusApplication(filename=app.filename, **kwargs)
        await self.client.pyxsession.Executor.run_dbus_application(
            dbus_app
        )


default_executor = Executor()
