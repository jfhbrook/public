import winston from 'winston';

import * as core from './core';

export const levels = core.levels;
export const colors = core.colors;
export const priorities = core.priorities;
export const MIN_LEVEL = core.MIN_LEVEL;
export const MAX_LEVEL = core.MAX_LEVEL;

export function observe(logger: winston.Logger, level?: string) {
  const lvl = level || 'debug';

  const logging = (process as any).logging;

  // If process.logging isn't defined, bounce
  if (!logging) return;
  if (!logging.observe) {
    logger.warn(
      'process.logging.observe is undefined - are you using @jfhbrook/logref?'
    );
    return;
  }

  logging.observe(function onLog(log: any) {
    log.on('log', function logToWinston(msg: string, ctx: any) {
      var event: any = {
        level: lvl,
        message: (log.formatter || logging.formatter)(msg, ctx),
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
}

export const formatter = winston.format.cli({colors: core.colors});

export const Logger = winston.Logger;

export function createLogger(opts: any) {
  opts = opts || {};

  var meta = opts.meta || {};
  var level = opts.level || 'info';
  var logrefLevel = (opts.logref || {}).level || 'debug';

  var tx = new winston.transports.Console();

  let format = formatter;
  if (opts.colors) {
    format = winston.format.cli({colors: opts.colors});
  }

  var logger = winston.createLogger({
    level,
    levels: core.levels,
    format,
    defaultMeta: meta,
    transports: [tx],
    exceptionHandlers: [tx],
    rejectionHandlers: [tx]
  });

  observe(logger, logrefLevel);

  return logger;
}
