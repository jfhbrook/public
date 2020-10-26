# Copyright 2020 Josh Holbrook
#
# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at https://mozilla.org/MPL/2.0/.

from functools import total_ordering
import os.path
from pathlib import Path
from shutil import copy2

import click
import crayons
from pygments import highlight
from pygments.lexers.configs import IniLexer
from pygments.formatters import Terminal256Formatter
from pygments.styles import get_style_by_name
import xdg.BaseDirectory
import xdg.Mime

from korbenware.cli.base import (
    safe_str,
    color_text_block,
    command,
    echo_table,
    get_color,
    group,
    pass_context,
)
from korbenware.config import load_config
from korbenware.editor import edit as open_editor
from korbenware.logger import create_logger
from korbenware.xdg.applications import ApplicationsRegistry
from korbenware.xdg.autostart import Autostart, AutostartRegistry
from korbenware.xdg.mime import (
    MimeRegistry,
    xdg_mimeapps_files,
    XDG_MIMEINFO_CACHE_FILES,
)


def echo_desktop_file(contents, config):
    return click.echo(
        highlight(
            contents,
            IniLexer(),
            Terminal256Formatter(
                style=get_style_by_name(config.format.pygments_formatter)
            ),
        )
    )


def file_path_table(paths):
    table = [["file path", "exists?"]]

    for f in paths:
        if os.path.isfile(f):
            f = crayons.magenta(f)
            exists = crayons.green("yes")
        else:
            f = crayons.cyan(f)
            exists = crayons.yellow("no")

        table.append([f, exists])

    return table


@group(
    hed="Korben's Cool Petsitter's Configuration Manager 🦜",
    subhed="programmed entirely while Korben was screaming at the neighbors",
)
@pass_context
def main(ctx):
    log = create_logger(namespace="korbenware.cli.config")

    ctx.ensure_object(dict)

    ctx.obj["LOGGER"] = log


@main.group(help="Commands related to the base config loaded from korbenware.toml")
def base():
    pass


@base.command(name="show", help="Show the base config")
@pass_context
def show_base_config(ctx):
    config = ctx.config

    table = [["section", "key", "value"]]

    for section_attr in config.__attrs_attrs__:
        section = getattr(config, section_attr.name)
        color = get_color()
        if hasattr(section, "__attrs_attrs__"):
            for attribute in section.__attrs_attrs__:
                table.append(
                    [
                        color(section_attr.name),
                        color(attribute.name),
                        color(getattr(section, attribute.name)),
                    ]
                )
        else:
            for k, v in section.items():
                table.append([color(section_attr.name), color(k), color(v)])

    echo_table(table, title="base config")


@base.command(name="edit", help="Edit the base config")
@pass_context
def edit_base_config(ctx):
    config = ctx.config
    log = ctx.obj["LOGGER"]

    config_filename = config.meta.config_filename

    log.info(f"Editing {config_filename}...")

    ctx.defer(lambda: open_editor(config_filename))


@main.group(help="Commands related to XDG applications")
@click.pass_context
def applications(ctx):
    ctx.obj["APPLICATIONS"] = ApplicationsRegistry(ctx.config)


@main.group(help="Commands related to XDG autostart entries")
@click.pass_context
def autostart(ctx):
    ctx.obj["AUTOSTART"] = AutostartRegistry(ctx.config)


def render_app_partials(app):
    color = crayons.magenta

    if app.executable.is_hidden:
        hidden = crayons.yellow("yes")
        color = crayons.blue
    else:
        hidden = crayons.green("no")

    if app.executable.no_display:
        no_display = crayons.yellow("yes")
        if not app.executable.is_hidden:
            color = crayons.cyan
    else:
        no_display = crayons.green("no")

    return color, hidden, no_display


def render_autostart_partials(app, config):
    color = crayons.magenta

    if app.should_autostart(config.autostart.environment_name):
        should_start = crayons.green("yes")
    else:
        should_start = crayons.yellow("no")
        color = crayons.blue

    if app.executable.is_hidden:
        hidden = crayons.yellow("yes")
    else:
        hidden = crayons.green("no")

    if app.executable.no_display:
        no_display = crayons.yellow("yes")
    else:
        no_display = crayons.green("no")

    return color, should_start, hidden, no_display


def render_app_detail(app, title, config):
    color = crayons.magenta

    is_autostart = isinstance(app, Autostart)

    if is_autostart:
        (color, should_start, hidden, no_display) = render_autostart_partials(
            app, config
        )

    else:
        color, hidden, no_display = render_app_partials(app)

    if app.executable.parsed:
        parsed = crayons.green("yes")
    else:
        parsed = color_text_block(crayons.yellow, app.executable.parse_exc)

    if app.executable.validated:
        validated = crayons.green("yes")
    else:
        validated = color_text_block(crayons.yellow, app.executable.validate_exc)

    if app.executable.exec_key_parsed:
        exec_key_parsed = crayons.green("yes")
    else:
        exec_key_parsed = color_text_block(
            crayons.yellow, app.executable.exec_key_parse_exc
        )

    table = [["key", "value"]]

    rows = [
        ["full path", app.fullpath],
        ["overridden paths", [o.fullpath for o in app.overrides]],
    ]

    if is_autostart:
        rows.append(["should autostart?", should_start])

    rows += [
        ["hidden?", hidden],
        ["no display?", no_display],
        ["exec key", app.executable.exec_key.raw],
        ["desktop file parsed?", parsed],
        ["desktop file validated?", validated],
        ["exec key parsed?", exec_key_parsed],
    ]

    for row in rows:
        table.append([color(cell) for cell in row])

    echo_table(table, title=title)
    click.echo("")
    click.echo("raw file")
    click.echo("----------")
    with open(app.fullpath, "r") as f:
        echo_desktop_file(f.read(), config)
    click.echo("----------")


def render_apps_overview(apps, title, config):
    is_autostart = isinstance(apps[0], Autostart)
    header = ["name"]

    if is_autostart:
        header.append("should autostart?")

    header += [
        "hidden?",
        "no display?",
        "parsed?",
        "validated?",
        "exec key parsed?",
        "exec key",
    ]

    table = [header]

    for app in apps:
        if is_autostart:
            (color, should_start, hidden, no_display) = render_autostart_partials(
                app, config
            )
        else:
            color, hidden, no_display = render_app_partials(app)

        if app.executable.parsed:
            parsed = crayons.green("yes")
        else:
            parsed = crayons.yellow("no")

        if app.executable.validated:
            validated = crayons.green("yes")
        else:
            validated = crayons.yellow("no")

        if app.executable.exec_key_parsed:
            exec_key_parsed = crayons.green("yes")
        else:
            exec_key_parsed = crayons.yellow("no")

        row = [color(app.filename)]

        if is_autostart:
            row.append(should_start)

        row += [
            hidden,
            no_display,
            parsed,
            validated,
            exec_key_parsed,
            color(app.executable.exec_key.raw),
        ]

        table.append(row)

    echo_table(table, title=title)


@applications.command(
    name="show", help=("Show the XDG applications loaded by Korbenware")
)
@click.option("-a", "--application", help="A particular application to show")
@pass_context
def show_applications(ctx, application):
    config = ctx.config
    log = ctx.obj["LOGGER"]
    applications = ctx.obj["APPLICATIONS"]

    if application:
        render_app_detail(
            applications.entries[application], title="application", config=config
        )
    else:
        render_apps_overview(
            sorted(applications.entries.values()), title="applications", config=config
        )


def sort_by_autostart(apps, environment_name):
    @total_ordering
    class SortElement:
        def __init__(self, app):
            self.app = app
            self.should_start = app.should_autostart(environment_name)

        def __lt__(self, other):
            if self.should_start == other.should_start:
                return self.app < other.app
            return self.should_start > other.should_start

        def __eq__(self, other):
            return (self.should_start == other.should_start) and (self.app == other.app)

    sorter = [SortElement(app) for app in apps]

    sorter.sort()

    return [element.app for element in sorter]


@autostart.command(
    name="show", help=("Show the XDG applications autstarted by Korbenware")
)
@click.option("-a", "--application", help="A particular autostart entry to show")
@pass_context
def show_autostart(ctx, application):
    config = ctx.config
    log = ctx.obj["LOGGER"]
    autostart = ctx.obj["AUTOSTART"]

    environment_name = config.autostart.environment_name

    if application:
        render_app_detail(
            autostart.entries[application], title="autostart entry", config=config
        )
    else:
        render_apps_overview(
            sort_by_autostart(autostart.entries.values(), environment_name),
            title="autostart entries",
            config=config,
        )


class UnresolvedApplicationPathError:
    def __init__(self, src_path, directories):
        super().__init__(
            f"Couldn't generate an edit path for {src_path} in any of: "
            f"{directories.join(', ')}"
        )


# TODO Both of these functions are very, very wrong
def get_desktop_path_from_name(application, registry):
    try:
        app = registry.entries[application]
    except KeyError:
        return os.path.join(registry.directories[0], application)
    else:
        return app.fullpath


def edit_desktop_file(ctx, log, path, directories):
    directories = [Path(directory) for directory in directories]

    src_path = Path(path)

    if copy:
        for directory in directories:
            try:
                dest_path = directories[0] / src_path.relative_to(directory)
            except ValueError:
                continue

        if not dest_path:
            raise UnresolvedApplicationPathError(src_path, directories)

        if src_path != dest_path:
            log.info(
                "Copying {src_path} to {dest_path}...",
                src_path=src_path,
                dest_path=dest_path,
            )
            copy2(src_path, dest_path)
    else:
        dest_path = src_path

    log.info("Opening {file_path} in the editor...", file_path=dest_path)

    ctx.defer(lambda: open_editor(dest_path))


@applications.command(name="edit", help=("Edit an application loaded by korbenware"))
@click.option("-a", "--application", help="An application to edit", required=True)
@click.option(
    "-c",
    "--copy/--no-copy",
    help=(
        "Copy the .desktop file to the highest priority search path if it "
        "doesn't already exist there"
    ),
)
@pass_context
def edit_application(ctx, application, copy):
    log = ctx.obj["LOGGER"]
    applications = ctx.obj["APPLICATIONS"]

    path = get_desktop_path_from_name(application, applications)

    edit_desktop_file(ctx, log, path, applications.directories, copy)


@autostart.command(name="edit", help=("Edit an autostart entry loaded by korbenware"))
@click.option("-a", "--application", help="An entry name to edit", required=True)
@click.option(
    "-c",
    "--copy/--no-copy",
    help=(
        "Copy the .desktop file to the highest priorty search path if it "
        "doesn't already exist there, either from an existing autostart "
        "entry or from an existing desktop entry if none is found"
    ),
)
@pass_context
def edit_autostart(ctx, application, copy):
    log = ctx.obj["LOGGER"]
    autostart = ctx.obj["AUTOSTART"]
    applications = ApplicationsRegistry(ctx.config)

    path = get_desktop_path_from_name(application, autostart)

    directories = autostart.directories + applications.directories

    edit_desktop_file(ctx, log, path, autostart.directories, copy)


@main.group(help="Commands related to MIME type lookups")
def mime():
    pass


@mime.group(help="Commands related to file type associations")
@pass_context
def associations(ctx):
    config = ctx.config

    applications = ApplicationsRegistry(config)
    mime = MimeRegistry(config, applications)

    ctx.obj["APPLICATIONS"] = applications
    ctx.obj["MIME"] = mime


class MimeType(click.ParamType):
    def convert(self, value, param, ctx):
        if not value:
            return value

        parts = str(value).split("/")

        if len(parts) != 2:
            self.fail(
                f"Invalid mime type {value} - must have the format `{{media}}/{{subtype}}`",
                param,
                ctx,
            )
        return xdg.Mime.MIMEtype(parts[0], parts[1])

    def __repr__(self):
        return "MimeType"


@associations.command(
    name="show", help="Show the file type associations recognized by korbenware"
)
@click.option(
    "-t", "--mime-type", type=MimeType(), help="A particular file type to show"
)
@pass_context
def show_associations(ctx, mime_type):
    mime = ctx.obj["MIME"]

    table = [["mime type", "applications", "default"]]

    if mime_type:
        keys = [mime_type]
    else:
        keys = sorted(set(mime.lookup.keys()) | set(mime.defaults.keys()), key=str)

    for mime_type in keys:
        applications = mime.lookup.get(mime_type, None)
        default = mime.defaults.get(mime_type, None)

        color = get_color()

        table.append(
            [
                color(mime_type),
                color(applications) if applications else crayons.yellow("None"),
                color(default) if default else crayons.yellow("None"),
            ]
        )

    echo_table(table, title="associations and defaults")


@mime.group(help="Commands related to mimeapps.list files")
def mimeapps():
    pass


@mimeapps.command(name="paths")
@pass_context
def show_mimeapps_paths(ctx):
    echo_table(file_path_table(xdg_mimeapps_files(ctx.config.mime.environment)))
