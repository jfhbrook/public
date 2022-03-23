var core = require('./core');

// A helper to take --verbose and -v flags from minimist and use them to
// adjust the level
exports.verbosity = function verbosity(opts, defaultLevel) {
  if (opts['log-level']) {
    if (typeof core.levels[opts['log-level']] !== 'number') {
      throw new Error('invalid log level!');
    }
    return opts['log-level'];
  }

  var adjustedLevel = core.levels[defaultLevel];

  if (opts.v || opts.verbose) {
    return core.priorities[
      Math.max(
        core.levels[core.MIN_LEVEL],
        Math.min(core.levels[core.MAX_LEVEL], core.levels[defaultLevel] + 1)
      )
    ];
  }

  return core.priorities[adjustedLevel];
};
