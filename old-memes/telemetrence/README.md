# @jfhbrook/telemetrence

the core of boltzmann's honeycomb implementation, bent to my own nefarious ends

## usage

TODO! I got the file I want set up, but I need to actually kick the tires on
it to figure out what's missing and/or how to fit it into the rest of old memes.

## development

boltzmann works off tera templates, and I take advantage of that with
[exb](https://npm.im/exercise-bike) to generate the actual bundle and test file.
therefore, to develop you'll need to edit [./honeycomb.ts.njk](./honeycomb.ts.njk)
and then run `npm run build` to generate `./honeycomb.ts` and `./test.ts` and
run `tsc`. `npm t` will automatically do this build.

## license

boltzmann is licensed under an Apache 2.0 license, so this is as well. see
the LICENSE and NOTICE files for details.
