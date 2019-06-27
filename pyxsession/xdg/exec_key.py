import re
from gshell import g_shell_parse_argv


FIELD_CODE_RE = '(?<!%)(%\S)'


def expand_field_codes(raw, fields):
    fields = fields or dict()

    def get_field(match):
        field = match.group(0)
        return fields.get(field[1:], field)

    return re.sub(FIELD_CODE_RE, get_field, raw)


def get_field_codes(raw):
    return {
        match.group(0)[1:]
        for match in re.findall(FIELD_CODE_RE, raw)
    }


class ExecKey:
    def __init__(self, raw):
        self.raw = raw

    def validate(self):
        g_shell_parse_argv(self.raw)

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
