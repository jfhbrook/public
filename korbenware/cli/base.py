from asyncio import coroutine, iscoroutinefunction
from functools import wraps, update_wrapper
import os
import sys

import click
from click._compat import get_text_stderr
from click._unicodefun import _verify_python3_env as verify_python_env
from click.core import augment_usage_errors, _bashcomplete as bashcomplete, make_str
from click.exceptions import Abort, ClickException, Exit
from click.globals import get_current_context
from click.utils import PacifyFlushWrapper
from twisted.internet.defer import ensureDeferred
from twisted.internet.task import react

from korbenware.config import load_config, NoConfigurationFoundError
from korbenware.logger import CliObserver, create_logger, publisher

# Note: Click has a BSD 3-clause license


class Context(click.Context):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self._defer = []

    def defer(self, f):
        self._defer.append(f)

    def run_deferred_actions(self):
        for f in self._defer:
            f()

    def invoke(*args, **kwargs):
        self, callback = args[:2]
        ctx = self

        if isinstance(callback, click.Command):
            other_cmd = callback
            callback = other_cmd.callback
            ctx = Context(other_cmd, info_name=other_cmd.name, parent=self)

            if callback is None:
                raise TypeError(
                    "The given command does not have a callback that can be invoked."
                )

            for param in other_cmd.params:
                if param.name not in kwargs and param.expose_value:
                    kwargs[param.name] = param.get_default(ctx)

        args = args[2:]

        if iscoroutinefunction(callback):
            async def async_runner(*args, **kwargs):
                try:
                    rv = await callback(*args, **kwargs)
                except (
                    EOFError, KeyboardInterrupt, SystemExit,
                    ClickException, OSError,
                    Exit, Abort
                ):
                    raise
                except:  # noqa
                    ctx
                    ctx.log.failure('== FLAGRANT SYSTEM ERROR ==')
                    ctx.log.critical('NOT OK 🙅')

                    sys.exit(1)
                else:
                    ctx.log.info('OK 👍')
                    ctx.run_deferred_actions()

                return rv

            def runner():
                return react(lambda reactor: ensureDeferred(
                    async_runner(reactor, *args, **kwargs)
                ))
        else:
            def runner():
                try:
                    rv = callback(*args, **kwargs)
                except (
                    EOFError, KeyboardInterrupt, SystemExit,
                    ClickException, OSError,
                    Exit, Abort
                ):
                    raise
                except:  # noqa
                    ctx
                    ctx.log.failure('== FLAGRANT SYSTEM ERROR ==')
                    ctx.log.critical('NOT OK 🙅')

                    ctx.exit(1)
                else:
                    ctx.log.info('OK 👍')
                    ctx.run_deferred_actions()

                return rv

        with augment_usage_errors(self):
            with ctx:
                try:
                    self.config = load_config()
                    self.config_exc = None
                except (NoConfigurationFoundError,) as exc:
                    self.config = None
                    self.config_exc = exc

                self.log = create_logger(namespace='korbenware.cli.base')
                self.observer = CliObserver(self.config, verbosity=kwargs.pop('verbose', None))
                publisher.addObserver(self.observer)

                self.log.info('It worked if it ends with OK 👍')

                greet_fields = [('hed', self.command.hed), ('subhed', self.command.subhed)]

                if self.command.dek:
                    greet_fields.append(('dek', self.command.dek))

                max_len = max(len(value) for name, value in greet_fields)

                self.log.info('┏━' + ('━' * max_len) + '━┓')
                for name, value in greet_fields:
                    log_format = '┃ {' + name + '}' + (' ' * (max_len - len(value))) + ' ┃'
                    self.log.info(log_format, **{name: value})
                self.log.info('┗━' + ('━' * max_len) + '━┛')

                if self.config_exc:
                    raise self.config_exc

                return runner()


class KorbenwareCommand:
    def make_context(self, info_name, args, parent=None, **extra):
        for key, value in self.context_settings.items():
            if key not in extra:
                extra[key] = value

        ctx = Context(self, info_name=info_name, parent=parent, **extra)
        with ctx.scope(cleanup=False):
            self.parse_args(ctx, args)
        return ctx


class Command(KorbenwareCommand, click.Command):
    def __init__(self, *args, **kwargs):
        self.hed = kwargs.pop('hed')
        self.subhed = kwargs.pop('subhed')
        self.dek = kwargs.pop('dek', None)

        super().__init__(*args, **kwargs)


class Group(KorbenwareCommand, click.Group):
    pass


verbosity = click.option(
    '-v', '--verbose', count=True,
    help="Set the verbosity for the cli logger. More v's means more logs!"
)


def command(name=None, **attrs):
    cmd = click.command(name, Command, **attrs)

    def decorator(f):
        with_verbose_flag = verbosity(f)
        update_wrapper(with_verbose_flag, f)

        return cmd(with_verbose_flag)

    return decorator


def group(name=None, **attrs):
    return click.command(name, Group, **attrs)


def pass_context(f):
    if iscoroutinefunction(f):
        @wraps(f)
        async def wrapper(*args, **kwargs):
            return await f(get_current_context(), *args, **kwargs)
        return wrapper

    return click.pass_context(f)


def pass_obj(f):
    if iscoroutinefunction(f):
        @wraps(f)
        async def wrapper(*args, **kwargs):
            return await f(get_current_context().obj, *args, **kwargs)

        return wrapper

    return click.pass_obj(f)
