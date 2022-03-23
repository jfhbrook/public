# old memes

old memes is an old-school node.js anti-framework built around the good parts
of flatiron, a selection of classic substack libraries and the few worthwhile
things I personally wrote between roughly 2009 and 2016 - with a targeted
dash of modern conveniences.

the old memes are in the process of being cleaned up and re-released - expect
more additions over the coming months.

## the memes

### framework shit

* kenny-loggins - extensions to make logging with winston sensible
* pickleback - my personal fork of hapi/shot (public)
* safe-url - strip creds from urls before printing

### wrappers, clients and bindings

* @jfhbrook/pandoc - my wrapper for pandoc

### cli tools

* licenseify - generate/maintain license info for new projects

### terminal shit

* @jfhbrook/prompt - prompting library

### math shit

* integers - like the range operator in python
* linspace - like linspace in matlab
* logspace - like logspace in matlab
* @jfhbrook/piecewise - kronecker delta and sgn functions

### devops shit

* clf-parser - parse clf formatted logs (public)
* prm - package registry manager

### funny jokes

* fake-progress-not-frozen - a fake progress bar
* hoarders - node.js's most complete "utility grab bag"

### the attic

a few retired modules may be found in the attic folder.

## install

each of the old memes are on npm and set to public. some of them are
namespaced but many of them are not.

## usage/api

every old meme should have a README.md with an example in it at a minimum.

## developer setup

all of the old memes are installed in an npm workspace. for instance, you may run
`npm i --workspaces` to install dependencies for everything post-clone.

## formatting/linting/style guide

each project has its own standards; some, no standards. if the project already
has formatting and linting let it be, but I plan to move towards standardized
presets for prettier and jshint in the future.

## testing

I've used mocha, vows (ugh) and node-tap at various points over the years.
current tests won't be changing frameworks. tests that are working, are
working. tests in new projects will probably be written in node-tap, but I'm
open to changing my mind.

## the weeds

the `pickleback.js` script is being used to manage the fork syncing process
for the pickleback module. in general, `npm run pickleback -- sync` should do
what you want it to do.

## licensing

each old meme has its own licensing. a lot of it, especially older projects,
use mit licenses, but the apache and mozilla licenses are in there too,
especially with newer projects.

## release plan

* publish prm to npm
* for every project:
  * get tests and/or linting passing, even if it means ripping it out
  * use prm to configure owners
  * update the README
  * if exposes a cli, get COPR to build it
* add justfile tasks to test/lint the workspace
* update the parent README
* dot i's, cross t's

## next steps

* mrs-commanderson - an obnoxious cli framework
* exercise-bike - a cli template runner
* bbgurl - a cli wrapper around request^H^H^H^H^H^H^Hundici

## experiments

* my-little-proxy
