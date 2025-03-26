# tplinkctl

`tplinctl` is a CLI tool for interacting with TP-Link home routers. It is a thin wrapper around the [tplinkrouterc6u Python module](https://pypi.org/project/tplinkrouterc6u/).

## Install

I currently do not have this project published on PyPI. It can, however, still be installed with `pip`:

```bash
pip install git+https://github.com/jfhbrook/public#subdirectory=tplinkctl
```

## Usage

Usage is pretty straightforward:

```bash
$ tplinkctl --help
Usage: tplinkctl [OPTIONS] COMMAND [ARGS]...

Options:
  --url TEXT
  --help      Show this message and exit.

Commands:
  reboot  Reboot the router
  status  Get a simple status report
  wifi    Commands involving WiFi
```

```bash
$ tplinctl wifi --help
Usage: tplinkctl wifi [OPTIONS] COMMAND [ARGS]...

  Commands involving WiFi

Options:
  --help  Show this message and exit.

Commands:
  disable  Disable a WiFi connection
  enable   Enable a WiFi connection
```

### Configuration

To connect to a router, `tplinkrouterc6u` needs two things: a URL, and a password.

By default, the URL will be set to <https://tplinkwifi.net>, which will typically resolve to your home router. But if need be, a URL may be supplied with with the `--url` option, or the `TPLINK_URL` environment variable.

A password may be supplied with the `TPLINK_PASSWORD` environment variable. If not supplied, `tplinkctl` will prompt the user.

## Unsupported Features

This tool currently does not support the following:

* VPN status or configuration
* LTE features, such as SMS

## License

MIT. See the LICENSE file for details.
