# old memes

old memes is an old-school node.js anti-framework built around the good parts
of flatiron, a selection of classic substack libraries and the few worthwhile
things I personally wrote between roughly 2009 and 2016 - with a targeted
dash of modern conveniences.

the old memes are in the process of being cleaned up and re-released - expect
more additions over the coming months.

## the memes

### framework stuff

* [kenny-loggins](./kenny-loggins) - extensions to make logging with winston sensible
* [@jfhbrook/http-server-request-accept](./http-server-request-accept) - extract the accept header from a server request
* [@jfhbrook/http-server-request-ip](./http-server-request-ip) - get the client ip from an http server request, respecting x-forwarded-for headers
* [pickleback](./pickleback) - my personal fork of hapi/shot
* [safe-url](./safe-url) - strip creds from urls before printing

### wrappers, clients and bindings

* [@jfhbrook/pandoc](./pandoc) - my wrapper for pandoc

### cli tools

* [licenseify](./licenseify) - generate/maintain license info for new projects

### terminal stuff

* [@jfhbrook/prompt](./prompt) - a prompting library

### math stuff

* [integers](./integers) - like the range operator in python
* [linspace](./linspace) - like linspace in matlab
* [logspace](./logspace) - like logspace in matlab
* [@jfhbrook/piecewise](./piecewise) - kronecker delta and sgn functions

### devops stuff

* [clf-parser](./clf-parser) - parse clf formatted logs (public)
* [@jfhbrook/prm](./prm) - package registry manager

### funny jokes

* [@jfhbrook/fake-progress-not-frozen](./fake-progress-not-frozen) - a fake progress bar
* [hoarders](https://github.com:jfhbrook/hoarders) - node.js's most complete "utility grab bag"

## install

each of the packages are on npm and set to public. some of them are
namespaced but many of them are not.

## usage/api

every old meme should have a README.md with an example in it at a minimum.

## developer setup

all of the packages are installed in an npm workspace. for instance, you may run
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
