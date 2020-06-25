import os
import shlex


def edit(path):
    argv = shlex.split(os.environ.get('EDITOR', 'vi'))
    cmd = argv[0]
    argv.append(path)

    print(cmd, argv)

    os.execvpe(cmd, argv, os.environ)
