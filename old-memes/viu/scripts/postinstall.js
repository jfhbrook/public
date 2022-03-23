#!/usr/bin/env node

'use strict';

const { execSync } = require('child_process');

const find = require('../find');

async function postinstall() {
  try {
    const bin = await find();
    console.log(`viu found at: ${bin}`);
  } catch (err) {
    console.log('attempting to build viu...');
    try {
      execSync('cd vendor/viu-1.4.0 && cargo build --release', { stdio: 'inherit' });
    } catch (err) {
      console.log('could not build vui:');
      console.log(err);
    }
  }
}

postinstall();
