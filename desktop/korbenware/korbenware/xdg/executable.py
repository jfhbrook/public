# Copyright 2020 Josh Holbrook
#
# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at https://mozilla.org/MPL/2.0/.

import os
import os.path
import shutil

import attr
from gshell import GShellError
from xdg.Exceptions import ParsingError, ValidationError
from xdg.DesktopEntry import DesktopEntry

from korbenware.presentation import representable
from korbenware.presentation.markdown import markdownable
from korbenware.xdg.exec_key import ExecKey


@markdownable
@representable
@attr.s
class Executable:
    filename = attr.ib()
    entry = attr.ib()
    parsed = attr.ib()
    parse_exc = attr.ib()
    validated = attr.ib()
    validate_exc = attr.ib()
    exec_key = attr.ib()
    exec_key_parsed = attr.ib()
    exec_key_parse_exc = attr.ib()

    @classmethod
    def from_path(cls, fullpath):
        filename = os.path.basename(fullpath)
        try:
            entry = DesktopEntry(fullpath)
            parsed = True
            parse_exc = None
        except ParsingError as exc:
            entry = None
            parsed = False
            parse_exc = exc

        return cls._construct(fullpath, filename, entry, parsed, parse_exc)

    @classmethod
    def from_desktop_entry(cls, entry):
        return cls._construct(getattr(entry, "filename", None), None, entry, True, None)

    @classmethod
    def _construct(cls, fullpath, filename, entry, parsed, parse_exc):
        """
        See: https://specifications.freedesktop.org/autostart-spec/autostart-spec-0.5.html#idm140434866991296
        """  # noqa

        if not parsed:
            validated = False
            validate_exc = None
            exec_key = None
            exec_key_parsed = False
            exec_key_parse_exc = None
        else:
            try:
                entry.validate()
                validated = True
                validate_exc = None
            except ValidationError as exc:
                validated = False
                validate_exc = exc

            exec_key = ExecKey(entry.getExec())

            try:
                exec_key.validate()
            except GShellError as exc:
                exec_key_parsed = False
                exec_key_parse_exc = exc
            else:
                exec_key_parsed = True
                exec_key_parse_exc = None

        return Executable(
            filename,
            entry,
            parsed,
            parse_exc,
            validated,
            validate_exc,
            exec_key,
            exec_key_parsed,
            exec_key_parse_exc,
        )

    @property
    def is_application(self):
        if self.parsed:
            return self.entry.getType() == "Application"
        else:
            return False

    @property
    def is_hidden(self):
        if self.parsed:
            return self.entry.getHidden()
        else:
            return True

    @property
    def no_display(self):
        if self.parsed:
            return self.entry.getNoDisplay()
        else:
            return False

    @property
    def only_show_in(self):
        if not self.parsed:
            return None
        return self.entry.getOnlyShowIn()

    @property
    def not_show_in(self):
        if not self.parsed:
            return None
        return self.entry.getNotShowIn()

    def should_show_in(self, show_in):
        if (
            (not self.parsed)
            or (self.only_show_in and self.not_show_in)
            or (show_in in self.not_show_in)
        ):
            return False

        if self.only_show_in and self.not_show_in:
            return False

        if show_in in self.not_show_in:
            return False

        if self.only_show_in:
            return show_in in self.only_show_in

        return True

    @property
    def dbus_activatable(self):
        if not self.parsed:
            return False

        return self.entry.get("DBusActivatable", type="boolean")

    @property
    def runtime_path(self):
        if not self.parsed:
            return None
        return self.entry.getPath() or None

    def passes_try_exec(self):
        if not self.parsed:
            return False

        try_exec = self.entry.getTryExec()

        if not try_exec:
            return True

        return bool(shutil.which(try_exec))
