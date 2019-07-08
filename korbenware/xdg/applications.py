from collections import defaultdict
import os
import os.path

import attr
from twisted.python.failure import Failure
from xdg.BaseDirectory import load_data_paths

from korbenware.logger import create_logger
from korbenware.util.decorators import dictable, representable
from korbenware.xdg.executable import Executable


XDG_APPLICATIONS_DIRS = list(load_data_paths('applications'))


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


@representable
@dictable(['entries'])
class ApplicationSet:
    def __init__(self, log):
        self.log = log
        self.entries = []

    def add_entry(self, entry):
        self.entries.append(entry)

    def coalesce(self, *, skip_unparsed, skip_invalid):
        for entry in self.entries:
            executable = entry.executable
            parsed = executable.parsed and executable.exec_key_parsed
            valid = executable.validated

            if not executable.parsed:
                self.log.warn(
                    'Desktop file parse error while loading {filename}!',
                    filename=executable.filename,
                    log_failure=Failure(executable.parse_exc)
                )
            elif not executable.exec_key_parsed:
                self.log.warn(
                    'Exec key parse error while loading {filename}!',
                    filename=executable.filename,
                    log_failure=Failure(executable.exec_key_parse_exc)
                )

            if executable.parsed and not valid:
                self.log.debug(
                    'Desktop file validation issue while loading {filename}!',
                    filename=executable.filename,
                    log_failure=Failure(executable.validate_exc)
                )

            if (
                (not parsed and skip_unparsed)
                or
                (not valid and skip_invalid)
            ):
                self.log.info(
                    'Skipping loading {filename} due to loading issues',
                    filename=executable.filename
                )
                continue
            else:
                if not parsed:
                    self.log.warn(
                        'Loading {filename} despite parsing issues!',
                        filename=executable.filename
                    )

            return entry

        return None


def _load_application_dir(dirpath, log, cls):
    try:
        filenames = os.listdir(dirpath)
    except FileNotFoundError:
        return

    for filename in filenames:
        if filename.endswith('.desktop'):
            fullpath = os.path.join(dirpath, filename)

            log.debug(
                'Loading application desktop file {filename}',
                filename=fullpath
            )

            yield cls.from_path(fullpath)


def load_application_sets(dirs, log, cls=Application):
    entry_sets = defaultdict(lambda: ApplicationSet(log))

    for dirname in dirs:
        log.debug('Loading application directory {dirname}', dirname=dirname)

        for entry in _load_application_dir(dirname, log, cls):
            entry_sets[entry.filename].add_entry(entry)

    return entry_sets


@representable
@dictable([
    'directories',
    'entries'
])
class ApplicationsRegistry:
    log = create_logger()

    def __init__(self, config, key='applications', cls=Application):
        self.directories = getattr(config, key).directories
        self.entry_sets = load_application_sets(
            self.directories, self.log, cls
        )
        self.entries = dict()

        for filename, entry_set in self.entry_sets.items():
            entry = entry_set.coalesce(
                skip_unparsed=getattr(config, key).skip_unparsed,
                skip_invalid=getattr(config, key).skip_invalid
            )
            if entry:
                self.entries[filename] = entry
