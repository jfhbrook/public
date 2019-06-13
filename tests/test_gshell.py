# A port of relevant gshell tests from glib
# See https://github.com/GNOME/glib/blob/master/glib/tests/shell.c
# Licence: LGPL

import pytest

from pyxsession.gshell import g_shell_parse_argv, g_shell_unquote
from pyxsession.gshell import EmptyStringError, BadQuotingError

@pytest.mark.parametrize('cmdline,argv,exc_cls', [
    ('foo bar', ['foo', 'bar'], None),
    ("foo 'bar'", ['foo', 'bar'], None),
    ('foo "bar"', ['foo', 'bar'], None),
    ("foo '' 'bar'", ['foo', '', 'bar'], None),
    (
        "foo \"bar\"'baz'blah'foo'\\''blah'\"boo\"",
        [
            'foo',
            "barbazblahfoo'blahboo"
        ],
        None
    ),
    (
        'foo \t \tblah\tfoo\t\tbar  baz',
        ['foo', 'blah', 'foo', 'bar', 'baz'],
        None
    ),
    (
        "foo '    spaces more spaces lots of     spaces in this   '  \t",
        ['foo', '    spaces more spaces lots of     spaces in this   '],
        None
    ),
    ('foo \\\nbar', ['foo', 'bar'], None),
    ("foo '' ''", ['foo', '', ''], None),
    ("foo \\\" la la la", ['foo', '"', 'la', 'la', 'la'], None),
    ('foo \\ foo woo woo\\ ', ['foo', ' foo', 'woo', 'woo '], None),
    ('foo "yada yada \\$\\""', ['foo', 'yada yada $"'], None),
    ('foo "c:\\\\"', ['foo', 'c:\\'], None),
    ('foo # bla bla bla\n bar', ['foo', 'bar'], None),
    ('foo a#b', ['foo', 'a#b'], None),
    ('#foo', None, EmptyStringError),
    ('foo bar \\', None, BadQuotingError),
    ("foo 'bar baz", None, BadQuotingError),
    ('foo \'"bar" baz', None, BadQuotingError),
    ('', None, EmptyStringError),
    ('  ', None, EmptyStringError),
    ('# foo bar', None, EmptyStringError),
    (
        "foo '/bar/summer'\\''09 tours.pdf'",
        ['foo', "/bar/summer'09 tours.pdf"],
        None
    )
])
def test_cmdline(cmdline, argv, exc_cls):
    if exc_cls:
        with pytest.raises(exc_cls):
            res = g_shell_parse_argv(cmdline)
    else:
        res = g_shell_parse_argv(cmdline)

        assert res == argv


@pytest.mark.parametrize('in_,out,exc_cls', [
    ('', '', None),
    ('a', 'a', None),
    ("'a'", 'a', None),
    ("'('", '(', None),
    ("''\\'''", "'", None),
    ("''\\''a'", "'a", None),
    ("'a'\\'''", "a'", None),
    ("'a'\\''a'", "a'a", None),
    ("\\\\", "\\", None),
    ("\\\n", "", None),
    ("'\\''", None, BadQuotingError),
    ( "\"\\\"\"", "\"", None),
    ('"', None, BadQuotingError),
    ("'", None, BadQuotingError),
    ("\x22\\\\\"", "\\", None),
    ("\x22\\`\"", "`", None),
    ("\x22\\$\"", "$", None),
    ("\x22\\\n\"", "\n", None),

    # These three fail!
    # "\'" -> \'
    ("\"\\'\"", "\\'", None),
    # "\[carriage return]" -> \[carriage return]
    ("\x22\\\r\"", "\\\r", None),
    # "\n" -> \n
    ("\x22\\n\"", "\\n", None)
])
def test_unquote(in_, out, exc_cls):
    if exc_cls:
        with pytest.raises(exc_cls):
            res = g_shell_unquote(in_)
    else:
        res = g_shell_unquote(in_)
        assert res == out
