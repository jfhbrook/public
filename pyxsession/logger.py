import threading
from queue import Queue

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


class _Action:
    pass


LOG_ACTION = _Action()

EXIT_ACTION = _Action()


class JournaldObserverError(Exception):
    pass


@implementer(ILogObserver)
class JournaldObserver:
    def __init__(self, reactor):
        self.queue = Queue()
        self.thread = threading.Thread(target=self.worker)
        self.thread.start()
        self.reactor = reactor
        self.reactor.addSystemEventTrigger(
            'after', 'shutdown', self.stop
        )

    def stop(self):
        self.queue.put((EXIT_ACTION, None, None))

    def worker(self):
        while True:
            action, message, kwargs = self.queue.get(block=True)

            if action == EXIT_ACTION:
                break
            elif action == LOG_ACTION:
                journal.send(message, **kwargs)
                self.queue.task_done()
            else:
                raise JournaldObserverError(
                    f'Unknown action {action}'
                )

    def __call__(self, event):
        level = event.get('log_level', LogLevel.error)
        priority = SYSLOG_PRIORITY_BY_LEVEL.get(level, 5)
        namespace = event.get('log_namespace', '????')
        message = f'{namespace} - {formatEvent(event)}'
        time = event.get('log_time')
        if time:
            time = repr(time)
        else:
            time = '???'

        if 'log_failure' in event:
            failure = event['log_failure']
            traceback = _formatTraceback(failure)

        kwargs =  dict(
            PRIORITY=priority,
            TWISTED_LEVEL=NAME_BY_LEVEL[level],
            TWISTED_NAMESPACE=namespace,
            TWISTED_TIME=time,
            SYSLOG_FACILITY=2,
            # TODO: Read from config
            SYSLOG_IDENTIFIER='pyxsession'
        )

        if traceback:
            kwargs['TWISTED_FAILURE'] = traceback

        self.queue.put((LOG_ACTION, message, kwargs))
