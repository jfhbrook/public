import os
import os.path
import shutil
from pyxsession.gshell import g_shell_parse_argv
from pyxsession.util.decorators import representable
from xdg.BaseDirectory import xdg_config_dirs
from xdg.Exceptions import ParsingError, ValidationError
from xdg.DesktopEntry import DesktopEntry

XDG_AUTOSTART_DIRS = [
    os.path.join(base, 'autostart')
    for base in xdg_config_dirs
]


@representable([
    'fullpath',
    'filename',
    'overrides',
    'entry',
    'parsed',
    'parse_exc',
    'validated',
    'validate_exc',
    'exec_parsed',
    'exec_parse_exc',
    'exec',
    'is_application',
    'is_hidden',
    'only_show_in',
    'not_show_in',
    'dbus_activatable',
    'runtime_path'
])
class AutostartEntry:
    def __init__(self, fullpath):
        """
        See: https://specifications.freedesktop.org/autostart-spec/autostart-spec-0.5.html#idm140434866991296
        """
        self.fullpath = fullpath
        self.filename = os.path.basename(fullpath)
        self.overrides = []

        try:
            self.entry = DesktopEntry(fullpath)
            self.parsed = True
        except ParsingError as exc:
            self.parsed = False
            self.parse_exc = exc
            self.validated = False
            self.exec_parsed = False
        else:
            try:
                self.entry.validate()
                self.validated = True
            except ValidationError as exc:
                self.validated = False
                self.validate_exc = exc

            try:
                # TODO: The freedesktop specification allows for %-encoded
                # substitution variables. This logic is based on what
                # xfce4-session does, which is use gshell's args parser.
                # It's believed that the gshell parser is a de facto
                # reference implementation for the rest of the rules and
                # likely that because of the lack of a use case for file
                # or url substitution that this is actually basically how
                # this works elsewhere.
                #
                # See also:
                # - https://specifications.freedesktop.org/desktop-entry-spec/desktop-entry-spec-latest.html#exec-variables
                # - https://github.com/xfce-mirror/xfce4-session/blob/0a915310582803296fbfb075e1ea1c045b20bfcc/xfce4-session/xfsm-global.c#L397
                # - https://github.com/xfce-mirror/libxfce4ui/blob/master/libxfce4ui/xfce-spawn.c#L564
                #
                # See the gshell module for more information.
                self.exec = g_shell_parse_argv(self.entry.getExec())
                self.exec_parsed = True
            except GShellError as exc:
                self.exec_parsed = False
                self.exec_parse_exc = exc

    def register_overridden_file(fullpath):
        self.overrides.append(fullpath)

    @property
    def is_application(self):
        if self.parsed:
            return self.entry.getType() == 'Application'
        else:
            return False

    @property
    def is_hidden(self):
        if self.parsed:
            return self.entry.getHidden()
        else:
            return True

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
            (not self.parsed) or
            (self.only_show_in and self.not_show_in) or
            (show_in in self.not_show_in)
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

        return self.entry.get('DBusActivatable', type='boolean')

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

    def should_autostart(self, environment_name):
        return all([
            self.parsed,
            self.is_application,
            self.exec_parsed,
            not self.is_hidden,
            not self.dbus_activatable,
            self.should_show_in(environment_name),
            self.passes_try_exec()
        ])


def _load_autostart_dir(dirpath):
    try:
        filenames = os.listdir(dirpath)
    except FileNotFoundError as exc:
        # TODO: Logging
        print(exc)
        return

    # TODO: Validate that only NotShowIn or OnlyShowIn is defined
    # NOTE: built in validation is too strict on its own but can be
    # used to get some ideas and conventions

    for filename in filenames:
        yield AutostartEntry(os.path.join(dirpath, filename))


def _load_autostart(dirs):
    # Based on the logic described in:
    # https://specifications.freedesktop.org/autostart-spec/autostart-spec-0.5.html#idm140434866702736
    desktop_files = dict()

    # With the understanding that these are in order of precedence
    for dirname in dirs:
        for entry in _load_autostart_dir(dirname):
            # Understanding is that topmost file takes precedence
            if entry.filename not in desktop_files:
                desktop_files[entry.filename] = entry
            else:
                # TODO: Right now an AutostartEntry can represent a
                # garbage file. In this case, should we delegate to the
                # overridden file?
                # TODO: Should we take the liberty of trying to parse the
                # backup file? Related question
                # TODO: Configurable?
                desktop_files[entry.filename].register_overridden_file(
                    entry.fullpath
                )

    return desktop_files


@representable([
    'directories',
    'environment_name',
    'all_files',
    'should_autostart'
])
class AutostartConfiguration:
    def __init__(
        self,
        directories=XDG_AUTOSTART_DIRS,
        environment_name='pyxsession'
    ):
        self.directories = directories
        self.environment_name = environment_name

        self.all_files = _load_autostart(directories)

        self.should_autostart = dict()

        for filename, entry in self.all_files.items():
            if entry.should_autostart(environment_name):
                self.should_autostart[filename] = entry
