import os
import os.path

from xdg.BaseDirectory import xdg_config_dirs

from korbenware.logger import create_logger
from korbenware.keys import keys
from korbenware.presentation import representable
from korbenware.presentation.markdown import markdownable
from korbenware.xdg.applications import Application, ApplicationsRegistry


XDG_AUTOSTART_DIRS = [
    os.path.join(base, 'autostart')
    for base in xdg_config_dirs
]


class Autostart(Application):
    def __init__(self, fullpath, filename, executable):
        super().__init__(fullpath, filename, executable)

        self._conditions = dict()
        self._shoulds = dict()

    def autostart_conditions(self, environment_name):
        if environment_name in self._conditions:
            conditions = self._conditions[environment_name]
        else:
            conditions = dict(
                parsed=self.executable.parsed,
                is_application=self.executable.is_application,
                exec_key_parsed=self.executable.exec_key_parsed,
                not_hidden=not self.executable.is_hidden,
                not_dbus_activatable=not self.executable.dbus_activatable,
                should_show_in=(
                    self.executable.should_show_in(environment_name)
                ),
                passes_try_exec=self.executable.passes_try_exec()
            )
            self._conditions[environment_name] = conditions
        return conditions

    def should_autostart(self, environment_name):
        if environment_name in self._shoulds:
            should = self._shoulds[environment_name]
        else:
            should = all(self.autostart_conditions(environment_name).values())
        return should


@markdownable
@representable
@keys([
    'directories',
    'environment_name',
    'entries',
    'autostart_entries'
])
class AutostartRegistry(ApplicationsRegistry):
    log = create_logger()

    def __init__(self, config, environment_name='korbenware'):
        super().__init__(config, key='autostart', cls=Autostart)

        self.environment_name = environment_name
        self.autostart_entries = dict()

        for name, entry in self.entries.items():
            if entry.should_autostart(self.environment_name):
                self.log.debug(
                    'Entry {filename} elligible for autostart',
                    filename=entry.filename
                )
                self.autostart_entries[entry.filename] = entry
            else:
                self.log.warn(
                    'Entry {filename} not eligible for autostart',
                    filename=entry.filename,
                    conditions=entry.autostart_conditions(
                        self.environment_name
                    )
                )
