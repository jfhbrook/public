# mrs commanderson

mrs commanderson is a command line parsing library built on top of
[minimist](https://www.npmjs.com/package/minimist) and
[director](https://github.com/flatiron/director).

![](./mrs-commanderson.png)

## install

this package is distributed with npm and may be installed with:

```bash
npm install @jfhbrook/mrs-commanderson
```

## examples

the simplest example looks like this:

```javascript
#!/usr/bin/env node

const { app } = require('../');

app(process.argv.slice(2), async (opts) => {
  console.log(`hello ${opts.message}`);
});

```

this will construct a default minimist `ParsedArgs` object and call the main
function with it as a coroutine.

a more interesting example implements subcommands:

```javascript
#!/usr/bin/env node

const { App } = require('../');

const app = new App();

app.command("init", async (ctx) => {
  console.log('init:', ctx);
});
app.command("install :pkg", async (ctx, pkg) => {
  console.log('install:', pkg, ctx);
});

app.run(process.argv.slice(2));

```

this example is pretending to be some kind of installer, and supports the
commands `init` and `install <some package>`.

## api

the api is poorly documented right now, beyond the examples. this is because
there are some issues with the api in the underlying routing library which
I'd like to iron out before going too deep into documentation. that said,
the `index.ts` is short and sweet, and `router.ts` is well-commented.

## background

like a lot of people, I enjoy using minimist to parse options. what it brings
to the table is a simple, straightforward API and clear conventions for how
cli arguments translate into javascript objects. it's great! I use it in all
my cli tools!

however, one thing minimist isn't very good at - or rather, doesn't try to
solve at all - is subcommands. what minimist does instead is collect all
positional arguments and assign them to `_: string[]` in the return value.

what minimist is missing is command line routing. a good example of what this
might look like is [click](https://click.palletsprojects.com/en/8.1.x/) - click
uses a decorators pattern to connect command handlers to routes. click is a
little more heavy-handed than what I want though - I still want the lightwight
approach of minimist that scales *small*, while also having just a *little*
extra addition of abstraction to support subcommands.

enter flatiron and director. director is the flatiron framework's router, as
would be used in an http server. but they also supported a version of it on
the frontend, and - important here - a command line version. in fact, it's
what nodejitsu used to power [jitsu](https://github.com/nodejitsu/jitsu).

but using director directly, I found a bit of friction. the API made a lot of
compromises to support all three use cases with the same base implementation.
it set `this` in function callbacks to a hard-coded context object with
minimal customizability. it was written prior to async/await and didn't support
promises. finally, I was trying to use it with typescript, and the types
available - while workable - weren't quite what I wanted either.

so, here's what I did:

* I took director's core router and cli router, and mashed them together
* I converted the router code into typescript, with additional (but not total)
  type safety
* I converted the tests to use [tap](https://node-tap.org/) and
  [@jfhbrook/swears](https://www.npmjs.com/package/@jfhbrook/swears), and got
  the CLI-specific tests running
* I removed "async" (callbacks) routing support and changed everything to
  await coroutines
* I made the context the first argument to route handlers the context object,
  and I made the context object fully customizable
* I wrapped it all in an `Application` abstraction which plumbs minimist and
  the router together.

## current status

the basics work - I have the mvp of features for the director router married
to minimist options.

however, the truth is tha those compromises the router made are still leaking
through to the app-level api. for instance, a custom routing table doesn't
actually work right now and there aren't good mechanisms in place for when
routes don't match anything.

I'm also trying to decide if I should integrate logging into this library or
not. click only integrates logging insofar as it handles some console encoding
edge cases better than `print()` does, but I also have strong opinions on
logging that I set up every time. mrs. commanderson doesn't have logging right
now, but may in the future.

my strategy going forward is going to be trying to use this, and scratching
itches / shaving yaks when I really need to.

## license

this work is based on director, which has an MIT license. it also incorporates
some ideas from the DefinitelyTyped stubs, which have a similarly permissive
license. *my* work is licensed under an apache 2.0 license. for more
information, read the LICENSE and NOTICE texts.
