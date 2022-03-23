#!/usr/bin/env node

'use strict';

const fs = require('fs');
const os = require('os');
const path = require('path');
const { spawn } = require('child_process');

const find = require('./find');

module.exports = viu;

async function viu(...argv) {
  const bin = await find(true);

  const proc = spawn(bin, argv, { stdio: 'inherit' });

  return new Promise((resolve, reject) => {
    proc.on('exit', (code) => {
      if (code) {
        reject(new Error(`viu exited with code ${code}`));
      } else {
        resolve(null);
      }
    });
  });
}
