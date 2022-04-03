#!/usr/bin/env node

const { app } = require('../');

app(process.argv.slice(2), async (opts) => {
  console.log(`hello ${opts.message}`);
});
