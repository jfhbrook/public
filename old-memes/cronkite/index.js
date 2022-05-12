const path = require('path');
const { promisify } = require('util');
const exec = promisify(require('child_process').exec);

const bole = require('@entropic/bole');
const cron = require('node-cron');
const minimist = require('minimist');

const LOG_FORMAT = {
  PRETTY: 'pretty',
  JSON: 'json'
}


const STATUS = {
  STOPPED: 'stopped',
  WAITING: 'waiting',
  RUNNING: 'running'
}

function createScheduler(crontab) {
  const scheduler = {
    jobs: [],
    start() {
      for (let job of this.jobs) {
        job.start();
      }
    },
    stop() {
      for (let job of this.jobs) {
        job.stop();
      }
    }
  };

  crontab.forEach(([schedule, command], id) => {
    const name = `(${id}) "${schedule} ${command}"`
    const log = bole(name);

    const job = {
      id,
      name,
      log,
      scheduler,
      task: null,
      status: STATUS.STOPPED,
      start() {
        this.status = STATUS.WAITING;

        log.info('scheduling');
        this.task = cron.schedule(schedule, async () => {
          if (this.status === STATUS.RUNNING) {
            log.warn('still running from last start D:');
          } else {
            this.status = STATUS.RUNNING;

            log.info('starting job...');
            try {
              const { stdout, stderr } = await exec(command);
              log.info('finished successfully');
              log.debug('stdout', stdout);
              log.debug('stderr', stderr);
            } catch (err) {
              log.error('failed with an error', err);
            }
            this.status = STATUS.WAITING;
            log.debug(`status: ${this.status}`);
          }
        });
      },
      stop() {
        if (this.task) {
          this.task.stop();
        }
        this.status = STATUS.STOPPED;
      }
    };

    scheduler.jobs.push(job);
  });

  return scheduler;
}

function help() {
  console.log(`USAGE: cronkite [CONFIG_FILE]`);
}

function main(argv = process.argv, env = process.env) {
  const opts = minimist(argv, {
    boolean: [
      'help',
      'verbose',
      'quiet'
    ],
    string: [
      'format'
    ],
    alias: {
      h: ['help'],
      v: ['verbose'],
      q: ['quiet']
    },
    default: {
      format: 'pretty'
    }
  });

  if (opts.help) {
    help();
    return;
  }

  const configFile = opts.config || env.CRONKITE_CONFIG || './crontab.json';
  const config = require(path.resolve(configFile));

  let level = 'info';
  let format = opts.format;

  // TODO: config in file + increase/decrease log level
  if (env.LOG_LEVEL) {
    level = env.LOG_LEVEL;
  } else if (opts.verbose) {
    level = 'debug'
  } else if (opts.quiet) {
    level = 'warn'
  }

  let stream = process.stdout;
  if (format === LOG_FORMAT.PRETTY) {
    const pretty = require('bistre')({ time: true });
    pretty.pipe(stream);
    stream = pretty;
  } else if (format !== LOG_FORMAT.JSON) {
    throw new Error(`Unknown format: ${format}`);
  }

  bole.output({
    level: level || process.env.LOG_LEVEL || 'debug',
    stream
  });

  const scheduler = createScheduler(config.crontab);

  scheduler.start();
}

module.exports = {
  createScheduler,
  main
}
