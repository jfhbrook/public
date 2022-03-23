var tap = require('tap');

var Ticker = require('./');

var ticker = new Ticker();

ticker.start();

tap.plan(1);

setTimeout(function () {
  ticker.stop(function (err) {
    tap.error(err);
    tap.end();
  });
}, 1000);
