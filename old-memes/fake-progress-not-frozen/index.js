var moment = require('moment'),
  multimeter = require('multimeter')(process),
  EventEmitter = require('events').EventEmitter,
  util = require('util'),
  chalk = require('chalk');

multimeter.charm.on('^C', function () {
  //multimeter.charm.reset();
  console.log('\n');
  process.exit();
});

var Ticker = (module.exports = function (opts) {
  EventEmitter.call(this);

  opts = opts || {};

  this.clock = opts.clock || 40;
  this.gain = opts.gain || 10;
  this.count = 0;
});

util.inherits(Ticker, EventEmitter);

Ticker.prototype.start = function () {
  var self = this;

  multimeter.drop(
    {
      width: 17,
      before:
        chalk.green('info') +
        ':   [' +
        chalk.blue('waitingjerk') +
        '] ' +
        chalk.bold('FAKE PROGRESS: ') +
        chalk.grey('(NOT frozen)') +
        chalk.bold(' ~={|'),
      after: chalk.bold('|:: '),
      solid: {
        background: 'black',
        foreground: 'green',
        text: '✓'
      }
    },
    function (bar) {
      var n = 1,
        t = self.clock,
        k = self.gain;

      var iv = setInterval(function () {
        var p =
          ((98 * (t / k + 1)) / t) * k * (n / (n + k * t) - 1 / (1 + k * t)) -
          1;

        bar.percent(p);

        n++;
      }, t);

      self.on('stop', function (cb) {
        clearInterval(iv);
        bar.percent(100);
        console.log();
        multimeter.destroy();
        if (cb) {
          cb();
        }
      });
    }
  );

  return this;
};

Ticker.prototype.stop = function (cb) {
  this.emit('stop', cb);

  return this;
};
