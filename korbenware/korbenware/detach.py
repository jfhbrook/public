import os
import sys
from subprocess import Popen, DEVNULL

# Our strategy is to spawn a process piped to /dev/null that then forks and
# execvpe's our program for us. The goal is to get a process that won't shut
# down when we close the parent.
#
# This can be useful if an application is launched directly in the shell,
# since it'll background the process and let you keep typing on your computer.
#
# TODO: Test behavior of X11 applications during logout. It would be really
# funny if it doesn't handle this well.
# TODO: Check the properties of the child process to ensure that this is
# actually doing what I think it is!
#
# My favorite StackOverflow reading on how/why "double forking" is desired:
#
# https://stackoverflow.com/questions/881388/what-is-the-reason-for-performing-a-double-fork-when-creating-a-daemon  # noqa


def spawn(argv, *, env=None, cwd=None):
    # We execute a child process rather than fork here, because twisted gets
    # very grumpy if you call os.fork while the reactor is running. See:
    # https://stackoverflow.com/questions/13181561/python-twisted-fork-for-background-non-returning-processing  # noqa

    shim_argv = [sys.executable, "-m", "korbenware.detach"] + argv

    return Popen(
        shim_argv, env=env, cwd=cwd, stdin=DEVNULL, stdout=DEVNULL, stderr=DEVNULL
    )


def _fork_and_popen(argv, env):
    pid = os.fork()
    if pid > 0:
        return

    # A good description on StackOverflow as to why this is necessary:
    # https://stackoverflow.com/questions/45911705/why-use-os-setsid-in-python
    os.setsid()

    cmd = argv[0]

    if argv:
        os.execvpe(cmd, argv, env)
    else:
        os.execlpe(cmd, env)


if __name__ == "__main__":
    _fork_and_popen(sys.argv[1:], os.environ)
