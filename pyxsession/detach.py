import os
import sys
from subprocess import Popen, DEVNULL


    # Double-forking to truly detach the process
    # For more on the strategy, see:
    #
    # * https://stackoverflow.com/questions/5772873/python-spawn-off-a-child-subprocess-detach-and-exit  # noqa
    # * https://stackoverflow.com/questions/6011235/run-a-program-from-python-and-have-it-continue-to-run-after-the-script-is-kille  # noqa


# Our strategy is to spawn a process that then forks and execvpe's


def spawn(argv, *, env=None, cwd=None):
    shim_argv = [sys.executable, '-m', 'pyxsession.detach'] + argv

    return Popen(
        shim_argv,
        env=env,
        cwd=cwd,
        stdin=DEVNULL,
        stdout=DEVNULL,
        stderr=DEVNULL
    )


def _fork_and_popen(argv, env):
    pid = os.fork()
    if pid > 0:
        return

    os.setsid()

    print(argv)

    cmd = argv[0]

    print(cmd, argv)

    print(len(argv))
    print(bool(argv))

    if argv:
        os.execvpe(cmd, argv, env)
    else:
        os.execlpe(cmd, env)


if __name__ == '__main__':
    _fork_and_popen(sys.argv[1:], os.environ)
