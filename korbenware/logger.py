from contextlib import contextmanager

import crayons
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


def create_logger(**kwargs):
    return Logger(observer=publisher, **kwargs)


@implementer(ILogObserver)
class CliObserver:
    def __init__(self, config):
        self.threshold = LogLevel._levelPriorities[
            LEVEL_BY_NAME[
                config.logger.level
            ]
        ]

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
                f'{pretty_level} - {pretty_namespace} - {formatEvent(event)}'  # noqa
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
        print(eventAsJSON(event))


@implementer(ILogObserver)
class JournaldObserver:
    def __call__(self, event):
        level = event.get('log_level', LogLevel.error)
        namespace = event.get('log_namespace', '????')

        priority = SYSLOG_PRIORITY_BY_LEVEL.get(level, 5)
        message = f'{namespace} - {formatEvent(event)}'

        traceback = (
            _formatTraceback(event['log_failure'])
            if 'log_failure' in event
            else None
        )

        kwargs = dict(
            PRIORITY=priority,
            TWISTED_LOG_LEVEL=NAME_BY_LEVEL[level],
            TWISTED_LOG_NAMESPACE=namespace,
            SYSLOG_FACILITY=2,
            # TODO: Read from config
            SYSLOG_IDENTIFIER='korbenware'
        )

        for k, v in event.items():
            if k not in {
                'log_level', 'log_namespace', 'log_format', 'log_logger',
                'log_failure'
            }:
                kwargs[f'TWISTED_{k.upper()}'] = str(v)

        if traceback:
            kwargs['TWISTED_LOG_FAILURE'] = traceback

        journal.send(message, **kwargs)


@contextmanager
def captured(log):
    log.info('It worked if it ends with OK 👍')
    try:
        yield
    except:  # noqa
        log.failure('== FLAGRANT SYSTEM ERROR==')
        log.critical('NOT OK 🙅')
    else:
        log.info('OK 👍')
