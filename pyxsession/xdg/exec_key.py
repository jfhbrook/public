import re
from gshell import g_shell_parse_argv


FIELD_CODE_RE = '(?<!%)(%\S)'


def expand_field_codes(raw, fields):
    fields = fields or dict()

    def get_field(match):
        field = match.group(0)
        return fields.get(field[1:], '')

    return re.sub(FIELD_CODE_RE, get_field, raw)


def get_field_codes(raw):
    return {
        match.group(0)[1:]
        for match in re.findall(FIELD_CODE_RE, raw)
    }


class ExecKey:
    def __init__(self, raw):
        self.raw = raw
        self._is_valid = None
        self._valid_exc = None

    def validate(self):
        if self._is_valid is None:
            try:
                g_shell_parse_argv(self.raw)
            except GShellError as exc:
                self._is_valid = False
                self._valid_exc = exc
                raise exc
            else:
                self._is_valid = True
        elif not self._is_valid:
            raise self._valid_exc
            
    def is_valid(self):
        if self._is_valid is None:
            try:
                self.validate()
            except GShellError:
                pass

        return self._is_valid

    def expected_fields(self):
        return {
            code
            for arg in g_shell_parse_argv(self.raw)
            for code in get_field_codes(arg)
        }

    def build_argv(self, fields=None):
        return [
            expand_field_codes(arg, fields)
            for arg in g_shell_parse_argv(self.raw)
        ]
