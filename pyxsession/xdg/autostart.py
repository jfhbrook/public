from collections import defaultdict
import os
import os.path

import attr
from xdg.BaseDirectory import xdg_config_dirs

from pyxsession.util.decorators import dictable, representable
from pyxsession.xdg import config_basedir
from pyxsession.xdg.executable import Executable


XDG_AUTOSTART_DIRS = [
    os.path.join(base, 'autostart')
    for base in xdg_config_dirs
]


@representable
@attr.s
class AutostartEntry:
    fullpath = attr.ib()
    filename = attr.ib()
    executable = attr.ib()

    @classmethod
    def from_path(fullpath):
        """
        See: https://specifications.freedesktop.org/autostart-spec/autostart-spec-0.5.html#idm140434866991296
        """  # noqa

        filename = os.path.basename(fullpath)
        executable = Executable.from_path(fullpath)

        return AutostartEntry(fullpath, filename, executable)

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
class AutostartEntrySet:
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


def _load_autostart_dir(dirpath):
    try:
        filenames = os.listdir(dirpath)
    except FileNotFoundError as exc:
        # TODO: Logging
        print(exc)
        return

    for filename in filenames:
        yield AutostartEntry(os.path.join(dirpath, filename))


def _load_autostart(dirs):
    # Based on the logic described in:
    # https://specifications.freedesktop.org/autostart-spec/autostart-spec-0.5.html#idm140434866702736
    configuration_sets = defaultdict(AutostartEntrySet)

    for dirname in dirs:
        for entry in _load_autostart_dir(dirname):
            configuration_sets[entry.filename].add_entry(entry)

    return configuration_sets


@representable
@dictable([
    'directories',
    'environment_name',
    'all_files',
    'autostart_entries'
])
class AutostartConfiguration:
    def __init__(self, config):
        self.directories = config.autostart.directories
        self.environment_name = config.autostart.environment_name

        self.entry_sets = _load_autostart(self.directories)

        self.autostart_entries = dict()

        for filename, entry_set in self.entry_sets.items():
            entry = entry_set.coalesce(
                skip_unparsed=config.autostart.skip_unparsed,
                skip_invalid=config.autostart.skip_invalid
            )
            if entry.should_autostart(self.environment_name):
                self.autostart_entries[filename] = entry
