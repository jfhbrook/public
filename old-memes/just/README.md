# @jfhbrook/just

a wrapper for [casey/just](https://github.com/casey/just).

I like using just to coordinate running pipelines of *mostly* shell code,
something node is mediocre for at best. but I sometimes want to use it from
wrapper scripts, which may have more sophisticated options parsing, configure
environments, and so on. other times, I want to have tighter integration
between [gulp](https://gulpjs.com/) and just. this lil library helps.

## examples

### running a just recipe

suppose you bundle a `justfile` in your node app:

```justfile
# ./justfile

set dotenv-load := false

hello message:
  echo "{{message}}"
```

here's how you can execute `just hello world` from nodejs:

```js
// ./index.js

const path = require('path');
const { Just } = require('@jfhbrook/just');

(async function main() {
  const just = new Just(path.join(__dirname, 'justfile'));

  // just hello world
  await just.run('hello', 'world');
})();
```

### calling just recipes from gulp (beta)

here's how you can get gulp-cli to run just recipes:

```js
const path = require('path');

const { registry, series } = require('gulp');

const { JustRegistry } = require('@jfhbrook/just/gulp');

registry(new JustRegistry(path.join(__dirname, 'justfile')));

exports.default = series('just:task');
```

I haven't figured out how to pass parameters to just in a reasonable way yet,
so expect this to change quite a bit.

## install

in order for this to work, you'll need to install just. your package manager
probably has it, and cargo definitely has it. I might bundle a few builds
in the future but haven't decided to yet.

afterwards, run `npm install @jfhbrook/just` and you should be off to the
races.

## api

### Just

```js
const just = new Just(JUSTFILE);
```

create a new just instance with the supplied `justfile`.

### just.run

```js
await just.run(...args)
```

run a just command, using the instance's `justfile`. stdio are inherited and
non-zero exits will throw an error.

my needs don't require piping the output elsewhere and finding an ergonomic
child process api in node is a yak I am NOT shaving today.

### just.dump

```js
const dump = await just.dump();
```

runs `just --unstable --dump --dump-format json` and parses and returns the
results. note the `--unstable` flag - I've historically had to install a
beta version of `just` to get it working. idk if that's still required today
because I haven't messed with it in a while!

## development

I actually wrote tests!! you can run them with `npm test`.

no linting or prettifier. I think my code is pretty.

## license

MIT!
