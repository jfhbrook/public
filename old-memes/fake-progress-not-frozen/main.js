#!/usr/bin/env node

var fs = require('fs');
var spawn = require('child_process').spawn;

var chalk = require('chalk');
var minimist = require('minimist');
var Ticker = require('./');

var ticker = new Ticker();

var HELP = [
  'USAGE: fake-progress-not-frozen [OPTIONS] -- CMD [ARGS]',
  '',
  'OPTIONS:',
  '    --help        Show this help',
  '    --log-file    A file to write logs to'
].join('\n');

var opts = minimist(process.argv.slice(2), {
  boolean: ['help'],
  string: ['log-file'],
  alias: { 'log-file': ['f'] }
});

if (opts.help) {
  console.log(HELP);
  process.exit();
}

var logFile = opts['log-file']
  ? fs.createWriteStream(opts['log-file'])
  : null;

var child = spawn(opts._.shift(), opts._);

if (logFile) {
  child.stdout.pipe(logFile);
  child.stderr.pipe(logFile);
}

ticker.start();

child.on('exit', function () {
  ticker.stop(function (err) {
    if (err) throw err;
  });
});
