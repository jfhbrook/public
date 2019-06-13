# Functions and code based on glib's gshell library
# See: https://github.com/GNOME/glib/blob/master/glib/gshell.c
# License: LGPL
#
# Missing functions:
# * unquote_string_inplace, ensure_token and delimit_token are all inlined
#   into their various call sites
# * g_shell_quote (just haven't needed it yet)


class GShellError(Exception):
    pass


class BadQuotingError(GShellError):
    pass


class EmptyStringError(GShellError):
    pass


def g_shell_unquote(quoted_string):
    unquoted = 0
    end = 0
    start = 0
    l = len(quoted_string)
    retval = ''

    # Lord forgive me for what I'm about to do...
    class UNQUOTED_STRING(Exception):
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
                    raise BadQuotingError(
                        "Quoted text doesn't begin with a quotation mark"
                    )

                s += 1

                if quote_char == '"':
                    while s < l:
                        if quoted_string[s] == '"':
                            s += 1
                            end = s

                            raise UNQUOTED_STRING(dest)

                        elif quoted_string[s] == '\\':
                            s += 1
                            if quoted_string[s] in '"\\`$\n':
                                dest += quoted_string[s]
                                s += 1
                            else:
                                dest += '\\'
                                s += 1
                        else:
                            dest += quoted_string[s]
                            s += 1
                else:
                    while s < l:
                        if quoted_string[s] == "'":
                            s += 1
                            end = s

                            raise UNQUOTED_STRING(dest)
                        else:
                            dest += quoted_string[s]
                            s += 1

                raise BadQuotingError('Unmatched quotation mark in command line or other shell quoted text')
            except UNQUOTED_STRING as exc:
                retval += exc.value
                start = end
            else:
                assert False, (
                    "It isn't supposed to be possible to reach this part of "
                    'the code'
                )

    return retval


def tokenize_command_line(command_line):
    current_quote = None
    current_token = None
    retval = []
    quoted = False

    l = len(command_line)
    i = 0

    while i < l:
        p = command_line[i]

        if current_quote == '\\':
            if p == '\n':
                pass
            else:
                current_token = current_token or ''
                current_token += '\\'
                current_token += p
            current_quote = None
        elif current_quote == '#':
            while i < l and command_line[i] != '\n':
                i += 1

            if i < l:
                p = command_line[i]
            current_quote = None

            if i >= l:
                break
        elif current_quote:
            if (
                (p == current_quote) and
                not ((current_quote == '"') and quoted)
            ):
                current_quote = None
            current_token = current_token or ''
            current_token += p
        else:
            if p == '\n':
                retval.append(current_token)
                current_token = None
            elif p in {' ', '\t'}:
                if current_token:
                    if current_token:
                        retval.append(current_token)
                        current_token = None
            elif p in {"'", '"', '\\'}:
                if p != '\\':
                    current_token = current_token or ''
                    current_token += p
                current_quote = p
            elif p == '#':
                if i == 0:
                    current_quote = p
                else:
                    prior = command_line[i-1]
                    if (
                        (prior == ' ') or
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

    if current_token is not None:
        retval.append(current_token)
    current_token = None

    if current_quote:
        if current_quote == '\\':
            raise BadQuotingError('Text ended just after a "\\" character.')
        else:
            raise BadQuotingError(
                f'Text ended before matching quote was found for '
                f'{current_quote}. (The text was "{command_line}")'
            )

    if not retval:
        raise EmptyStringError(
            'Text was empty (or contained only whitespace)'
        )

    return retval



def g_shell_parse_argv(command_line):
    return [
        g_shell_unquote(token)
        for token in tokenize_command_line(command_line)
    ]
