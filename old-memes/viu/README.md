# an npm distribution and wrapper for vue

## what

[vue](https://github.com/atanunq/viu) is a terminal image viewer written in
rust that is pretty nice! this package distributes and wraps vue with npm.

## how?

give this a shot:

```bash
npx @jfhbrook/viu ./buddy.jpg
```

or, call the API:

```js
const viu = require('@jfhbrook/viu');

(async () => {
  await viu('buddy.jpg');
})();
```

## no, I mean *how??*

before publishing, I download and unpack an official release tarball for viu and
use [cross](https://github.com/cross-rs/cross) to build vue for common
architectures:

- linux x64
- linux aarch64
- linux arm32 (targeting raspberry pi)
- windows x64

then, after install, if there isn't a matching pre-built binary, npm will
attempt to build viu from source.

finally, at runtime, if a viu binary can't be found - either pre-built or built
on install - we check the `PATH` to see if viu is already installed for the
user as a last-ditch effort.

## why?!

"but josh, why don't you use [sidre sorhus's terminal-image](https://github.com/sindresorhus/terminal-image),
which is in pure javascript?

terminal-image is great, but it has fewer features than viu - namely, viu supports
[kitty's](https://sw.kovidgoyal.net/kitty/graphics-protocol/) graphics protocol
in addition to iterm's.

on the other hand, this package is a little chonky - it includes a bunch of
binary builds after all - and will fail when an architecture is unsupported
and cargo isn't installed.

if you want the best of both worlds, consider installing *both*, catching
errors from calling viu, and fall back to terminal-image.

## version info

ideally, the version of this package will be the same as the version of viu
that it includes. however, intermediate changes at the package level will require
bumping the patch version when publishing to npm. in other words, the patch
version may be ahead of viu's, but the major and minor should match.

I haven't had a need to make sweeping changes to this module; if/when I do,
I'll revisit this strategy.

## license

This wrapper is released under an MIT license, as is viu.
