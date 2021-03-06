# Copyright 2020 Josh Holbrook
#
# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at https://mozilla.org/MPL/2.0/.

import os

from korbenware.detach import spawn as spawn_detached
from korbenware.env import load_env
from korbenware.logger import create_logger
from korbenware.twisted.procmon import ProcessMonitor
from korbenware.xdg.exec_key import ExecKey
from korbenware.xdg.executable import Executable
from korbenware.keys import asdict, keys
from korbenware.presentation import representable
from korbenware.presentation.markdown import markdownable


class BaseExecutor:
    log = create_logger()

    def run_argv(
        self, process_name, argv, *, env=None, cwd=None,
    ):
        env = load_env(env)
        cwd = cwd or os.getcwd()

        self.log.info(
            "Spawning {process_name} using {argv} as a detached process...",
            process_name=process_name,
            argv=argv,
            env=env,
            cwd=cwd,
        )
        spawn_detached(argv, env=env, cwd=cwd)

    def run_config(self, process_name, config):
        kwargs = asdict(config)
        for key in list(kwargs.keys()):
            if not kwargs.get(key, None) and not isinstance(
                kwargs.get(key, None), bool
            ):
                del kwargs[key]

        return self.run_argv(process_name, **kwargs)

    def run_exec_key(
        self,
        process_name,
        exec_key,
        *,
        exec_key_fields=None,
        env=None,
        cwd=None,
        **kwargs,
    ):
        argv = exec_key.build_argv(exec_key_fields)

        self.run_argv(process_name, argv, env=env, cwd=cwd, **kwargs)

    def run_command(self, process_name, raw, **kwargs):
        return self.run_exec_key(process_name, ExecKey(raw), **kwargs)

    def run_xdg_executable(self, executable, **kwargs):
        self.log.debug(
            "Running XDG executable {filename}...",
            filename=executable.filename or ("<unknown filename>"),
        )
        return self.run_exec_key(executable.filename, executable.exec_key, **kwargs)

    def run_xdg_desktop_entry(self, entry, **kwargs):
        return self.run_xdg_executable(Executable.from_desktop_entry(entry), **kwargs)

    def run_xdg_application(self, app, **kwargs):
        return self.run_xdg_executable(app.executable, **kwargs)


@markdownable
@representable
@keys(["monitor"])
class MonitoringExecutor(BaseExecutor):
    log = create_logger()

    def __init__(self, reactor=None):
        super().__init__()
        self.monitor = ProcessMonitor(log=self.log, reactor=reactor)

    def start(self):
        self.log.info("Starting monitoring service...")
        self.monitor.startService()

    def stop(self):
        self.log.info("Stopping monitoring service...")
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
        cwd=None,
    ):
        if not monitor:
            return super().run_argv(process_name, argv, env=env, cwd=cwd)

        env = load_env(env)
        cwd = cwd or os.getcwd()
        monitor_params = monitor_params or dict()

        self.log.info(
            "Adding {process_name} using {argv} as a monitored process...",  # noqa
            process_name=process_name,
            argv=argv,
            restart=restart,
            cleanup=cleanup,
            monitor_params=monitor_params,
            env=env,
            cwd=cwd,
        )

        self.monitor.addProcess(
            process_name, argv, env=env, cwd=cwd, restart=restart, cleanup=cleanup
        )

    def start_process(self, name):
        self.monitor.startProcess(name)

    def stop_process(self, name):
        self.monitor.stopProcess(name)

    def restart_process(self, name):
        self.monitor.restartProcess(name)

    def has_process(self, name):
        return self.monitor.hasProcess(name)


class ApplicationExecutor(MonitoringExecutor):
    log = create_logger()

    def __init__(self, *, reactor=None, applications=None):
        super().__init__(reactor=reactor)
        self.applications = applications

    def run_xdg_application_by_name(self, filename, **kwargs):
        self.log.debug(
            "Running XDG application {filename} by name...", filename=filename
        )
        app = self.applications.entries[filename]
        return self.run_xdg_application(app, **kwargs)
