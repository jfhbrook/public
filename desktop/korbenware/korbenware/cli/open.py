# Copyright 2020 Josh Holbrook
#
# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at https://mozilla.org/MPL/2.0/.

import click

from korbenware.cli.base import command, pass_context
from korbenware.config import load_config, log_config
from korbenware.executor import BaseExecutor
from korbenware.logger import create_logger
from korbenware.open import ApplicationFinder, exec_key_fields, OpenError
from korbenware.urls import UrlRegistry
from korbenware.xdg.applications import ApplicationsRegistry
from korbenware.xdg.mime import MimeRegistry


@command(
    help=("Open files and URLs with default and mime-appropriate XDG applications"),
    hed="Korby Jr. The File/Url Opener 🦜",
    subhed='"open up or else!"',
    dek="programmed entirely while eating a spider plant",
)
@click.argument("urls_and_or_files", nargs=-1, required=True)
@pass_context
async def main(ctx, reactor, urls_and_or_files):
    log = create_logger(namespace="korbenware.cli.open")
    config = ctx.config

    applications = ApplicationsRegistry(config)
    mime = MimeRegistry(config, applications)
    urls = UrlRegistry(config, applications)
    finder = ApplicationFinder(urls, mime)

    # TODO: dbus executor
    executor = BaseExecutor()

    for url_or_file in urls_and_or_files:
        try:
            app = finder.get_by_url_or_file(url_or_file)
        except OpenError:
            log.error(
                "Unable to find a suitable application for opening {url_or_file}",  # noqa
                url_or_file=url_or_file,
            )
        else:
            log.info(
                "Opening {url_or_file} with application {application}...",
                url_or_file=url_or_file,
                application=app.filename,
            )
            executor.run_xdg_application(
                app, exec_key_fields=exec_key_fields(app, url_or_file)
            )
