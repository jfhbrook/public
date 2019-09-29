# `db_hooks`

Extremely beta sqlalchemy and toml based sql connection manager.

## config file

`db_hooks` looks for a local config file at `./.databases.toml` in your working directory and then looks for a global config file using the [appdirs](https://pypi.org/project/appdirs/) library. Right now there isn't an obvious way to find this path, but running `db_hooks list` will bomb with a useful error message if the file isn't there. In general, try these locations:

|         os | location                                                |
|------------|---------------------------------------------------------|
|      linux | `~/.local/share/db_hooks/databases.toml`                |
|        osx | `~/Library/Application Support/db_hooks/databases.toml` |
| windows 10 | `~\AppData\local\jfhbrook\db_hooks`                     |

Keys in the TOML file are connection names. Under those are key/value pairs for the various parameters in a connection. Connections support the following parameters:

* `connection` - a sqlalchemy-compatible connstring. May have a `{password}` f-string parameter.
* `password_cmd` - a bash command that will be executed in order to fetch the password, which will be applied to `connection` as an f-string.

In general, one would use `password_cmd` to write a small snippet that fetches the password. This is designed to allow the most flexibility and therefore will depend on your needs.

For example, you may have a local postgres account and want to read the password using [`zenity`](https://help.gnome.org/users/zenity/):

```toml
[pg_example]
connection = "postgresql+psycopg2://josh:{password}@localhost:5432/josh"
password_cmd = "zenity --password"
```

## in your code

Once you have a connection configured, you can load a sqlalchemy engine using
the `get_engine` API:

```py
from db_hooks import get_engine

engine = get_engine('pg_example')
```

This will pull the connection, run your `password_cmd` and give you a configured sqlalchemy engine.

Note that `get_engine` is cached with a `cachetools.TTLCache` configured with a ttl of 10 minutes.

## the cli

`db_hooks` exposes a CLI that will launch either `psql` or `mysql` in a manner appropriate to the underlying connection. You can run `db_hooks --help` for hopefully useful help output.

## licensing

This library is licensed under the Apache Software License. See the LICENSE and NOTICE files for details.
