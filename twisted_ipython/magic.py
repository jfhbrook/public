import re
from textwrap import dedent, indent

from IPython import get_ipython
from IPython.core import magic_arguments
from IPython.core.magic import (
    cell_magic, line_magic, Magics, magics_class
)

import twisted_ipython.config as config
from twisted_ipython.async_runner import twisted_runner


def install_autoawait(ipython):
    ipython.loop_runner_map['twisted'] = (twisted_runner, True)


def _detect_indentation(cell):
    for line in cell.split('\n'):
        m = re.match(r'^(\s+)\S+', line)

        if m:
            return m.group(0)

    return '    '


class ConfigError(Exception):
    pass


@magics_class
class TwistedMagics(Magics):

    @magic_arguments.magic_arguments()
    @magic_arguments.argument(
        'key', type=str
    )
    @magic_arguments.argument(
        'value', type=str, nargs='*'
    )
    @line_magic
    def crochet_config(self, line):
        """
        Configure settings for Crochet_:

        - *timeout*: How long to wait for autoawaited twisted code to run
          before canceling, in seconds. Defaults to 60. Crochet uses ``2**31``
          internally as a "basically infinity" constant, if you would like
          this limitation to just go away and leave you alone.

        Examples::

            # Show the current config
            %crochet_config show

            %crochet_config set timeout 5
        """
        args = magic_arguments.parse_argstring(self.crochet_config, line)

        SETTINGS = dict(
            timeout=60
        )

        if args.key == 'show':
            print('# Crochet settings:')
            for key in SETTINGS.keys():
                print(
                    ' - {key}={value}'.format(
                        key=key, value=getattr(config, key)
                    )
                )
        elif args.key == 'reset':
            print('# Resetting Crochet settings to their defaults:')
            for key, value in SETTINGS.items():
                setattr(config, key, value)
                print(' - {key}={value}'.format(key=key, value=value))
        elif args.key in SETTINGS:
            assert len(args.value) == 1, (
                'Can only set a config setting to a single value!'
            )
            print('Setting {} to {}!'.format(args.key, args.value[0]))
            setattr(
                config,
                args.key,
                type(getattr(config, args.key))(args.value[0])
            )
        else:
            raise ConfigError(
                'May either call "show", "reset" or "<key> <value>"'
            )

    @magic_arguments.magic_arguments()
    @magic_arguments.argument(
        'assign',
        type=str, nargs='*', default='_'
    )
    @cell_magic
    def run_in_reactor(self, line, cell):
        """
        Run the contents of the cell using run_in_reactor_.

        When this magic is enabled, the cell will get rewritten to::

            import crochet

            def _cell():
                # Your code here

            @crochet.run_in_reactor
            def _run_in_reactor():
                return _cell()

            _ = _run_in_reactor()
            _

        ``_run_in_reactor`` returns an EventualResult_. The name of the
        variable that this value gets assigned to can be set as an
        argument. For instance::

            %run_in_reactor result

            result.wait(5)

        For more information, see the documentation for crochet_.

        .. _run_in_reactor: https://crochet.readthedocs.io/en/stable/api.html#run-in-reactor-asynchronous-results
        .. _EventualResult: https://crochet.readthedocs.io/en/stable/api-reference.html#crochet.EventualResult
        .. _crochet: https://crochet.readthedocs.io/en/stable/index.html
        """  # noqa

        args = magic_arguments.parse_argstring(self.run_in_reactor, line)

        ipython = get_ipython()

        indentation = _detect_indentation(cell)

        new_cell = (
            dedent('''
                import crochet


                def _cell():
            ''') +
            indent(cell, indentation) +
            dedent('''
                @crochet.run_in_reactor
                def _run_in_reactor():
                {indent}return _cell()
                {assign} = _run_in_reactor()
                {assign}
            ''').format(
                indent=indentation,
                assign=args.assign[0] if args.assign else '_'
            )
        )

        ipython.run_cell(new_cell)
