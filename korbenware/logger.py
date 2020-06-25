from contextlib import contextmanager
import datetime
import sys

import crayons
import pandas as pd
from systemd import journal
from twisted.logger import (
    eventAsJSON, formatEvent, ILogObserver, Logger, LogLevel, LogPublisher
)
from twisted.logger._format import _formatTraceback
from zope.interface import implementer

publisher = LogPublisher()

LEVEL_BY_NAME = dict(
    debug=LogLevel.debug,
    info=LogLevel.info,
    warn=LogLevel.warn,
    error=LogLevel.error,
    critical=LogLevel.critical
)

PRETTY_BY_LEVEL = {
    LogLevel.debug: crayons.magenta('debug 🙃'),
    LogLevel.info: crayons.green('info 👉'),
    LogLevel.warn: crayons.yellow('warning ⚠️'),
    LogLevel.error: crayons.red('error 😬'),
    LogLevel.critical: crayons.red('CRITICAL 😱', bold=True)
}

NAME_BY_LEVEL = {
    v: k
    for k, v in LEVEL_BY_NAME.items()
}

SYSLOG_PRIORITY_BY_LEVEL = {
    LogLevel.debug: 7,
    LogLevel.info: 6,
    LogLevel.warn: 4,
    LogLevel.error: 3,
    LogLevel.critical: 2
}

LEVEL_BY_VERBOSITY = {
    0: LogLevel.error,
    1: LogLevel.warn,
    2: LogLevel.info,
    3: LogLevel.debug
}

VERBOSITY_BY_LEVEL = {
    level: verbosity for verbosity, level in LEVEL_BY_VERBOSITY.items()
}


def get_level_config(config, verbosity=None):
    config_level = LEVEL_BY_NAME[config.logger.level]
    if not verbosity:
        return config_level
    else:
        return LEVEL_BY_VERBOSITY[
            min([VERBOSITY_BY_LEVEL[config_level] + verbosity, 3])
        ]


def create_logger(**kwargs):
    return Logger(observer=publisher, **kwargs)


@implementer(ILogObserver)
class CliObserver:
    def __init__(self, config, level=None, verbosity=None):
        if not level:
            level = get_level_config(config, verbosity)
        self.threshold = LogLevel._levelPriorities[level]

    def __call__(self, event):
        level = event.get('log_level', LogLevel.error)

        if LogLevel._levelPriorities[level] >= self.threshold:

            namespace = event.get('log_namespace', '????')

            if 'log_failure' in event:
                pretty_namespace = crayons.yellow(namespace)
            else:
                pretty_namespace = crayons.blue(namespace)

            pretty_level = PRETTY_BY_LEVEL[level]

            print(
                f'{pretty_level} - {pretty_namespace} - {formatEvent(event)}',  # noqa
                file=sys.stderr
            )

            if 'log_failure' in event:
                failure = event['log_failure']

                for line in _formatTraceback(failure).split('\n'):
                    print(
                        f'{pretty_level} - {pretty_namespace} - {line}'  # noqa
                    )


@implementer(ILogObserver)
class JsonStdoutObserver:
    def __init__(self, config):
        self.threshold = LogLevel._levelPriorities[
            LEVEL_BY_NAME[
                config.logger.level
            ]
        ]

    def __call__(self, event):
        print(eventAsJSON(event), file=sys.stderr)


@implementer(ILogObserver)
class JournaldObserver:
    def __call__(self, event):
        level = event.pop('log_level', LogLevel.error)
        namespace = event.pop('log_namespace', '????')

        priority = SYSLOG_PRIORITY_BY_LEVEL.get(level, 5)
        message = f'{namespace} - {formatEvent(event)}'

        kwargs = dict(
            PRIORITY=priority,
            TWISTED_LOG_LEVEL=NAME_BY_LEVEL[level],
            TWISTED_LOG_NAMESPACE=namespace,
            SYSLOG_FACILITY=2,
            # TODO: Read from config
            SYSLOG_IDENTIFIER='korbenware'
        )

        if 'log_failure' in event:
            failure = event.pop('log_failure')
            traceback = _formatTraceback(failure)

            for line in traceback.split('\n'):
                message += f'\n{namespace} - {line}'

            kwargs['TWISTED_LOG_FAILURE'] = traceback

        for k, v in event.items():
            if k not in {
                'log_format', 'log_logger'
            }:
                kwargs[f'TWISTED_{k.upper()}'] = str(v)

        journal.send(message, **kwargs)


@implementer(ILogObserver)
class PandasObserver:
    COLUMNS = ['timestamp', 'level', 'namespace', 'message', 'failure', 'traceback', 'event']
    def __init__(self):
        self.df = pd.DataFrame(columns=self.COLUMNS)

    def __call__(self, event):
        message = formatEvent(event)
        failure = event.get('log_failure', None)

        traceback = None
        if failure:
            traceback = _format_traceback(failure)
            message += f'\n{traceback}'

        self.df = self.df.append(dict(
            timestamp=pd.to_datetime(datetime.datetime.now()),
            level=NAME_BY_LEVEL.get(event.get('log_level', LogLevel.error), 'error'),
            namespace=event.get('log_namespace', '????'),
            message=message,
            failure=failure,
            traceback=traceback,
            event=event
        ), ignore_index=True)


@contextmanager
def captured(log):
    log.info('It worked if it ends with OK 👍')
    try:
        yield
    except:  # noqa
        log.failure('== FLAGRANT SYSTEM ERROR ==')
        log.critical('NOT OK 🙅')
    else:
        log.info('OK 👍')


def greet(log, hed, subhed, subsubhed=None):
    fields = [('hed', hed), ('subhed', subhed)]
    if subsubhed:
        fields.append(('subsubhed', subsubhed))

    max_len = max(len(value) for name, value in fields)

    log.info('┏━' + ('━' * max_len) + '━┓')
    for name, value in fields:
        log_format = '┃ {' + name + '}' + (' ' * (max_len - len(value))) + ' ┃'
        log.info(log_format, **{name: value})
    log.info('┗━' + ('━' * max_len) + '━┛')
