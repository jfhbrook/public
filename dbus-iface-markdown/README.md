# dbus-iface-markdown

A little perl script for generating markdown documentation from a live Dbus interface.

## Install

```bash
sudo dnf copr enable jfhbrook/joshiverse
sudo dnf install dbus-iface-markdown
```

## Usage

```
$ dbus-iface-markdown --help
Usage: dbus-iface-markdown [--help] [--system | --session | --bus=ADDRESS | --peer=ADDRESS] [--sender=NAME] [--dest=NAME] [--reply-timeout=MSEC] <PATH>

PARAMETERS:
  PATH  An optional object path (defaults to /)

OPTIONS:
  --help                Show this help message
  --bus ADDRESS         Connect to the bus at the supplied address
  --dest DEST           Dbus destination
  --out FILE            File to write output to (defaults to stdout)
  --peer ADDRESS        Connect to the peer bus at the supplied address
  --reply-timeout MSEC  Set a reply timeout
  --sender SENDER       Dbus sender
  --session             Connect to the session bus
  --system              Connect to the system bus
```

## License

MIT - see `LICENSE` for details.
