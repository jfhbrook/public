from collections import defaultdict
import os
import sys
from subprocess import Popen, DEVNULL

import attr
from twisted.internet import reactor
from twisted.internet.error import ReactorNotRunning

from pyxsession.xdg.executable import Executable
from pyxsession.twisted.procmon import ProcessMonitor


def spawn_detached_process(argv, *, env=None, cwd=None):
    # Double-forking to truly detach the process
    # For more on the strategy, see:
    #
    # * https://stackoverflow.com/questions/5772873/python-spawn-off-a-child-subprocess-detach-and-exit  # noqa
    # * https://stackoverflow.com/questions/6011235/run-a-program-from-python-and-have-it-continue-to-run-after-the-script-is-kille  # noqa

    pid = os.fork()
    if pid > 0:
        return

    # TODO: An OSError here means forking failed. Right now we eat shit, do
    # we want to do something different?

    os.setsid()

    Popen(
        argv,
        stdin=DEVNULL,
        stdout=DEVNULL,
        stderr=DEVNULL,
        env=env,
        cwd=cwd
    )

    sys.exit(0)


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
            spawn_detached_process(argv, env=env, cwd=cwd)
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
