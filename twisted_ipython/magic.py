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
        m = re.match(r'^(\s+)', line)

        if m:
            return m.group(0)

    return '    '


@magics_class
class TwistedMagics(Magics):

    @magic_arguments.magic_arguments()
    @magic_arguments.argument(
        'assign',
        type=str, nargs='*', default='_'
    )
    @cell_magic
    def run_in_reactor(self, line, cell):
        """
        Run this cell wrapped by `crochet.run_in_reactor`.
        """

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
                assign=args.assign[0] if args.assign else '_')
        )

        ipython.run_cell(new_cell)
