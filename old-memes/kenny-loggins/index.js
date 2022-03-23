var winston = require('winston');

var core = require('./core');

exports.levels = core.levels;
exports.colors = core.colors;
exports.priorities = core.priorities;
exports.MIN_LEVEL = core.MIN_LEVEL;
exports.MAX_LEVEL = core.MAX_LEVEL;

exports.observe = function observe(logger, level) {
  level = level || 'debug';

  // If process.logging isn't defined, bounce
  if (!process.logging) return;
  if (!process.logging.observe) {
    logger.warn(
      'process.logging.observe is undefined - are you using @jfhbrook/logref?'
    );
    return;
  }

  process.logging.observe(function onLog(log) {
    log.on('log', function logToWinston(msg, ctx) {
      var event = {
        level: level,
        message: (log.formatter || process.logging.formatter)(msg, ctx),
        logging: {
          name: log.name
        }
      };

      Object.keys(ctx).forEach(function (k) {
        event[k] = ctx[k];
      });

      logger.log(event);
    });
  });
};

exports.formatter = winston.format.cli({colors: core.colors});

exports.Logger = winston.Logger;

exports.createLogger = function createLogger(opts) {
  opts = opts || {};

  var meta = opts.meta || {};
  var level = opts.level || 'info';
  var logrefLevel = (opts.logref || {}).level || 'debug';

  var tx = new winston.transports.Console();

  let formatter = exports.formatter;
  if (opts.colors) {
    formatter = winston.format.cli({colors: opts.colors});
  }

  var logger = winston.createLogger({
    level: opts.level,
    levels: core.levels,
    format: formatter,
    defaultMeta: meta,
    transports: [tx],
    exceptionHandlers: [tx],
    rejectionHandlers: [tx]
  });

  exports.observe(logger, logrefLevel);

  return logger;
};
