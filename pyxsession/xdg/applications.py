from collections import defaultdict
import os
import os.path

import attr

from pyxsession.util.decorators import dictable, representable
from pyxsession.xdg import config_basedir
from pyxsession.xdg.executable import Executable


@representable
@attr.s
class Application:
    fullpath = attr.ib()
    filename = attr.ib()
    executable = attr.ib()

    @classmethod
    def from_path(cls, fullpath):
        """
        See: https://specifications.freedesktop.org/autostart-spec/autostart-spec-0.5.html#idm140434866991296
        """  # noqa

        filename = os.path.basename(fullpath)
        executable = Executable.from_path(fullpath)

        return cls(fullpath, filename, executable)

    def should_autostart(self, environment_name):
        return all([
            self.executable.parsed,
            self.executable.is_application,
            self.executable.exec_parsed,
            not self.executable.is_hidden,
            not self.executable.dbus_activatable,
            self.executable.should_show_in(environment_name),
            self.executable.passes_try_exec()
        ])


@representable
@dictable(['entries'])
class ApplicationSet:
    def __init__(self):
        self.entries = []

    def add_entry(self, entry):
        self.entries.append(entry)

    def coalesce(self, *, skip_unparsed, skip_invalid):
        for entry in self.entries:
            executable = entry.executable
            parsed = executable.parsed and executable.exec_parsed
            valid = executable.validated

            if (
                (not parsed and skip_unparsed)
                or
                (not valid and skip_invalid)
            ):
                continue

            return entry

        return None


def _load_application_dir(dirpath, cls):
    try:
        filenames = os.listdir(dirpath)
    except FileNotFoundError as exc:
        # TODO: Logging
        print(exc)
        return

    for filename in filenames:
        yield cls(os.path.join(dirpath, filename))


def load_application_sets(dirs, cls=Application):
    entry_sets = defaultdict(ApplicationSet)

    for dirname in dirs:
        for entry in _load_application_dir(dirname, cls):
            entry_sets[entry.filename].add_entry(entry)

    return entry_sets


@representable
@dictable([
    'directories',
    'entries'
])
class ApplicationDatabase:
    def __init__(self, config, key='applications', cls=Application):
        self.directories = getattr(config, key).directories
        self.entry_sets = load_application_sets(self.directories, cls)
        self.entries = dict()

        for filename, app_set in self.entry_sets.items():
            entry = entry_set.coalesce(
                skip_unparsed=getattr(config, key).skip_unparsed,
                skip_invalid=getattr(config, key).skip_invalid
            )
            if entry:
                self.entries[filename] = entry
