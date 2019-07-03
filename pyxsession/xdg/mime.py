import os.path

import attr
from xdg.BaseDirectory import xdg_config_dirs
from xdg.IniFile import IniFile
from xdg.Exceptions import ParsingError
from xdg.Mime import MIMEtype, get_type2 as get_type

from pyxsession.util.decorators import dictable, representable


XDG_MIMEAPPS_DIRS = xdg_config_dirs + [
    '/usr/local/share/applications',
    '/usr/share/applications'
]


def xdg_mimeapps_files(environment=None):
    for directory in xdg_config_dirs:
        filenames = [f'{environment}-mimeapps.list'] if environment else []
        filenames.append('mimeapps.list')

        for filename in filenames:
            yield os.path.join(directory, filename)


def _get_group(ini_file, group):
    if not ini_file:
        return dict()
    return {
        MIMEtype(mine_type): [app for app in apps.split(';') if app]
        for mine_type, apps in ini_file.content.get(group, dict()).items()
    }


@representable
@attr.s
class MimeAppsList:
    filename = attr.ib()
    ini_file = attr.ib()
    parsed = attr.ib()
    parse_exc = attr.ib()

    def get_added_associations(self):
        return _get_group(self, 'Added Associations')

    def get_removed_associations(self):
        return _get_group(self, 'Removed Associations')

    def get_default_applications(self):
        return _get_group(self, 'Default Applications')


def load_xdg_mime_lists(environment=None):
    for filename in xdg_mimeapps_files(environment):
        if os.path.isfile(filename):
            try:
                ini_file = IniFile()
                ini_file.parse(filename)
            except ParsingError as exc:
                yield MimeAppsList(
                    filename,
                    None,
                    False,
                    exc
                )
            else:
                yield MimeAppsList(
                    filename,
                    ini_file,
                    True, None
                )


def _insert(mimetype, apps, target):
    if mimetype not in target:
        target[mimetype] = set()
    else:
        for app in apps:
            target[mimetype].add(app)


def _remove(mimetype, apps, target):
    if mimetype not in target:
        return

    for app in apps:
        target[mimetype].remove(app)

    if not target[mimetype]:
        del target[mimetype]


@representable
@dictable(['environment', 'default_applications', 'registered_applications'])
class MimeDatabase:
    def __init__(self, config):
        self.environment = config.mime.environment

        try:
            self.cache_ini_file = IniFile()
            self.cache_ini_file.parse(config.mime.cache)
        except ParsingError as exc:
            self.cache_parsed = False
            self.cache_parse_exc = exc
            self.registered_applications = dict()
        else:
            self.cache_parsed = True
            self.cache_parse_exc = None

            self.registered_applications = {
                mimetype: set(apps)
                for mimetype, apps in
                _get_group(self.cache_ini_file, 'MIME Cache').items()
            }

        self.default_applications = dict()

        # TODO: Alternate algorithm that doesn't require reversing?
        # The list is short so it's not a big deal
        for mime_list in reversed(list(
            load_xdg_mime_lists(
                environment=self.environment
            )
        )):
            if mime_list.parsed:
                added_associations = mime_list.get_added_associations()
                for mimetype, apps in added_associations.items():
                    _insert(mimetype, apps, self.registered_applications)

                removed_associations = mime_list.get_removed_assoiations()

                for mimetype, apps in removed_associations.items():
                    _remove(mimetype, apps, self.registered_applications)

                    # Assumption is that if the mimetype is removed that we
                    # don't want an associated default application either.
                    #
                    # I could change my mind on this.
                    if mimetype in self.default_applications:
                        for removed_app in apps:
                            self.default_applications[mimetype] = [
                                app
                                for app in self.default_applications[mimetype]
                                if app is not removed_app
                            ]

                default_applications = mime_list.get_default_applications()
                for mimetype, apps in default_applications:
                    _insert(mimetype, apps, self.registered_applications)

                    # Current assumption is that an override should override
                    # the entire key.
                    #
                    # I could change my mind on this.
                    self.default_applications[mimetype] = apps

            else:
                # TODO: Logging
                print(mime_list.exc)

    # TODO: You would need to look up the result of this call against some
    # kind of desktop registry
    def file_applications(filename):
        return self.registered_applications[get_type(filename)]

    def file_default(filename):
        return self.default_applications[get_type(filename)]
