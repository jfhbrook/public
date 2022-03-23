# kenny-loggins

### HIGHWAY TO THE LOGGING ZONE

![](https://i.imgur.com/sGpGwH4.jpeg)

### RIGHT INTO THE LOGGING ZONE

## what

this is my logging module. it uses a combination of [winston](https://npm.im/winston)
and [@jfhbrook/logref](https://npm.im/@jfhbrook/logref) to do the heavy lifting,
supplies a few handy functions and mostly stays out of the way.

## api

### var loggins = require('kenny-loggins');

#### loggins.createLogger(opts)

this function returns a winston logger configured for cli logging to stdout
and configured to observe logs from the `@jfhbrook/logref` implementation
of `process.logging`. it's also configured to log unhandled exceptions and
unhandled rejections.

options:

- `level` - the level of the logger, defaults to 'info'
- `logref.level` - the level at which to log process.logging events, defaults to
  'debug'
- `meta` - the winston `defaultMeta` argument, except I was able to make the
  name shorter

#### loggins.observe(logger, level)

this function takes a winston logger and a logging level and uses the
`process.logging.observe` api as implemented in `@jfhbrook/logref` to collect
logs from `process.logging` and send them to winston. all logs from all
`process.logging` loggers are emitted at the same level.

#### loggins.levels

this is an object containing a winston levels object.

kenny-loggins configures winston to use these levels:

- debug - stuff you usually don't want to see
- info - stuff you might want to mute in production
- warn - warnings
- error - errors
- fatal - errors that crash the process

#### loggins.priorities

this is the reverse lookup for `loggins.levels`. while levels map from
a string name to an integer priority, this maps from priority back to level.

#### loggins.colors

this is an object containing a [logform](https://npm.im/logform) colors spec
for the cli log formatter. its colors are similar to what we see in the
standard winston cli logger, but it also includes a color for the "fatal"
log level.

#### loggins.formatter

this is the winston formatter used by this library. right now it's the
standard winston cli formatter with colors configured.

### var minimistLog = require('kenny-loggins/minimist');

this module contains helpers for integrating [minimist](https://npm.im/minimist)
options parsing with kenny-loggins.

#### minimistLog.verbosity(opts, defaultLevel)

this function will take a minimist style opts object and a default level.
if minimist appears to set either the `-v` or `--verbose` flag it will return
a level one lower, and if not it will return the default level.

if the `--log-level` flag is set in the opts object, that level will be used.

### var syslog = require('kenny-loggins/syslog');

#### syslog.toSyslog(level)

this function will take a kenny-loggins level and return an appropriate
syslog compatible priority number.

#### syslog.fromSyslog(priority)

this function will take a syslog priority number and return an appropriate
kenny-loggins level.

## development

this project uses `tap` for testing and `prettier` for formatting. I don't have
linting yet because my linting config and my prettier config don't agree rn.
Either way, you can run formatting with `npm run format` and tests with
`npm test`.

## license

kenny-loggins is licensed under the apache license, v2.0.
