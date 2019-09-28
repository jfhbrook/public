import attr

from korbenware.dbus import Bool, dbus_attr, DBusField, Str, List
from korbenware.dbus.proxy import dbus_method, dbus_proxy
from korbenware.detach import spawn as spawn_detached
from korbenware.logger import create_logger
from korbenware.twisted.procmon import ProcessMonitor
from korbenware.xdg.exec_key import ExecKey
from korbenware.xdg.executable import Executable


class BaseExecutor:
    log = create_logger()

    def run_argv(
        self,
        process_name,
        argv,
        *,
        env=None,
        cwd=None
    ):
        self.log.info(
            'Spawning {process_name} using {argv} as a detached process...',
            process_name=process_name,
            argv=argv,
            env=env,
            cwd=cwd
        )
        spawn_detached(argv, env=env, cwd=cwd)

    def run_exec_key(
        self,
        process_name,
        exec_key,
        *,
        exec_key_fields=None,
        env=None,
        cwd=None
    ):
        argv = exec_key.build_argv(exec_key_fields)

        self.run_argv(process_name, argv, env=env, cwd=cwd)

    def run_command(
        self,
        process_name,
        raw,
        **kwargs
    ):
        return self.run_exec_key(
            process_name,
            ExecKey(raw),
            **kwargs
        )

    def run_xdg_executable(
        self,
        executable,
        **kwargs
    ):
        self.log.debug(
            'Running XDG executable {filename}...',
            filename=executable.filename or ('<unknown filename>')
        )
        return self.run_exec_key(
            executable.filename,
            executable.exec_key,
            **kwargs
        )

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


class MonitoringExecutor(BaseExecutor):
    log = create_logger()

    def __init__(self, reactor=None):
        super().__init__()
        self.monitor = ProcessMonitor(log=self.log, reactor=reactor)

    def start(self):
        self.log('Starting monitoring service...')
        self.monitor.startService()

    def stop(self):
        self.log('Stopping monitoring service...')
        self.monitor.stopService()

    def run_argv(
        self,
        process_name,
        argv,
        *,
        monitor=False,
        restart=False,
        cleanup=True,
        monitor_params=None,
        env=None,
        cwd=None
    ):
        if not monitor:
            return super().run_argv(process_name, argv, env=env, cwd=cwd)

        monitor_params = monitor_params or dict()

        self.log.info(
            'Spawning {process_name} using {argv} as a monitored process...',  # noqa
            process_name=process_name,
            argv=argv,
            restart=restart,
            cleanup=cleanup,
            monitor_params=monitor_params,
            env=env,
            cwd=cwd
        )

        self.monitor.addProcess(
            process_name,
            argv,
            env=env,  # TODO: Parent env
            cwd=cwd,  # TODO: default to ./
            restart=restart,
            cleanup=cleanup
        )


class ApplicationExecutor(MonitoringExecutor):
    log = create_logger()

    def __init__(self, *, reactor=None, applications=None):
        super().__init__(self, reactor=reactor)
        self.applications = applications

    def run_xdg_application_by_name(
        self,
        filename,
        **kwargs
    ):
        self.log.debug(
            'Running XDG application {filename} by name...',
            filename=filename
        )
        app = self.applications.entries[filename]
        return self.run_xdg_application(app, **kwargs)


class MonitorAttrsMixin:
    monitor = dbus_attr(field=Bool(), default=False)
    restart = dbus_attr(field=Bool(), default=False)
    cleanup = dbus_attr(field=Bool(), default=True)
    monitor_params = dbus_attr(
        field=DBusField('a{sv}'),
        default=attr.Factory(dict)
    )


class EnvAttrsMixin:
    env = dbus_attr(
        field=DBusField('a{ss}'),
        default=attr.Factory(dict)
    )
    cwd = dbus_attr(field=Str(), default='')

    def repair_env_in_place(self):
        if self.env == dict():
            self.env = None
        if self.cwd == '':
            self.cwd = None


@attr.s
class DBusApplicationPayload(MonitorAttrsMixin, EnvAttrsMixin):
    filename = dbus_attr(field=Str(), default='')
    exec_key_fields = dbus_attr(
        field=DBusField('a{ss}'),
        default=attr.Factory(dict)
    )


@attr.s
class DBusArgvPayload(MonitorAttrsMixin, EnvAttrsMixin):
    process_name = dbus_attr(field=Str(), default='')
    argv = dbus_attr(field=List(Str()), default=attr.Factory(list))


@dbus_proxy
class DBusExecutor(BaseExecutor):

    @dbus_method([DBusArgvPayload], None)
    async def run_argv(self, server_method, *args, **kwargs):
        await server_method(DBusArgvPayload(*args, **kwargs))

    @run_argv.server_method
    async def _run_dbus_argv(self, payload):
        payload.repair_env_in_place()
        await self.underlying.run_argv(**payload)

    # run_exec_key calls run_argv
    # run_command calls run_exec_key

    async def run_xdg_executable(self, *args, **kwargs):
        raise NotImplementedError(
            'run_xdg_executable not implemented over dbus!'
        )

    async def run_xdg_desktop_entry(self, *args, **kwargs):
        raise NotImplementedError(
            'run_xdg_desktop_entry not implemented over dbus!'
        )

    @dbus_method([DBusApplicationPayload], None)
    async def run_xdg_application_by_name(
        self, server_method, filename, **kwargs
    ):
        await server_method(DBusApplicationPayload(
            filename=filename,
            **kwargs
        ))

    @run_xdg_application_by_name.server_method
    async def _run_dbus_application(self, payload):
        payload.repair_env_in_place()
        await self.underlying.run_xdg_application_by_name(**payload)

    def run_xdg_application(self, app, **kwargs):
        return self.run_xdg_application_by_name(app.filename, **kwargs)
