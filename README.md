# `db_hooks`

Extremely beta sqlalchemy and toml based sql connection manager.

## config file

`db_hooks` looks for toml a local config file at `./.databases.toml` in your working directory and then looks for a global config file using the [appdirs](https://pypi.org/project/appdirs/) library. Right now there isn't an obvious way to find this path, but running `db_hooks list` will bomb with a useful error message if the file isn't there. In general, try these locations:

|         os | location                                                |
|------------|---------------------------------------------------------|
|      linux | `~/.local/share/db_hooks/databases.toml`                |
|        osx | `~/Library/Application Support/db_hooks/databases.toml` |
| windows 10 | `~\AppData\local\jfhbrook\db_hooks`                     |

Keys in the TOML file are connection names. Under those are key/value pairs for the varios parameters in a connection. Connections support the following parameters:

* `connection` - a sqlalchemy-compatible connstring. May have a `{password}` f-string parameter.
* `password` - a plaintext password that can be applied to `connection`
* `password_cmd` - a bash command that will be executed in order to fetch the password.

In general, one would use `password_cmd` to write a small snippet that fetches the password. This is designed to allow the most flexibility and therefore will depend on your needs.

For example, you may have a local postgres account and want to read the password using [`zenity`](https://help.gnome.org/users/zenity/):

```toml
[pg_example]
connection = "postgresql+psycopg2://josh:{password}@localhost:5432/josh"
password_cmd = "zenity --password"
```

## the cli

`db_hooks` exposes a CLI that will launch either `psql` or `mysql` in a manner appropriate to the underlying connection. You can run `db_hooks --help` for hopefully useful help output.

## licensing

This library is licensed under the Apache Software License. See the LICENSE file for details.
