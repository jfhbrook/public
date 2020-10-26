import os
import shlex


def edit(path):
    argv = shlex.split(os.environ.get("EDITOR", "vi"))
    cmd = argv[0]
    argv.append(str(path))

    os.execvpe(cmd, argv, os.environ)
