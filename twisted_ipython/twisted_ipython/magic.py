import re
from textwrap import dedent, indent

from IPython import get_ipython
from IPython.core import magic_arguments
from IPython.core.magic import (
    cell_magic, line_magic, Magics, magics_class
)

from twisted_ipython.config import config
from twisted_ipython.async_runner import twisted_runner


def install_autoawait(ipython):
    ipython.loop_runner_map['twisted'] = (twisted_runner, True)


def _detect_indentation(cell):
    for line in cell.split('\n'):
        m = re.match(r'^(\s+)\S+', line)

        if m:
            return m.group(0)

    return '    '


@magics_class
class TwistedMagics(Magics):

    @magic_arguments.magic_arguments()
    @magic_arguments.argument(
        'key', type=str
    )
    @magic_arguments.argument(
        'value', type=str, nargs='?', default=None
    )
    @line_magic
    def twisted_config(self, line):
        """
        Configure settings for twisted_ipython:

        - *timeout*: How long to wait for autoawaited twisted code to run
          before canceling, in seconds. Defaults to 60. Crochet uses ``2**31``
          internally as a deprecated "basically infinity" constant, which you
          can use yourself by passing in 'INFINITY'.

        Examples::

            # Show the current config
            %twisted_config show

            # Show just the config for timeout
            %twisted_config show timeout

            # Set the timeout to 5 seconds
            %twisted_config timeout 5

            # Reset the config to its default settings
            %twisted_config reset
        """
        args = magic_arguments.parse_argstring(self.twisted_config, line)

        if args.key == 'show':
            config.show()
        elif args.key == 'reset':
            config.reset()
        else:
            config.set(args.key, args.value)

    @magic_arguments.magic_arguments()
    @magic_arguments.argument(
        'assign',
        type=str, nargs='?', default='_'
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

        For more information, see the documentation for Crochet_.

        .. _run_in_reactor: https://crochet.readthedocs.io/en/stable/api.html#run-in-reactor-asynchronous-results
        .. _EventualResult: https://crochet.readthedocs.io/en/stable/api-reference.html#crochet.EventualResult
        .. _Crochet: https://crochet.readthedocs.io/en/stable/index.html
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
                assign=args.assign
            )
        )

        ipython.run_cell(new_cell)
