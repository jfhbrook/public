const { exec: execNodeback, spawn } = require('child_process');
const { promisify } = require('util');

const exec = promisify(execNodeback);

class JustError extends Error {
  constructor(argv, code) {
    super(`just ${argv.join(' ')} exited with code ${code}`);
    this.argv = argv;
    this.code = code;
  }
}

class Just {
  constructor(justfile, env = process.env, cwd = process.cwd()) {
    this._justfile = justfile;
    this._env = env;
    this._cwd = cwd;
  }

  just(...args) {
    return new Promise((resolve, reject) => {
      const argv = ['-f', this._justfile].concat(args);
      const p = spawn('just', argv, {
        env: this._env,
        cwd: this._cwd,
        stdio: 'inherit'
      });
      p.on('exit', (code) => {
        if (code) {
          reject(new JustError(argv, code));
        } else {
          resolve();
        }
      });
    });
  }

  async recipes() {
    const {
      stdout,
      stderr
    } = await exec('just --unstable --dump --dump-format json', {
      env: this._env,
      cwd: this._cwd
    });

    if (stderr && stderr.length) {
      // TODO: process.logging lol
      console.error(stderr);
    }

    return JSON.parse(stdout.toString()).recipes;
  }
}

module.exports = {
  Just,
  JustError
};
