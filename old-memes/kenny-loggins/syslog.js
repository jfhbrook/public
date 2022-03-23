var core = require('./core');

// convert from a loggins log level to a syslog level.
exports.toSyslog = function toSysLog(level) {
  var n = core.levels[level];

  if (n <= 0) return 2; // fatal -> critical
  if (n === 1) return 3; // error -> error
  if (n === 2) return 4; // warn -> warning
  if (n === 3) return 6; // info -> info (no notice/verbose)
  return 7; // debug -> debug
};

// convert from a syslog log level to a loggins log level
exports.fromSyslog = function fromSysLog(n) {
  if (n >= 7) return core.priorities[4]; // debug -> debug
  if (n === 6) return core.priorities[3]; // info -> info
  if (n >= 4) return core.priorities[2]; // notice, warning -> warn
  if (n == 3) return core.priorities[1]; // error -> error
  return core.priorities[0]; // anything higher is fatal
};
