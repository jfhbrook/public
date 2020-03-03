import datetime
import dateutil.parser
import logging
import os
import os.path
import re
import stat

import arrow
import attr
from terminaltables import SingleTable as Table

from db_hooks.password import PasswordLoader

PERMISSIONS = stat.S_IRUSR | stat.S_IWUSR

PGPASS_PROTOCOLS = {"postgres", "postgresql", "pg"}

logger = logging.getLogger(__name__)


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
    def create(cls, host, port, database, username, password, connection_name=None):
        metadata = dict(modified=datetime.datetime.utcnow())

        if connection_name:
            metadata["name"] = connection_name

        return cls(
            raw=None,
            managed=True,
            host=host,
            port=port,
            database=database,
            username=username,
            password=password,
            metadata=metadata,
        )

    @classmethod
    def from_config(cls, name, config):
        connection_config = config.connections[name]
        return cls.create(
            connection_config.host,
            connection_config.port,
            connection_config.database,
            connection_config.username,
            connection_config.password,
            name,
        )

    def touch(self):
        self.metadata["modified"] = datetime.datetime.utcnow()

    def stringify(self):
        if self.managed:
            comment = ", ".join(
                [
                    f"{k}: {v}"
                    for k, v in [
                        _dehydrate_metadata_kv(k, v) for k, v in self.metadata.items()
                    ]
                ]
            )

            raw = ":".join(
                [
                    self.host,
                    str(self.port),
                    self.database,
                    self.username,
                    f"{self.password} # db_hooks {comment}",
                ]
            )
        else:
            raw = self.raw
        return raw

    @property
    def pgpass_key(self):
        if self.managed:
            return ":".join([self.host, str(self.port), self.database, self.username])
        # Try to print everything prior to the password at least
        match = re.match(r"^([^:]+?:[^:]+?:[^:]+?:[^:]+?):", self.raw.strip())
        if match:
            return match.group(1)
        else:
            # Fall back to the actual raw value
            return self.raw.strip()

    @property
    def name(self):
        if self.managed and self.metadata and "name" in self.metadata:
            return self.metadata["name"]
        return None

    @property
    def age(self):
        # Kinda a joke default :)
        modified = datetime.datetime.fromtimestamp(0)

        if self.managed and "modified" in self.metadata:
            modified = self.metadata["modified"]

        return datetime.datetime.utcnow() - modified

    @property
    def human_age(self):
        modified = datetime.datetime.fromtimestamp(0)

        if self.managed and "modified" in self.metadata:
            modified = self.metadata["modified"]

        return arrow.get(modified).humanize()

    def load_password(self, config):
        connection_config = config.connections[self.name]
        loader = PasswordLoader.from_config(config)
        password = (
            loader.get_password(self.name)
            if connection_config.password is None
            else connection_config.password
        )

        self.password = password


class PgPass:
    def __init__(self, filename, ttl=600, clear_backup=True):
        self._data = []
        self._filename = filename
        self._clear_backup = clear_backup
        self.ttl = ttl

    def read(self):
        logger.info(f"Reading {self._filename}...")
        with open(self._filename, "r") as f:
            raw = f.read()
        for line in raw.split("\n"):
            if line:
                self._data.append(PgPassEntry.parse(line))

    @classmethod
    def from_config(cls, config):
        self = cls(
            config.pgpass.location, config.pgpass.ttl, config.pgpass.clear_backup
        )
        self.read()
        return self

    def write(self):
        logger.info(f"Writing {self._filename}...")
        with open(f"{self._filename}.stage", "w") as stage:
            for entry in self._data:
                stage.write(f"{entry.stringify()}\n")
            os.rename(self._filename, f"{self._filename}.bak")
            os.rename(stage.name, self._filename)
            if os.name != "nt":
                os.chmod(self._filename, PERMISSIONS)
            if self._clear_backup:
                os.remove(f"{self._filename}.bak")
        logger.debug(f"Finished writing to {self._filename}.")

    def get_entry(self, name, config):
        # O(n) but likely to not be many of these so shrug
        for entry in self._data:
            if entry.name == name:
                return entry
        entry = PgPassEntry.from_config(name, config)

        self._data.append(entry)

        return entry

    def add(self, pg_pass_entry):
        logger.debug(
            f"Adding {pg_pass_entry.name} ({pg_pass_entry.pgpass_key}) to pgpass..."
        )
        self._data.append(pg_pass_entry)

    def evict(self, ttl=None):
        if not ttl:
            ttl = self.ttl

        logger.info(f"Evicting managed entries in pgpass older than {ttl} seconds...")

        self._data = [
            entry
            for entry in self._data
            if (
                (not entry.managed)
                or ("modified" in getattr(entry, "metadata", dict()))
                and (
                    entry.metadata["modified"]
                    > (datetime.datetime.utcnow() - datetime.timedelta(seconds=ttl))
                )
            )
        ]

    def clear(self):
        logger.info(f"Clearing all managed entries from pgpass...")
        self._data = [entry for entry in self._data if not entry.managed]

    def show(self):
        table = Table(
            [["connection name", "pgpass key", "managed", "age"]]
            + [
                [
                    entry.pgpass_key or "<unknown>",
                    entry.name or "<n/a>",
                    entry.managed,
                    entry.human_age,
                ]
                for entry in self._data
            ]
        )
        print(table.table)
