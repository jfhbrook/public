import crayons
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

            pretty_namespace = crayons.blue(event.get('log_namespace', '????'))
            pretty_level = PRETTY_BY_LEVEL[level]

            print(
                f'{pretty_level} - {pretty_namespace} - {formatEvent(event)}'  # noqa
            )

            if 'log_failure' in event:
                failure = event['log_failure']

                for line in _formatTraceback(failure).split('\n'):
                    print(
                        f'{pretty_level} - {pretty_namespace} - {crayons.yellow("traceback")}: {line}'  # noqa
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
