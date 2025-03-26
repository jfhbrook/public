# -*- coding: utf-8 -*-

from contextlib import contextmanager
import os
from typing import Generator, Optional, Self

import click
from rich.console import Console
from tplinkrouterc6u import (
    AbstractRouter,
    Connection,
    Firmware,
    Status,
    TplinkRouterProvider,
)

from tplinkctl.status import (
    connection_counts_table,
    device_table,
    system_table,
    wifi_enabled_table,
)


class Obj:
    def __init__(self: Self, url: Optional[str]) -> None:
        self._url: Optional[str] = url
        self._router: Optional[AbstractRouter] = None
        self.console = Console()

    @property
    def router(self: Self) -> AbstractRouter:
        if self._router:
            return self._router

        url = self._url if self._url else os.environ.get("TPLINK_URL", "https://tplinkwifi.net")
        password: str = (
            os.environ["TPLINK_PASSWORD"]
            if "TPLINK_PASSWORD" in os.environ
            else click.prompt("Password", type=str, hide_input=True)
        )

        self._router = TplinkRouterProvider.get_client(url, password, verify_ssl=False)

        return self._router

    @contextmanager
    def session(self: Self) -> Generator[AbstractRouter, None, None]:
        try:
            self.router.authorize()
            yield self.router
        finally:
            self.router.logout()


class WifiConnectionChoice(click.Choice):
    name = "connection"

    def __init__(self: Self) -> None:
        super().__init__(
            [
                conn.name
                for conn in Connection
                if conn not in {Connection.WIRED, Connection.UNKNOWN}
            ]
        )

    def convert(
        self: Self,
        value: str,
        param: Optional[click.Parameter],
        ctx: Optional[click.Context],
    ) -> Connection:
        choice = super().convert(value, param, ctx)

        return Connection[choice]


WIFI_CONNECTION = WifiConnectionChoice()


@click.group()
@click.option("--url", type=str)
@click.pass_context
def main(ctx: click.Context, url: Optional[str]) -> None:
    ctx.obj = Obj(url)


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
@click.argument("connection", type=WIFI_CONNECTION)
@click.pass_obj
def enable(obj: Obj, connection: Connection) -> None:
    """
    Enable a WiFi connection
    """

    with obj.session() as router:
        router.set_wifi(connection, True)


@wifi.command()
@click.argument("connection", type=WIFI_CONNECTION)
@click.pass_obj
def disable(obj: Obj, connection: Connection) -> None:
    """
    Disable a WiFi connection
    """

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
