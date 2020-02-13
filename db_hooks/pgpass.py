import os
import os.path
import re
import stat

import attrs

PERMISSIONS = stat.S_IRUSR | stat.S_IWUSR

def pg_pass_file():
    if os.name == "nt":
        return os.path.join(os.getenv("APPDATA"), "postgresql", "pgpass.conf")
    return os.path.expanduser("~/.pgpass")

@attr.s
class PGPassLine:
    raw = attr.ib()
    managed = attr.ib(default=False)
    host = attr.ib(default=None)
    port = attr.ib(default=None)
    database = attr.ib(default=None)
    username = attr.ib(default=None)
    password = attr.ib(default=None)
    metadata = attr.ib(default=attr.factory(dict))

    @classmethod
    def parse(cls, raw):
        match = re.match(
            r"^([^:]+?):([^:]+?):([^:]+?):([^:]+?):([^:]+?)\s+#\s+db_hooks\s+(.*)",
            raw.strip()
        )
        if match:
            return cls(
                raw=raw,
                managed=True,
                host = match.group(1),
                port = int(match.group(2)),
                database = match.group(3),
                username = match.group(4),
                password = match.group(5),
                # TODO: Apply business rules to this metadata - in our case we
                # need to track modified time (value as iso8601) in order to
                # manage evictions
                metadata = dict([
                    tuple(re.split(r":\s+", pair))
                    for pair in re.split(r",\s+", match.group(6).strip())
                ])
            )
        else:
            return cls(raw=raw, managed=False)


class PgPass:
    def __init__(self, filename):
        self._data = []
        self._filename = filename

    def read(self):
        with open(self._filename, 'r') as f:
            raw = f.read()
        for line in raw.split('\n'):
            self._data.append(PgPassLine(line))

    def write(self):
        with open(f"{self._filename}.stage", "w") as stage:
            for line in self._data:
                if line.managed:
                    comment = ", ".join([ f"{k}: {v}" for k, v in line.metadata.items() ])
                    raw = f"{line.host}:{line.port}:{line.db}:{line.username}:{line.password} # db_hooks {comment}\n"
                    stage.write(raw)
                else:
                    stage.write(f"{line.raw}\n")
            os.rename(filename, f"{self._filename}.bak")
            os.rename(stage.name, self._filename)
            os.chmod(self._filename, PERMISSIONS)

    def add(self, line):
        self._data.append(line)

    def evict(self):
        # TODO
