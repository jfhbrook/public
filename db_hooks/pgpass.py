import datetime
import dateutil.parser
import os
import os.path
import re
import stat

import attr
from terminaltables import SingleTable as Table

PERMISSIONS = stat.S_IRUSR | stat.S_IWUSR

PGPASS_PROTOCOLS = {"postgres", "postgresql", "pg"}


def is_pgpass_protocol(protocol):
    return protocol in PGPASS_PROTOCOLS


def pg_pass_file():
    if os.name == "nt":
        return os.path.join(os.getenv("APPDATA"), "postgresql", "pgpass.conf")
    return os.path.expanduser("~/.pgpass")


def _hydrate_metadata_kv(k, v):
    if k in {"modified"}:
        return k, dateutil.parser.isoparse(v)
    return k, v


def _dehydrate_metadata_kv(k, v):
    if k in {"modified"}:
        return k, v.isoformat()
    return k, v


@attr.s
class PgPassEntry:
    raw = attr.ib()
    managed = attr.ib(default=False)
    host = attr.ib(default=None)
    port = attr.ib(default=None)
    database = attr.ib(default=None)
    username = attr.ib(default=None)
    password = attr.ib(default=None)
    metadata = attr.ib(default=attr.Factory(dict))

    @classmethod
    def parse(cls, raw):
        match = re.match(
            r"^([^:]+?):([^:]+?):([^:]+?):([^:]+?):([^:]+?)\s+#\s+db_hooks\s+(.*)",
            raw.strip(),
        )
        if match:
            metadata = dict(
                [
                    _hydrate_metadata_kv(*tuple(re.split(r":\s+", pair)))
                    for pair in re.split(r",\s+", match.group(6).strip())
                ]
            )

            return cls(
                raw=raw,
                managed=True,
                host=match.group(1),
                port=int(match.group(2)),
                database=match.group(3),
                username=match.group(4),
                password=match.group(5),
                metadata=metadata,
            )
        else:
            return cls(raw=raw, managed=False)

    @classmethod
    def create(cls, host, port, database, username, password):
        return cls(
            raw=None,
            managed=True,
            host=host,
            port=port,
            database=database,
            username=username,
            password=password,
            metadata=dict(modified=datetime.datetime.now()),
        )

    def stringify(self):
        if self.managed:
            comment = ", ".join(
                [
                    f"{k}: {v}"
                    for k, v in [
                        _dehydrate_metadata_kv(kv) for kv in self.metadata.items()
                    ]
                ]
            )
            raw = ":".join(
                [
                    self.host,
                    self.port,
                    self.db,
                    self.username,
                    f"{self.password} # db_hooks {comment}",
                ]
            )
        else:
            raw = self.raw
        return raw

    @property
    def name(self):
        if self.managed:
            return ":".join(
                self.host,
                self.port,
                self.db,
                self.username
            )
        else:
            # Try to print everything prior to the password at least
            match = re.match(r"^([^:]+?:[^:]+?:[^:]+?:[^:]+?):", self.raw.strip())
            if match:
                return match.group(1)
            else:
                # Fall back to the actual raw value
                return self.raw.strip()

    @property
    def age(self):
        # Kinda a joke default :)
        modified = datetime.datetime.fromtimestamp(0)

        if self.managed and 'modified' in self.metadata:
            modified = self.metadata['modified']

        return datetime.datetime.now() - modified


class PgPass:
    def __init__(self, filename, ttl=600, clear_backup=True):
        self._data = []
        self._filename = filename
        self._clear_backup = clear_backup
        self.ttl = ttl

    def read(self):
        with open(self._filename, "r") as f:
            raw = f.read()
        for line in raw.split("\n"):
            if line:
                self._data.append(PgPassEntry.parse(line))

    @classmethod
    def from_config(cls, config):
        self = cls(
            config.pgpass.location,
            config.pgpass.ttl,
            config.pgpass.clear_backup
        )
        self.read()
        return self

    def write(self):
        with open(f"{self._filename}.stage", "w") as stage:
            for entry in self._data:
                stage.write(f"{entry.stringify()}\n")
            os.rename(self._filename, f"{self._filename}.bak")
            os.rename(stage.name, self._filename)
            if os.name != "nt":
                os.chmod(self._filename, PERMISSIONS)
            if self._clear_backup:
                os.remove(f"{self._filename}.bak")

    def add(self, pg_pass_line):
        self._data.append(pg_pass_line)

    def evict(self):
        self._data = [
            entry
            for entry in self._data
            if (
                (not entry.managed)
                or ("modified" in getattr(entry, "metadata", dict()))
                and (
                    entry.metadata["modified"]
                    < (datetime.datetime.now() - datetime.timedelta(self.ttl))
                )
            )
        ]

    def clear(self):
        self._data = [entry for entry in self._data if not entry.managed]

    def show(self):
        print(Table([
            ["entry", "managed", "age (s)"]
        ] + [
            [entry.name, entry.managed, entry.age]
            for entry in self._data
        ]).table)
