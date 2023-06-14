#!/usr/bin/env node

const minimist = require('minimist');
const http = require('http');
const fs = require('fs');
const path = require('path');
const util = require('util');
const url = require('url');

const colors = require('ansi-colors');
const progress = require('stream-progressbar');

const USAGE = 'USAGE: bbgurl URL [OPTIONS]';

const HELP = `bbgurl: a cli http client using undici

${USAGE}

make an HTTP request using undici.request.

most undici options are bled straight through the args, using conventions
from the optimist and minimist libraries.

for more information on undici, see: https://npm.im/undici

OPTIONS:
    --help                   print this message.

    -Q/--quiet               suppress logging.

    -X/--method METHOD       an http method. defaults to GET.

    --body BODY              the request body. if the first character is a @,
                             will read from file. defaults to stdin.

    --headers HEADERS        a JSON blob representing an undici headers
                             argument. defaults to null.

    --upgrade UPGRADE        optionally upgrade the request with the specified
                             upgrade type.

    --bodyTimeout MILLIS     how long to wait for the body before timing out.
                             defaults to 30 seconds.

    --headersTimeout MILLIS  how long to wait for the headers before timing
                             out. defaults to 30 seconds.

    --maxRedirections N      the maximum number of redirects to follow.

    --mixin MIXIN            if specified, call the appropriate fetch mixin on the body.

    -i/--include             include response status, headers and trailers.

    --logfile FILE           an optional file to write logs to.

    -o/--output FILE         a file to write the response to. defaults to stdout.

    -U/--user CREDENTIALS    specify basic auth credentials. ex: '-u user:pass'
`;

function parseArgs(argv) {
  const opts = minimist(argv, {
    string: [
      'method',
      'body',
      'headers',
      'upgrade',
      'bodyTimeout',
      'headersTimeout',
      'maxRedirections',

      'mixin',
      'logfile',
      'output',
      'user'
    ],
    boolean: [
      'idempotent',
      'blocking',

      'help',
      'quiet',
      'verbose',
      'include'
    ],
    alias: {
      method: 'X',
      body: 'd',
      headers: 'H',
      include: 'i',
      output: 'o',
      user: 'u',
      quiet: 'Q'
    },
    default: {
      include: false,
      verbose: true
    }
  });

  let _url = opts._.length ? url.parse(opts._.join(' ')) : null;

  if (opts.user) {
    _url.auth = opts.user;
  }

  const undiciOptions = {
    method: opts.method,
    headers: opts.headers ? JSON.parse(opts.headers) : undefined,
    idempotent: opts.idempotent,
    blocking: opts.blocking,
    bodyTimeout: opts.bodyTimeout ? parseInt(opts.bodyTimeout, 10) : undefined,
    headerstimeout: opts.headersTimeout ? parseInt(opts.headersTimeout, 10) : undefined,
    maxRedirections: opts.maxRedirections ? parseInt(opts.maxRedirections, 10) : undefined
  };

  if (opts.body && opts.body[0] === '@' && fs.existsSync(opts.body.slice(1))) {
    undiciOptions.body = fs.createReadStream(opts.body.slice(1));
  } else if (opts.body) {
    undiciOptions.body = opts.body;
  } else if (opts.method && opts.method !== 'GET') {
    undiciOptions.body = process.stdin;
  }

  const appOptions = {
    output: opts.output ? fs.createWriteStream(opts.output) : process.stdout,
    outputFile: opts.output ? path.resolve(opts.output) : null,
    help: opts.help,
    quiet: opts.quiet,
    verbose: !opts.quiet,
    include: opts.include,
    logfile: opts.logfile,
    mixin: opts.mixin
  };

  return [[ _url, undiciOptions], appOptions ];
}

class IOManager {
  constructor(opts) {
    this.output = opts.output;

    this._print = () => {};

    if (opts.verbose && !opts.logfile) {
      this._log = console.error;
    } else if (opts.logfile) {
      this._logfile = fs.createWriteStream(path.resolve(opts.logfile));
      this._log = (message, ...params) => {
        this._logfile.write(util.format(message, ...params) + '\n');
      };
    }

    if (opts.outputFile !== process.stdin) {
      this.output.on('close', () => {
        this.log('data written to %s', opts.outputFile);
      });
    }
  }

  log(message, ...params) {
    this._log(`[${colors.magenta('♥')}] ${message}`, ...params);
  }

  printLn(message, ...params) {
    this.output.write(
      (
        message
        ? util.format(message, ...params)
        : ''
      ) + '\r\n'
    );
  }

  usage() {
    this.log(USAGE);
    this.log('');
    this.log('For more information, run "bbgurl --help".');
  }

  help() {
    HELP.split('\n').forEach((line) => {
      this.log(line);
    });
  }

  printStatus(statusCode) {
    this.printLn(`HTTP ${statusCode} ${http.STATUS_CODES[statusCode]}`);
  }

  printHeaders(headers) {
    Object.entries(headers).forEach(([key, value]) => {
      this.printLn('%s: %s', key, value);
    });
    this.printLn();
  }
}

async function main() {
  const [[url, undiciOpts], appOpts] = parseArgs(process.argv.slice(2));
  const io = new IOManager(appOpts);

  if (appOpts.help) {
    io.help();
    return;
  }

  if (!url) {
    io.usage();
    process.exit(1);
  }

  const undici = await import('undici');

  const showProgress = !appOpts.mixin && appOpts.verbose;

  const {
    statusCode,
    headers,
    trailers,
    body
  } = await undici.request(url, undiciOpts);

  if (appOpts.include) {
    io.printStatus(statusCode);
    io.printHeaders(headers);
  }

  let total = null;

  try {
    total = parseInt(headers['content-length'], 10);
  } catch (err) {}

  if (appOpts.mixin) {
    io.printLn(await body[appOpts.mixin]());
    printTrailers();
  } else {
    let res = body;
    if (showProgress && total) {
      res = res.pipe(
        progress(
          `[${colors.magenta('♥')}] Downloading: :bar :percent (:current/:total)`,
          { total, width: 40 }
        )
      );
    }

    res.pipe(appOpts.output);

    res.on('end', printTrailers);
  }

  function printTrailers() {
    if (appOpts.include) {
      io.printHeaders(trailers);
    }
  }
}

module.exports = {
  parseArgs,
  IOManager,
  main
};
