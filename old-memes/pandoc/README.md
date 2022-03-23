# a thin wrapper around pandoc

this module wraps [pandoc](https://pandoc.org/) in a chainable API,
[which was the style at the time](https://www.youtube.com/watch?v=yujF8AumiQo).

## usage

first, you'll need to [install pandoc](https://pandoc.org/installing.html),
probably through your package manager. then, you'll need to install this module,
with `npm i @jfhbrook/pandoc`.

once that's all done, you can import the wrapper and fluently construct calls
to pandoc like so:

```js
var pandoc = require('@jfhbrook/pandoc'),
    fs = require('fs');

pandoc
  .from('markdown')
  .to('latex')
  .render(fs.createReadStream('./README.md'), function (err, res) {
    console.log(res);
  })
;
```

## tests

right now, the test is running the above example (minus import paths). that's
good enough for my needs right now, but if/when I discover weird bugs I'll
consider more comprehensive test coverage.

## license

this project is available under the [MPL 2.0](https://www.mozilla.org/en-US/MPL/2.0/)
license.
