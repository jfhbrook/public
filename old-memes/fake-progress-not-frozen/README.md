# FAKE PROGRESS: (NOT frozen)

![](https://i.imgur.com/QtQUZUo.png)

a ridiculous fake progress bar to show that the app is still working

## example

this is a full example, which you can also run with `node ./example.js` in
this repo:

```js
var chalk = require('chalk');
var Ticker = require('./');

var ticker = new Ticker();

function log(message) {
  console.log(chalk.green('info') + ':   ' + message);
}

log('about to do something that will take a while...');

var SECONDS = 1000;
var howLong = 15 * SECONDS;

ticker.start();

setTimeout(function () {
  ticker.stop(function (err) {
    if (err) throw err;
    log('all done!');
  });
}, howLong);
```

this example was used to generate the above screenshot.

## license

MIT!

