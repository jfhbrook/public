const { inspect } = require('util');

const colors = require('ansi-colors');

let shrug = false;
let shellMode = false;
let logger = null;

exports.setShrug = function (_shrug) {
  shrug = _shrug;
}

exports.setShellMode = function (_shellMode) {
  shellMode = _shellMode;
}

exports.setLogger = function (_logger) {
  logger = _logger;
}


exports.greatSuccess = greatSuccess;
exports.flagrantError = flagrantError;
exports.falconPunch = falconPunch;

function greatSuccess() {
  if (!shellMode) {
    logger.info(colors.green('ok'));
  }
  process.exit(0);
}

function flagrantError(err) {
  // errors have a highlight designed for a BSOD, not appropriate for a
  // warning
  if (!shrug) {
    const { green, grey, red, yellow, white } = inspect.colors;
    inspect.styles = {
      bigint: yellow,
      boolean: yellow,
      date: yellow,
      module: yellow,
      name: yellow,
      null: red,
      number: yellow,
      regexp: red,
      special: red,
      string: green,
      symbol: red,
      undefined: grey
    };
  }

  // the stack is meaningless in shell mode
  let message = shellMode ? colors.white(String(err)) : inspect(err, { colors: true });

  // find the width of the message string
  let width = message.split('\n').reduce((n, l) => Math.max(l.length, n), 0) + 8;

  // split and add padding
  message = message.split('\n').map(l => {
    return '    ' + l + (' '.repeat(width - l.length - 4));
  });

  // be less shouty on a shrug
  let header = shrug ? 'houston, we got a problem!! ' : 'FLAGRANT ERROR';
  header = (
    ' '.repeat(Math.floor((width - header.length) / 2))
    + header
    + ' '.repeat(Math.ceil((width - header.length) / 2))
  );

  // stack 'em to the heavens!
  message = [
    ' '.repeat(width),
    header,
    '-'.repeat(width),
    ' '.repeat(width)
  ].concat(message).concat([
    ' '.repeat(width),
    '-'.repeat(width)
  ]);

  // in shrug
  if (shrug) {
    message.forEach(l => {
      logger.warn(colors.yellow(l));
    });
  } else {
    message.forEach(l => {
      logger.error(colors.bgBlue(l));
    });
  }

  // let the parent process log exit
  if (!shellMode && shrug) {
    logger.warn('ok ' + colors.yellow('~despite errors~'));
    process.exit(0);
  }

  if (!shellMode) {
    logger.error(colors.red('not') + ' ok');
    process.exit(1);
  }
}

function falconPunch() {
  // Hook the entire world to muh error handling lol
  process.on('uncaughtException', flagrantError);
  process.on('unhandledRejection', flagrantError);

  // gotta do everything myself!!
  Promise.prototype.done = function () {
    this.then(greatSuccess, flagrantError);
  }
}


