# -*- coding: utf-8 -*-

from contextlib import contextmanager
import os

import click
from rich.console import Console
from rich.table import Table
from tplinkrouterc6u import TplinkRouterProvider


class Context:
    def __init__(self):
        url = os.environ.get("ROUTER_URL", "https://tplinkwifi.net")
        password = os.environ["ROUTER_PASSWORD"]

        self.console = Console()
        self.router = TplinkRouterProvider.get_client(url, password, verify_ssl=False)

    @contextmanager
    def session(self):
        if not self.router:
            return
        try:
            self.router.authorize()
            yield self.router
        finally:
            self.router.logout()


def system_table(firmware, status):
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


def wifi_enabled_table(status):
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


def connection_counts_table(status):
    counts = Table(title="Active Connections")

    counts.add_column("Type")
    counts.add_column("Count")

    counts.add_row("Wired", str(status.wired_total or 0))
    counts.add_row("Guest", str(status.guest_clients_total or 0))
    counts.add_row("IoT", str(status.iot_clients_total or 0))
    counts.add_row("WiFi", str(status.wifi_clients_total or 0))

    return counts


def device_table(status):
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
def main(ctx):
    ctx.obj = Context()


@main.command()
@click.pass_context
def status(ctx):
    console = ctx.obj.console

    with ctx.obj.session() as router:

        firmware = router.get_firmware()
        status = router.get_status()

        console.print(system_table(firmware, status))
        console.print(wifi_enabled_table(status))
        console.print(connection_counts_table(status))
        console.print(device_table(status))


if __name__ == "__main__":
    main()
