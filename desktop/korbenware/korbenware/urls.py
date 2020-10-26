# Copyright 2020 Josh Holbrook
#
# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at https://mozilla.org/MPL/2.0/.

import urllib

from korbenware.logger import create_logger


class UrlRegistry:
    log = create_logger()

    def __init__(self, config, applications):
        self.lookup = dict()
        for scheme, desktop_file in config.urls.items():
            self.log.debug(
                "Registering desktop application {application_name} as the opener for {scheme}:// urls...",  # noqa
                application_name=desktop_file,
                scheme=scheme,
            )
            self.lookup[scheme] = desktop_file
        self.applications = applications

    def get_application_by_url(self, url):
        parsed = urllib.parse.urlparse(url)

        return self.get_application_by_scheme(parsed.scheme)

    def get_application_by_scheme(self, scheme):
        if scheme not in self.lookup:
            return None

        key = self.lookup[scheme]

        return self.applications.entries.get(key)
