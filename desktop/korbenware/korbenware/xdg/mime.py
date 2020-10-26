# Copyright 2020 Josh Holbrook
#
# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at https://mozilla.org/MPL/2.0/.

import os.path

import attr
from twisted.python.failure import Failure
from xdg.BaseDirectory import xdg_config_dirs
from xdg.IniFile import IniFile
from xdg.Exceptions import ParsingError
from xdg.Mime import MIMEtype, get_type2 as get_type

from korbenware.logger import create_logger
from korbenware.keys import keys
from korbenware.presentation import representable
from korbenware.presentation.markdown import markdownable
from korbenware.xdg.applications import XDG_APPLICATIONS_DIRS

# By far the most complete information on how this works can be found via
# this arch wiki link:
#
# https://wiki.archlinux.org/index.php/XDG_MIME_Applications

XDG_MIMEAPPS_DIRS = xdg_config_dirs + [
    "/usr/local/share/applications",
    "/usr/share/applications",
]

XDG_MIMEINFO_CACHE_FILES = [
    os.path.join(directory, "mimeinfo.cache") for directory in XDG_APPLICATIONS_DIRS
]


def xdg_mimeapps_files(environment=None):
    for directory in xdg_config_dirs:
        filenames = [f"{environment}-mimeapps.list"] if environment else []
        filenames.append("mimeapps.list")

        for filename in filenames:
            yield os.path.join(directory, filename)


def _get_group(ini_file, group):
    if not ini_file:
        return dict()

    return {
        MIMEtype(mime_type): [app for app in apps.split(";") if app]
        for mime_type, apps in ini_file.content.get(group, dict()).items()
    }


@markdownable
@representable
@attr.s
class MimeAppsList:
    filename = attr.ib()
    ini_file = attr.ib()
    parsed = attr.ib()
    parse_exc = attr.ib()

    def get_added_associations(self):
        return _get_group(self.ini_file, "Added Associations")

    def get_removed_associations(self):
        return _get_group(self.ini_file, "Removed Associations")

    def get_default_applications(self):
        return _get_group(self.ini_file, "Default Applications")


def load_xdg_mime_lists(environment=None):
    for filename in xdg_mimeapps_files(environment):
        if os.path.isfile(filename):
            try:
                ini_file = IniFile()
                ini_file.parse(filename)
            except ParsingError as exc:
                yield MimeAppsList(filename, None, False, exc)
            else:
                yield MimeAppsList(filename, ini_file, True, None)


def _insert(mimetype, apps, target):
    if mimetype not in target:
        target[mimetype] = set(apps)
    else:
        for app in apps:
            target[mimetype].add(app)


def _remove(mimetype, apps, target):
    if mimetype not in target:
        return

    for app in apps:
        target[mimetype].remove(app)

    if not target[mimetype]:
        del target[mimetype]


@markdownable
@representable
@attr.s
class DesktopDatabase:
    filename = attr.ib()
    ini_file = attr.ib()
    parsed = attr.ib()
    parse_exc = attr.ib()

    _cache = None

    @classmethod
    def from_file(cls, filename, log=None):
        ini_file = IniFile()
        try:
            ini_file.parse(filename)
        except ParsingError as exc:
            ini_file = None
            parsed = False
            parse_exc = exc
        else:
            parsed = True
            parse_exc = None

        return cls(
            filename=filename, ini_file=ini_file, parsed=parsed, parse_exc=parse_exc
        )

    def items(self):
        if not self._cache:
            self._cache = _get_group(self.ini_file, "MIME Cache")
        yield from self._cache.items()


@markdownable
@representable
@keys(["environment", "lookup", "defaults"])
class MimeRegistry:
    log = create_logger()

    def __init__(self, config, applications):
        self.environment = config.mime.environment
        self.applications = applications
        self.lookup = dict()
        self.defaults = dict()

        for filename in XDG_MIMEINFO_CACHE_FILES:
            self.log.debug(
                "Loading desktop mimeinfo database {filename}", filename=filename
            )
            database = DesktopDatabase.from_file(filename)

            if not database.parsed:
                self.log.warn(
                    "INI file parse error while loading mimeinfo database {filename} - skipping!",  # noqa
                    filename=filename,
                    log_failure=Failure(database.parse_exc),
                )
            else:
                for mimetype, apps in database.items():
                    self.log.debug(
                        "Associating applications {applications} with mimetype {mimetype}...",  # noqa
                        mimetype=mimetype,
                        applications=apps,
                    )
                    _insert(mimetype, apps, self.lookup)

        # TODO: Alternate algorithm that doesn't require reversing?
        # The list is short so it's not a big deal
        for mime_list in reversed(
            list(load_xdg_mime_lists(environment=self.environment))
        ):
            if mime_list.parsed:
                added_associations = mime_list.get_added_associations()
                for mimetype, apps in added_associations.items():
                    self.log.debug(
                        "Associating applications {applications} with mimetype {mimetype}...",  # noqa
                        mimetype=mimetype,
                        applications=apps,
                    )
                    _insert(mimetype, apps, self.lookup)

                removed_associations = mime_list.get_removed_associations()
                for mimetype, apps in removed_associations.items():
                    self.log.debug(
                        "Disassociating applications {applications} from mimetype {mimetype}...",  # noqa
                        mimetype=mimetype,
                        applications=apps,
                    )
                    _remove(mimetype, apps, self.lookup)

                    # Assumption is that if the mimetype is removed that we
                    # don't want an associated default application either.
                    #
                    # I could change my mind on this.
                    if mimetype in self.defaults:
                        to_remove = {
                            app for app in apps if app in self.defaults[mimetype]
                        }
                        if to_remove:
                            self.log.debug(
                                "Removing applications {applications} as defaults from mimetype {mimetype}...",  # noqa
                                mimetype=mimetype,
                                applications=list(to_remove),
                            )
                        for removed_app in to_remove:
                            self.defaults[mimetype] = [
                                app
                                for app in self.defaults[mimetype]
                                if app is not removed_app
                            ]

                default_applications = mime_list.get_default_applications()

                for mimetype, apps in default_applications.items():
                    self.log.debug(
                        "Registering applications {applications} as the defaults for mimetype {mimetype}...",  # noqa
                        mimetype=mimetype,
                        applications=apps,
                    )
                    _insert(mimetype, apps, self.lookup)

                    # Current assumption is that an override should override
                    # the entire key.
                    #
                    # I could change my mind on this.
                    self.defaults[mimetype] = apps
            else:
                self.log.warn(
                    "Parse issues while loading mimeapp list at {filename} - skipping!",  # noqa
                    filename=mime_list.filename,
                    log_failure=Failure(mime_list.parse_exc),
                )

    def applications_by_filename(self, filename):
        return [
            self.applications.entries[key]
            for key in self.lookup[get_type(filename)]
            if key in self.applications.entries
        ]

    def default_by_filename(self, filename):
        return [
            self.applications.entries[key]
            for key in self.defaults[get_type(filename)]
            if key in self.applications.entries
        ]
