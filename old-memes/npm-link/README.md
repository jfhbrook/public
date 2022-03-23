# npm-link
## a kinder, gentler alternative to npm link

## install

$ npm install @jfhbrook/npm-link

## usage

inside the project you want to link into:

```
npm-link <dependency> [--as <name>]
```

where dependency is the path to the dependency and --as is the module name. if
the module name isn't specified, the name of the module according to the
package.json at that path will be used (this is usually what you want!)

## rationale

many years ago, I wrote (with some edits):

> `npm link` is a nifty little tool that will symlink arbitrary node libraries on
> the filesystem directly into your project. This is really useful for developing
> a dependent and dependency concurrently.
> 
> However, there's a small but important wrinkle: Linking works in two parts.
> `npm link` exposes the module as installable by first linking it *globally*.
> Then, `npm link [dependency]` links the *global* version of the module into
> your project. Usually this isn't a deal-breaker, but there are some less
> savoury ramifications:
>
> * Running `npm link` as a priveleged user (not technically necessary, but the
>   default behavior) requires unsettlingly high permissions given the task at
>   hand
> * You expose a development version of potential module bins to all your shells
> * git+ssh urls can cause problems because ssh doesn't properly inherit
>   your known hosts when ran with sudo.
> 
> `npm-link` is used to symlink other modules directly into `node_modules`, thus
> avoiding some of these issues.

so here's the thing: I have no idea if this got fixed in the last 5 years, or
even if it got fixed earlier and I wasn't paying attention. but now I'm used
to using this homebrewed tool. it used to have a different name that I find
cringe now but I still want to use it SO I DONT HAVE TO LEARN so I moved it
here.

## Tests

Right now, just me using it.

## License

MIT.
