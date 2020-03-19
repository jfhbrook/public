import attr

from korbenware.dbus import Bool, dbus_attr, DBusField, Str, List
from korbenware.dbus.proxy import dbus_method, dbus_proxy
from korbenware.detach import spawn as spawn_detached
from korbenware.logger import create_logger
from korbenware.twisted.procmon import ProcessMonitor
from korbenware.xdg.exec_key import ExecKey
from korbenware.xdg.executable import Executable
from korbenware.keys import keys
from korbenware.presentation import representable
from korbenware.presentation.markdown import markdownable


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


@markdownable
@representable
@keys(['monitor'])
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
        super().__init__(reactor=reactor)
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
