import pytest
import pytest_twisted

from twisted.internet import reactor
from unittest.mock import Mock

from korbenware.twisted.procmon import ProcessMonitor


@pytest.fixture
def monitor():
    monitor = ProcessMonitor(reactor=reactor)

    monitor.spawnProcess = Mock()

    return monitor


def test_procmon(monitor):
    pass
