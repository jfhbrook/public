# Copyright 2020 Josh Holbrook
#
# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at https://mozilla.org/MPL/2.0/.

from collections import defaultdict
from functools import total_ordering
import os
import os.path

import attr
from twisted.python.failure import Failure
from xdg.BaseDirectory import load_data_paths

from korbenware.logger import create_logger
from korbenware.keys import keys
from korbenware.presentation import representable
from korbenware.presentation.markdown import markdownable
from korbenware.xdg.executable import Executable


XDG_APPLICATIONS_DIRS = list(load_data_paths("applications"))


@total_ordering
@markdownable
@representable
@attr.s(order=False)
class Application:
    fullpath = attr.ib()
    filename = attr.ib()
    executable = attr.ib()
    overrides = attr.ib(default=None)

    @classmethod
    def from_path(cls, fullpath):
        """
        See: https://specifications.freedesktop.org/autostart-spec/autostart-spec-0.5.html#idm140434866991296
        """  # noqa

        filename = os.path.basename(fullpath)
        executable = Executable.from_path(fullpath)

        return cls(fullpath, filename, executable)

    def __lt__(self, other):
        if self.executable.is_hidden == other.executable.is_hidden:
            if self.executable.no_display == other.executable.no_display:
                if self.filename == other.filename:
                    return self.fullpath < other.fullpath
                return self.filename < other.filename
            return self.executable.no_display < other.executable.no_display
        return self.executable.is_hidden < other.executable.is_hidden

    def __eq__(self, other):
        return (
            (self.fullpath == other.fullpath)
            and (self.executable.is_hidden == other.executable.is_hidden)
            and (self.executable.no_display == other.executable.no_display)
        )


@markdownable
@representable
@keys(["entries"])
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
                    "Desktop file parse error while loading {filename}!",
                    filename=executable.filename,
                    log_failure=Failure(executable.parse_exc),
                )
            elif not executable.exec_key_parsed:
                self.log.warn(
                    "Exec key parse error while loading {filename}!",
                    filename=executable.filename,
                    log_failure=Failure(executable.exec_key_parse_exc),
                )

            if executable.parsed and not valid:
                self.log.debug(
                    "Desktop file validation issue while loading {filename}!",
                    filename=executable.filename,
                    log_failure=Failure(executable.validate_exc),
                )

            if (not parsed and skip_unparsed) or (not valid and skip_invalid):
                self.log.info(
                    "Skipping loading {filename} due to loading issues",
                    filename=executable.filename,
                )
                continue
            else:
                if not parsed:
                    self.log.warn(
                        "Loading {filename} despite parsing issues!",
                        filename=executable.filename,
                    )

            entry.overrides = [
                overridden for overridden in self.entries if overridden != entry
            ]

            return entry

        return None


def _load_application_dir(dirpath, log, cls):
    try:
        filenames = os.listdir(dirpath)
    except FileNotFoundError:
        return

    for filename in filenames:
        if filename.endswith(".desktop"):
            fullpath = os.path.join(dirpath, filename)

            log.debug("Loading application desktop file {filename}", filename=fullpath)

            yield cls.from_path(fullpath)


def load_application_sets(dirs, log, cls=Application):
    entry_sets = defaultdict(lambda: ApplicationSet(log))

    for dirname in dirs:
        log.debug("Loading application directory {dirname}", dirname=dirname)

        for entry in _load_application_dir(dirname, log, cls):
            entry_sets[entry.filename].add_entry(entry)

    return entry_sets


@markdownable
@representable
@keys(["directories", "entries"])
class ApplicationsRegistry:
    log = create_logger()

    def __init__(self, config, key="applications", cls=Application):
        self.directories = getattr(config, key).directories
        self.entry_sets = load_application_sets(self.directories, self.log, cls)
        self.entries = dict()

        for filename, entry_set in self.entry_sets.items():
            entry = entry_set.coalesce(
                skip_unparsed=getattr(config, key).skip_unparsed,
                skip_invalid=getattr(config, key).skip_invalid,
            )
            if entry:
                self.entries[filename] = entry