# -*- coding: utf-8 -*-

from contextlib import contextmanager
import os
from typing import Generator, Optional, Self

import click
from rich.console import Console
from rich.table import Table
from tplinkrouterc6u import (
    AbstractRouter,
    Connection,
    Firmware,
    Status,
    TplinkRouterProvider,
)


class Obj:
    def __init__(self: Self) -> None:
        url = os.environ.get("ROUTER_URL", "https://tplinkwifi.net")
        password: str = (
            os.environ["ROUTER_PASSWORD"]
            if "ROUTER_PASSWORD" in os.environ
            else click.prompt("Password", type=str, hide_input=True)
        )

        self.console = Console()
        self.router = TplinkRouterProvider.get_client(url, password, verify_ssl=False)

    @contextmanager
    def session(self: Self) -> Generator[AbstractRouter, None, None]:
        if not self.router:
            return
        try:
            self.router.authorize()
            yield self.router
        finally:
            self.router.logout()


class ConnectionChoice(click.Choice):
    name = "connection"

    def __init__(self: Self) -> None:
        super().__init__([conn.name for conn in Connection])

    def convert(
        self: Self,
        value: str,
        param: Optional[click.Parameter],
        ctx: Optional[click.Context],
    ) -> Connection:
        choice = super().convert(value, param, ctx)

        return Connection[choice]


CONNECTION = ConnectionChoice()


def system_table(firmware: Firmware, status: Status) -> Table:
    table = Table(title="System Info")

    table.add_row("Model", firmware.model)
    table.add_row("Hardware Version", firmware.hardware_version)
    table.add_row("Firmware Version", firmware.firmware_version)
    table.add_column("Name")
    table.add_column("Value")

    table.add_row("Uptime", str(status.wan_ipv4_uptime))
    table.add_row("Memory Usage", str(status.mem_usage))
    table.add_row("CPU Usage", str(status.cpu_usage))

    return table


def wifi_enabled_table(status: Status) -> Table:
    wifi_status = Table(title="WiFi Status")

    wifi_status.add_column("Type")
    wifi_status.add_column("Band")
    wifi_status.add_column("Status")

    wifi_status.add_row(
        "WiFi", "2g", "[green]enabled" if status.wifi_2g_enable else "[red]disabled"
    )
    wifi_status.add_row(
        "", "5g", "[green]enabled" if status.wifi_5g_enable else "[red]disabled"
    )
    wifi_status.add_row(
        "", "6g", "[green]enabled" if status.wifi_6g_enable else "[red]disabled"
    )

    wifi_status.add_row(
        "Guest WiFi",
        "2g",
        "[green]enabled" if status.guest_2g_enable else "[red]disabled",
    )
    wifi_status.add_row(
        "", "5g", "[green]enabled" if status.guest_5g_enable else "[red]disabled"
    )
    wifi_status.add_row(
        "", "6g", "[green]enabled" if status.guest_6g_enable else "[red]disabled"
    )

    wifi_status.add_row(
        "IoT WiFi", "2g", "[green]enabled" if status.iot_2g_enable else "[red]disabled"
    )
    wifi_status.add_row(
        "", "5g", "[green]enabled" if status.iot_5g_enable else "[red]disabled"
    )
    wifi_status.add_row(
        "", "6g", "[green]enabled" if status.iot_6g_enable else "[red]disabled"
    )

    return wifi_status


def connection_counts_table(status: Status) -> Table:
    counts = Table(title="Active Connections")

    counts.add_column("Type")
    counts.add_column("Count")

    counts.add_row("Wired", str(status.wired_total or 0))
    counts.add_row("Guest", str(status.guest_clients_total or 0))
    counts.add_row("IoT", str(status.iot_clients_total or 0))
    counts.add_row("WiFi", str(status.wifi_clients_total or 0))

    return counts


def device_table(status: Status) -> Table:
    devices = Table(title="Devices")

    devices.add_column("MAC Address")
    devices.add_column("IP Address")
    devices.add_column("Hostname")
    devices.add_column("Packets Sent")
    devices.add_column("Packets Received")
    devices.add_column("Download")
    devices.add_column("Upload")

    for device in status.devices:
        devices.add_row(
            device.macaddr,
            device.ipaddr,
            device.hostname,
            str(device.packets_sent or 0),
            str(device.packets_received or 0),
            str(device.down_speed),
            str(device.up_speed),
        )

    return devices


@click.group()
@click.pass_context
def main(ctx: click.Context) -> None:
    ctx.obj = Obj()


@main.command()
@click.pass_obj
def status(obj: Obj) -> None:
    """
    Get a simple status report
    """

    console = obj.console

    with obj.session() as router:

        firmware: Firmware = router.get_firmware()
        status: Status = router.get_status()

        console.print(system_table(firmware, status))
        console.print(wifi_enabled_table(status))
        console.print(connection_counts_table(status))
        console.print(device_table(status))


class WifiError(Exception):
    pass


@main.group()
def wifi() -> None:
    """
    Commands involving WiFi
    """

    pass


@wifi.command()
@click.argument("connection", type=CONNECTION)
@click.pass_obj
def enable(obj: Obj, connection: Connection) -> None:
    """
    Enable a WiFi connection
    """

    if connection == Connection.WIRED:
        raise WifiError("Can not enable wired connection")

    with obj.session() as router:
        router.set_wifi(connection, True)


@wifi.command()
@click.argument("connection", type=CONNECTION)
@click.pass_obj
def disable(obj: Obj, connection: Connection) -> None:
    """
    Disable a WiFi connection
    """

    if connection == Connection.WIRED:
        raise WifiError("Can not disable wired connection")

    with obj.session() as router:
        router.set_wifi(connection, False)


@main.command()
@click.pass_obj
def reboot(obj: Obj) -> None:
    """
    Reboot the router
    """

    with obj.session() as router:
        router.reboot()


if __name__ == "__main__":
    main()
