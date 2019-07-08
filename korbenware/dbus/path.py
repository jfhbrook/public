def basename(path):
    return path.split('/')[-1]


def split(path):
    return path[1:].split('/')


def snaked(path):
    return '_'.join(split(path))
