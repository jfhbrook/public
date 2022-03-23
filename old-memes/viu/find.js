#!/usr/bin/env node

'use strict';

const fs = require('fs');
const { promisify } = require('util');
const os = require('os');
const path = require('path');
const { spawn } = require('child_process');

const which = require('which');

const exists = promisify(fs.exists);

module.exports = find;

async function find(sysemOk = false) {
  // First, see if npm built it from source
  let bin = path.join(
    __dirname,
    "vendor",
    "viu-1.4.0",
    "target",
    "release",
    "viu"
  );

  if (os.platform() === "windows") {
    bin += ".exe";
  }

  if (!await exists(bin)) {
    // If not, see if we have a pre-built cross-compiled binary
    const target = {
      "linux": {
        "arm": "armv7-unknown-linux-gnueabihf",
        "arm64": "aarch64-unknown-linux-gnu",
        "x64": "x86_64-unknown-linux-gnu"
      },
      "windows": {
        "x64": "x86_64-pc-windows-gnu"
      }
    }[os.platform()][os.arch()];

    if (target) {
      bin = path.join(
        __dirname,
        "vendor",
        "viu-1.4.0",
        "target",
        target,
        "release",
        "viu"
      );

      if (os.platform() === "windows") {
        bin += ".exe";
      }
    }
  }

  if (!await exists(bin)) {
    if (systemOk) {
      // last-ditch effort, check if it's already installed on the PATH
      bin = await which('viu');
    } else {
      throw new Error('could not find viu');
    }
  }

  return bin;
}
