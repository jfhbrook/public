var EventEmitter = require('events').EventEmitter;

// I define just these five levels. in practice I use debug, info, warn and
// error, and I reserve fatal for unhandledException type stuff.
// This object is winston-compatible.
exports.levels = {
  fatal: 0,
  error: 1,
  warn: 2,
  info: 3,
  debug: 4
};

exports.colors = {
  fatal: 'grey',
  error: 'red',
  warn: 'yellow',
  info: 'green',
  debug: 'cyan'
};

exports.MIN_LEVEL = 'debug';
exports.MAX_LEVEL = 'fatal';

// sorts them into an array, so x[0] is the lowest level, and so on.
exports.priorities = Object.keys(exports.levels).sort(function (a, b) {
  if (exports.levels[a] > exports.levels[b]) return 1;
  if (exports.levels[b] > exports.levels[a]) return -1;
  return 0;
});
