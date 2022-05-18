# primitivist

an options parser for bash scripts based on [minimist](https://npm.im/minimist).

## example

```bash
eval "$(primitivist -B foo -B bar -S baz -- --foo --baz quux a b c)"

echo "${HELP}"  # empty string
echo "${FOO}"   # 1
echo "${BAR}"   # empty string
echo "${BAZ}"   # quux
echo "${_}"     # (a b c)
```

## cli

primitivist takes two options, `--boolean` (short: `-B`) and `--string` (short: `-S`),
which map to their meanings in minimist. parsing stops early when an unexpected
parameter occurs (ie, `stopEarly: true`), and remaining arguments are passed to a
second minimist parse with the configured boolean and string fields.

## testing

I have a simple test in `./test.sh`. it should cover the basics

## license

MIT

