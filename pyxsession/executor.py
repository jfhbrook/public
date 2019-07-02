from collections import defaultdict
import os
import sys
from subprocess import Popen, DEVNULL

import attr
from twisted.internet import reactor
from twisted.internet.error import ReactorNotRunning

from pyxsession.xdg.executable import Executable
from pyxsession.twisted.procmon import ProcessMonitor
from pyxsession.detach import spawn as spawn_detached


class Executor:
    def __init__(self, log=None, reactor=None):
        self.monitor = ProcessMonitor(log, reactor)

    def start(self):
        self.monitor.startService()

    def stop(self):
        self.monitor.stopService()

    def run_xdg_desktop_entry(
        self,
        entry,
        **kwargs
    ):
        return self.run_xdg_executable(
            Executable.from_desktop_entry(entry),
            **kwargs
        )

    def run_xdg_executable(
        self,
        executable,
        *,
        monitor=False,
        restart=False,
        cleanup=True,
        monitor_params=None,
        exec_key_fields=None,
        env=None,
        cwd=None
    ):
        argv = executable.exec_key.build_argv(exec_key_fields)
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


class ExecutorPool(defaultdict):
    def __missing__(self, key):
        # TODO: Set up logging
        return Executor()


executors = ExecutorPool()


class _Key:
    pass


DEFAULT_KEY = _Key()
default_executor = executors[DEFAULT_KEY]


def autostart(autostart_configuration):
    raise NotImplementedError()
