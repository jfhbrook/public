# npm-link
## a targeted and direct alternative to npm link

## usage

suppose you have some local dependency somewhere on the filesystem and you're
in the directory of the app you want to use it in. using this tool would look
like this:

```bash
$ npx @jfhbrook/npm-link <dependency> [--as <name>]
```

where dependency is the path to the dependency and --as is the module name. if
the module name isn't specified, the name of the module according to the
package.json at that path will be used (this is usually what you want!)

## background & motivation

npm works great when you're installing third party modules into an app. but
when you're trying to develop coupled dependencies, things can get challenging.

if you have your modules in the same folder - or can otherwise hard-code the
relative paths to the module sources - then [npm workspaces](https://docs.npmjs.com/cli/v8/using-npm/workspaces)
(or similar functionality in yarn) should have you covered. if this is your
situation, then npm workspaces are the recommended approach.

however, in some situations you need to get a little more manual. if you were
to continue using the tools npm gives you, you would reach for
[`npm link`](https://docs.npmjs.com/cli/v8/commands/npm-link), which uses
symlinks to put the packages in the right place.

the problem with `npm link` (aside from windows not really having symbolic
links) is that exposing a module modifies npm's global namespace. as all the
cool kids know, the only thing more icky than state is global state. this
doesn't even consider the case where npm is installed on the system instead of
in a user-scoped environment - don't run npm with sudo, kids!

`npm-link`, in contrast, operates through a direct symlink between the module
that you point it at and your app's `node_modules` folder. this is *a lot dumber*
then npm (that may cause us surprises!), but it's also a lot more direct.

## tests

"testing" is largely me just using it. note that I haven't used it recently
due to adopting workspaces, but plan on integrating it in the near future.

## license

MIT.
