# `db_hooks`

Extremely beta sqlalchemy and toml based sql connection manager.

## config file

`db_hooks` looks for a local config file at `./.databases.toml` in your working directory and then looks for a global config file using the [appdirs](https://pypi.org/project/appdirs/) library.

You can edit or create this file in your `$EDITOR` by running `db_hooks edit`. For me, this is vim. If no config exists, it will create one at the default location. In general, that location is one of the following:

|         os | location                                                |
|------------|---------------------------------------------------------|
|      linux | `~/.local/share/db_hooks/databases.toml`                |
|        osx | `~/Library/Application Support/db_hooks/databases.toml` |
| windows 10 | `~\AppData\local\jfhbrook\db_hooks`                     |

The format of this file is currently poorly-documented. The best place to get an idea of the full api is [the source code](https://github.com/jfhbrook/db_hooks/blob/master/db_hooks/config.py). Defaults for most things are sensible.

### connections

Keys in the TOML file under the connections namespace are connection names. 

Connections names are nested under the `connections` namespace. Under those are key/value pairs for the various parameters in a connection. Connections support the following parameters:

* `protocol` - a supported protocol. Currently: `postgres`, `mysql` and `sqlite`.
* `username` - the username to log into the database with.
* `has_password` - set this flag to `false` in order to disable automatic password prompting. Defaults to `true` for all protocols where passwords are supported.
* `host` - the database host.
* `port` - the database port.
* `database` - the database name.
* `password_cmd` - a connection-specific override for the `password_cmd`. By default, a connection will use the globally-set `password_cmd`.

For a very simple example, a local postgres connection might looks like this:

```toml
[connections.pg_example]
protocol = "postgres"
username = "josh"
host = "localhost"
port = "5432"
database = "josh"
```

### passwords

`db_hooks` includes general purpose hooks for fetching passwords for connections, designed to be adaptable to multiple systems.

The top-level config supports two relevant parameters:

* `password_cmd` - a shell snippet that will be ran in order to fetch the password. The command should print a string password to stdout.
* `password_loader` - configure the shell loader/parser used for running the command. defaults to `shlex`, but can be set to `bash` or `powershell` in order to take advantage of a full shell language.

These two parameters, plus the `password_cmd` optional override, can be used to embed a small snippet that fetches the password.

This is designed to allow the most flexibility and therefore will depend on your needs.

For example, you may want to read passwords using [`zenity`](https://help.gnome.org/users/zenity/):

```toml
password_cmd = "zenity --password"
```

In Windows, you may want to use PowerShell to accomplish something similar:

```toml
password_loader = "powershell"
password_cmd = "(Get-Credential -Credential {name}).GetNetworkCredential().Password"
```

### caching

Connections in code are cached by `db_hooks` using [`cachetools`](https://cachetools.readthedocs.io/en/stable/). This means that if you call `get_engine` with the same connection name twice that it will in most cases reuse an already-initialized engine, meaning that you will only be prompted for a password once.

Caching supports four cache types: `LRUCache`, `RRCache`, `TTLCache` and `LFUCache`. Each of these takes a collection of keyword args, which are passed to the corresponding contructors directly.

The default is `LRUCache` with a `maxsize` of 512. This means that all connection info is cached indefinitely until over 512 distinct engines have been created, at which the least recently used engine is evicted.

This API is relatively unstable and may change as the `db_hooks` system is implemented for other languages.

## in your python code

Once you have a connection configured, you can load a sqlalchemy engine using
the `get_engine` API:

```py
from db_hooks import get_engine

engine = get_engine('pg_example')
```

This will pull the connection, prompt for your password, and give you a configured sqlalchemy engine.

## the cli

`db_hooks` exposes a CLI that will launch either `psql`, `mysql` or `sqlite` in a manner appropriate to the underlying connection. You can connect to this database by running `db_hooks connect {your_connection_name_here}`.

### bash complete

`db_hooks` has support for shell tab-completion. You can enable it by running `eval $(_DB_HOOKS_COMPLETE=source db_hooks)` for bash (the default shell for most Linux distributions and older versions of OSX) or `eval $(_DB_HOOKS_COMPLETE=source_zsh db_hooks)` (the default shell in new versions of OSX). PowerShell is unfortunately not supported. For more information, you can [read Click's docs for autocompltion](https://click.palletsprojects.com/en/7.x/bashcomplete/). 

## licensing

This library is licensed under the Apache Software License. See the LICENSE and NOTICE files for details.
