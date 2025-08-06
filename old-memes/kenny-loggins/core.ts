import {EventEmitter} from 'node:events';

// I define just these five levels. in practice I use debug, info, warn and
// error, and I reserve fatal for unhandledException type stuff.
// This object is winston-compatible.
export const levels: {[level: string]: number} = {
  fatal: 0,
  error: 1,
  warn: 2,
  info: 3,
  debug: 4
};

export const colors: {[level: string]: string} = {
  fatal: 'grey',
  error: 'red',
  warn: 'yellow',
  info: 'green',
  debug: 'cyan'
};

export const MIN_LEVEL = 'debug';
export const MAX_LEVEL = 'fatal';

// sorts them into an array, so x[0] is the lowest level, and so on.
export const priorities = Object.keys(exports.levels).sort(function (a, b) {
  if (levels[a] > levels[b]) return 1;
  if (levels[b] > levels[a]) return -1;
  return 0;
});
