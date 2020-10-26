def split(path):
    return path.split(".")


def snaked(path):
    return "_".join(split(path))
