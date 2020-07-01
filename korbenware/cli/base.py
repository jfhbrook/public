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
import crayons
from terminaltables import DoubleTable
from toml.decoder import TomlDecodeError
from twisted.internet.defer import ensureDeferred
from twisted.internet.task import react

from korbenware.config import load_config, NoConfigurationFoundError
from korbenware.logger import CliObserver, create_logger, publisher

# Note: Click has a BSD 3-clause license


class Context(click.Context):
    def __init__(self, command, parent=None, **extra):
        super().__init__(command, parent, **extra)

        # This Context class differs from its parent in that it loads the
        # korbenware base config, sets up logging and does a little logging
        # itself.
        if self.parent:
            self.config = getattr(parent, "config", None)
            self.config_exc = getattr(parent, "config_exc", None)
            self.log = getattr(parent, "log", None)
            self.observer = getattr(parent, "observer", None)
        else:
            self.config = None
            self.config_exc = None
            self.log = None
            self.observer = None

        self._defer = []

    def defer(self, f):
        """
        Defer an action until after a command has been executed but before exit
        actions take place. This is mostly used for exec calls, which replaces
        the process such that it effectively exits.
        """
        self._defer.append(f)

    def _run_deferred_actions(self):
        for f in self._defer:
            f()

    def _log_ok(self):
        # We only want to log the OK if this is the actual command being ran,
        # so when it's in the context of a group we stay quiet.
        if not hasattr(self.command, "commands"):
            self.log.info("OK 👍")

    def _log_failure(self):
        self.log.failure("== FLAGRANT SYSTEM ERROR ==")
        self.log.critical("NOT OK 🙅")

    def invoke(*args, **kwargs):
        # Starting from here is much the same as click.Context.invoke...
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

        if not iscoroutinefunction(callback):
            # In our version of invoke, we want custom logging of exits and
            # failures, so we try/except around the callback, ignoring a big
            # list of exceptions with special behavior in Click and Python,
            # and log accordingly.
            def runner():
                try:
                    rv = callback(*args, **kwargs)
                except (
                    EOFError,
                    KeyboardInterrupt,
                    SystemExit,
                    ClickException,
                    OSError,
                    Exit,
                    Abort,
                ):
                    raise
                except:  # noqa
                    self._log_failure()
                    self.exit(1)
                else:
                    self._log_ok()
                    self._run_deferred_actions()

                return rv

        else:
            # We also handle cases where the command is a Twisted coroutine -
            # in these scenarios we do basically the same thing as before,
            # except inside of a coroutine function.
            async def async_runner(*args, **kwargs):
                try:
                    rv = await callback(*args, **kwargs)
                except (
                    EOFError,
                    KeyboardInterrupt,
                    SystemExit,
                    ClickException,
                    OSError,
                    Exit,
                    Abort,
                ):
                    raise
                except:  # noqa
                    self._log_failure()
                    # Click's default exit mechanism is raising a special Exit
                    # exception, which it can't capture in an async context.
                    # Instead, we assume that its exit behaviors only matter
                    # before "async things happen" and manually exit(1).
                    sys.exit(1)
                else:
                    self._log_ok()
                    self._run_deferred_actions()

                return rv

            # This coroutine function is ran using task.react and ensureDeferred
            # - note that the return value that Click receives is that of
            # task.react and not of our coroutine. Such is life.
            def runner():
                return react(
                    lambda reactor: ensureDeferred(
                        async_runner(reactor, *args, **kwargs)
                    )
                )

        # These two context managers are as in Click...
        with augment_usage_errors(self):
            with ctx:
                # If necessary, we load the korbenware config, set up a
                # logger for the context and configure a CLI observer with
                # appropriate verbosity. If this is a child context, then it
                # should already have these properties.
                if not self.config:
                    try:
                        self.config = load_config()
                        self.config_exc = None
                    except (NoConfigurationFoundError, TomlDecodeError) as exc:
                        self.config = None
                        self.config_exc = exc

                if not self.log:
                    self.log = create_logger(namespace="korbenware.cli.base")
                if not self.observer:
                    self.observer = CliObserver(
                        self.config, verbosity=kwargs.pop("verbose", None)
                    )
                    publisher.addObserver(self.observer)
                else:
                    del kwargs["verbose"]

                if not self.parent:
                    self.log.info("It worked if it ends with OK 👍")

                    greet_fields = [
                        ("hed", self.command.hed),
                        ("subhed", self.command.subhed),
                    ]

                    if self.command.dek:
                        greet_fields.append(("dek", self.command.dek))

                    max_len = max(len(value) for name, value in greet_fields)

                    self.log.info("┏━" + ("━" * max_len) + "━┓")
                    for name, value in greet_fields:
                        log_format = (
                            "┃ {" + name + "}" + (" " * (max_len - len(value))) + " ┃"
                        )
                        self.log.info(log_format, **{name: value})
                    self.log.info("┗━" + ("━" * max_len) + "━┛")

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

    def handle_greet_fields(self, kwargs):
        self.hed = kwargs.pop("hed", "Korben's weird uncle's super secret command")
        self.subhed = kwargs.pop("subhed", '"If I told ya I\'d have to shoot cha!"')
        self.dek = kwargs.pop("dek", None)


class Command(KorbenwareCommand, click.Command):
    def __init__(self, *args, **kwargs):
        self.handle_greet_fields(kwargs)
        super().__init__(*args, **kwargs)


class Group(KorbenwareCommand, click.Group):
    def __init__(self, *args, **kwargs):
        self.handle_greet_fields(kwargs)
        super().__init__(*args, **kwargs)

    def command(self, *args, **kwargs):
        def decorator(f):
            cmd = command(*args, **kwargs)(f)
            self.add_command(cmd)
            return cmd

        return decorator

    def group(self, *args, **kwargs):
        def decorator(f):
            cmd = group(*args, **kwargs)(f)
            self.add_command(cmd)
            return cmd

        return decorator


verbosity = click.option(
    "-v",
    "--verbose",
    count=True,
    help="Set the verbosity for the cli logger. More v's means more logs!",
)


def command(name=None, cls=Command, **attrs):
    cmd = click.command(name, cls, **attrs)

    def decorator(f):
        with_verbose_flag = verbosity(f)
        update_wrapper(with_verbose_flag, f)

        return cmd(with_verbose_flag)

    return decorator


def group(name=None, **attrs):
    return command(name, Group, **attrs)


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


def safe_str(entity):
    """crayons has a bug where entity.str returns the raw thing (instead of
    stringifying it) when colors are disabled by the terminal. This function can
    be used to work around that.
    """
    return str(entity.__str__())


class ColorCycler:
    COLORS = ["blue", "magenta", "cyan"]

    def __init__(self):
        self.i = -1

    def __call__(self):
        self.i += 1
        if self.i >= len(self.COLORS):
            self.i = 0

        crayon = getattr(crayons, self.COLORS[self.i])

        return lambda o: safe_str(crayon(o))


get_color = ColorCycler()


def echo_table(table, **kwargs):
    t = DoubleTable([[safe_str(cell) for cell in row] for row in table], **kwargs)

    t.inner_row_border = True

    click.echo(t.table)


def color_text_block(crayon, block):
    return "\n".join([safe_str(crayon) for line in safe_str(block).split("\n")])
