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
* [@jfhbrook/logref](./logref) - my implementation of `process.logging`
* [@jfhbrook/mrs-commanderson](./mrs-commanderson) - a cli parsing/routing library
* [pickleback](https://github.com/jfhbrook/pickleback) - my personal fork of hapi/shot
* [@jfhbrook/prompt](./prompt) - a prompting library
* [safe-url](./safe-url) - strip creds from urls before printing

### clients and bindings

* [@jfhbrook/pandoc](./pandoc) - my wrapper for pandoc
* [@jfhbrook/just](./just) - a wrapper for [casey/just](https://github.com/casey/just)

### cli tools

* [bbgurl](./bbgurl) - a cli http client using udici
* [exercise-bike](./exercise-bike) - a command line interface for nunjucks
* [licenseify](./licenseify) - generate/maintain license info for new projects
* [primitivist](./primitivist) - a bash command line options parser based on minimist
* [@jfhbrook/cronkite](./cronkite) - a cli for scheduled jobs with [node-cron](https://npm.im/node-cron)
* [@jfhbrook/npm-link](./npm-link) - a targeted and direct alternative to npm link
* [@jfhbrook/viu](./viu) - a distribution and wrapper for [viu](https://crates.io/crates/viu)

### math stuff

* [integers](./integers) - like the range operator in python
* [linspace](./linspace) - like linspace in matlab
* [logspace](./logspace) - like logspace in matlab
* [@jfhbrook/piecewise](./piecewise) - kronecker delta and sgn functions

### devops stuff

* [clf-parser](./clf-parser) - parse clf formatted logs (public)

### typescript stuff

* [types-galore](https://github.com/jfhbrook/types-galore) - a collection + tool for third-party type stubs

### funny jokes

* [@jfhbrook/fake-progress-not-frozen](./fake-progress-not-frozen) - a fake progress bar
* [hoarders](https://github.com/jfhbrook/hoarders) - node.js's most complete "utility grab bag"
* [tests-of-the-sierra-madre](./tests-of-the-sierra-madre) - a humorous test stub

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

## licensing

each old meme has its own licensing. a lot of it, especially older projects,
use mit licenses, but the apache and mozilla licenses are in there too,
especially with newer projects.
