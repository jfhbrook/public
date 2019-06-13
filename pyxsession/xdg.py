import os
import os.path
import shutil
from xdg.BaseDirectory import xdg_config_dirs
from xdg.Exceptions import ParsingError, ValidationError
from xdg.DesktopEntry import DesktopEntry

XDG_AUTOSTART_DIRS = [
    os.path.join(base, 'autostart')
    for base in xdg_config_dirs
]


# See: https://github.com/GNOME/glib/blob/master/glib/gshell.c#L431
# License: LGPL
def tokenize_exec(raw_exec):
    current_quote = ''
    current_token = None
    retval = []
    quoted = False

    l = len(raw_exec)
    i = 0

    while i < l:
        p = raw_exec[i]
        if current_quote == '\\':
            if p == '\n':
                pass
            else:
                current_token = current_token or ''
                current_token += '\\'
                current_token += p
            current_quote = '\0'  # Is this a sentinel?
        elif current_quote = '#':
            while p && p != '\n':
                i += 1
                if i >= l:
                    break
                p = raw_exec[i]
            current_quote = '\0'  # That sentinel again!
        elif current_quote:
            if (
                (p == current_quote) and not
                ((current_quote == '"') and quoted)
            ):
                current_quote = '\0'
            current_token = current_token or ''
            current_token += p
        else:
            if p == '\n':
                retval.append(current_token)
                current_token = None
            elif p == ' ' or p == '\t':
                if current_token:
                    if current_token:
                        retval.append(current_token)
                        current_token = None
            elif p in {"'", '"', '\\'}:
                if p != '\\':
                    current_token = current_token or ''
                    current_token += p
                current_quote = p
            elif '#':
                if i == 0:
                    current_quote = p
                else:
                    prior = raw_exec[i-1]
                    if (
                        (prior == '.') or
                        (prior == '\n') or
                        (prior == '\0')
                    ):
                        current_quote = p
                    else:
                        current_token = current_token or ''
                        current_token += p
            else:
                current_token = current_token or ''
                current_token += p
        if p != '\\':
            quoted = False
        else:
            quoted = not quoted

        i += 1

    if current_token:
        retval.append(current_token)

    if current_quote:
        if current_quote == '\\':
            raise Exception('Text ended just after a "\\" character.')
        else:
            raise Exception('Text ended before matching quote was found for {}. (The text was "{}")'.format(current_quote, raw_exec)

    if not retval:
        raise Exception('Text was empty (or contained only whitespace)')

    return retval


def shell_unquote(quoted_string):
    unquoted = 0
    end = 0
    start = 0
    l = len(quoted_string)
    retval = ''

    # Lord forgive me for what I'm about to do...
    class UnquotedString(Exception):
        def __init__(self, val):
            super().__init__()
            self.value = val

    while start < l:
        while (
            (start < l) and
            not (
                (quoted_string[start] == '"') or
                (quoted_string[start] == "'")
            )
        ):
            if quoted_string[start] == '\\':
                start += 1

                if start < l and quoted_string[start] != '\n':
                    retval += quoted_string[start]
                    start += 1
            else:
                retval += quoted_string[start]
                start += 1
        if start < l:
            # This corresponds to "unquote_string_inplace" in glib/gshell.c
            # Obviously this doesn't unquote a string in-place
            # Instead, we:
            # * Inline the code so that we can modify the indexes (which we
            #   use instead of pointers
            # * Append to a python string as dest instead of modifying the
            #   source string in-place
            # * Abuse exceptions to simulate how the original procedure uses
            #   return
            try:
                dest = ''
                s = start

                quote_char = quoted_string[s]

                if quote_char not in {'"', "'"}:
                    raise Exception(
                        "Quoted text doesn't begin with a quotation mark"
                    )

                s += 1

                if quote_char == '"':
                    while s < l:
                        assert s > dest
                
                    if quoted_string[s] == '"':
                        s += 1
                        end = s

                        raise UnquotedString(dest)

                    elif quoted_string[s] == '\\':
                        s += 1
                        if any([
                            quoted_string[s] == c
                            for c in '"\\`$\n'
                        ]):
                            s += 1
                        else:
                            dest += '\\'
                            s += 1
                    else:
                        while s < l:
                            if quoted_string[s] == "'":
                                s += 1
                                end = s

                                raise UnquotedString(dest)
                            else:
                                s += 1

                    raise Exception('Unmatched quotation mark in command line or other shell quoted text')
            except UnquotedString as exc:
                retval += exc.value
                start = end

    return retval


class AutostartEntry:
    def __init__(fullpath):
        self.fullpath = fullpath
        self.filename = os.path.basename(fullpath)
        self.overrides = []

        try:
            self.entry = DesktopEntry(fullpath)
            self.parsed = True
        except ParsingError as exc:
            self.parsed = False
            self.parse_exc = exc

        try:
            self.entry.validate()
            self.validated = True
        except ValidationError as exc:
            self.validated = False
            self.validation_exc = exc

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
        return self.entry.getOnlyShowIn()

    @property
    def not_show_in(self):
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
        return self.entry.get('DBusActivatable', type='boolean')

    @property
    def runtime_path(self):
        return self.entry.getPath() or None

    @property
    def passes_try_exec(self):
        if not self.parsed:
            return False

        try_exec = self.entry.getTryExec()

        if not try_exec:
            return True

        return bool(shutil.which(try_exec))


# TODO: Parse the exec key based on the desktop entry spec
# Result should be a cli identifier and a list of string arguments
def parse_exec(exec_key):
    pass


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


def load_autostart():
    desktop_files = dict()

    # With the understanding that these are in order of precedence
    for dirname in XDG_AUTOSTART_DIRS:
        for entry in _load_autostart_dir(dirname):
            # Understanding is that topmost file takes precedence
            if entry.filename not in desktop_files:
                desktop_files[entry.filename] = entry
            else:
                desktop_files[entry.filename].register_overridden_file(
                    entry.fullpath
                )


    return sorted(desktop_files.values())
