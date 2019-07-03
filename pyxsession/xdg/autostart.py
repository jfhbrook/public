from collections import defaultdict
import os
import os.path

import attr
from xdg.BaseDirectory import xdg_config_dirs

from pyxsession.util.decorators import dictable, representable
from pyxsession.xdg import config_basedir
from pyxsession.xdg.applications import (
    Application, ApplicationsDatabase, load_application_sets
)


XDG_AUTOSTART_DIRS = [
    os.path.join(base, 'autostart')
    for base in xdg_config_dirs
]


class Autostart(Application):
    def should_autostart(self, environment_name):
        return all([
            self.executable.parsed,
            self.executable.is_application,
            self.executable.exec_parsed,
            not self.executable.is_hidden,
            not self.executable.dbus_activatable,
            self.executable.should_show_in(environment_name),
            self.executable.passes_try_exec()
        ])


@representable
@dictable([
    'directories',
    'environment_name',
    'entries',
    'autostart_entries'
])
class AutostartDatabase(ApplicationsDatabase):
    def __init__(self, config):
        super().__init__(config, key='autostart', cls=Autostart)
        self.autostart_entries = dict()

        self.autostart_entries = {
            filename: entry
            for entry in self.entries.items()
            if entry.should_autostart(self.environment_name)
        }
