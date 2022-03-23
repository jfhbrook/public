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
