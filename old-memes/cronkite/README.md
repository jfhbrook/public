# cronkite

a dumb little cron-like scheduler built with [node-cron](https://npm.im/node-cron)

## usage

cronkite loads a json file of cron expressions and commands. for example:

```json
{
  "crontab": [
    [ "*/15 * * * *", "echo 'testing 123'" ]
  ]
}
```

if this file is in `./crontab.json`, you can run:

```bash
npx @jfhbrook/cronkite
```

if the file has a different name, you can pass it in explicitly:

```bash
npx @jfhbrook/cronkite -- cron.json
```

## license

Apache 2.0. See the LICENSE file for details.
