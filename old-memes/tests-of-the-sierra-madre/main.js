#!/usr/bin/env node

'use strict';

const viu = require('@jfhbrook/viu');

const os = require('os');
const path = require('path');
const fs = require('fs');

const SHORT = !!process.env.SHORT;
const DEBUG = !!process.env.DEBUG;

// https://imgflip.com/i/69n5qj
const jpeg = path.join(__dirname, "macro.jpg")

function short() {
  console.log('"Tests? We ain\'t got no tests!"');
}

async function main() {
  if (SHORT) {
    short();
    return
  }
  try {
    await viu(jpeg);
  } catch (err) {
    if (DEBUG) {
      console.error(err);
    }

    const { default: terminalImage } = await import('terminal-image');
    console.log(await terminalImage.file(jpeg, simple));
  }
}

main();
