#!/usr/bin/env node

const { App } = require('../');

const app = new App();

app.command("init", async (ctx) => {
  console.log('init:', ctx);
});
app.command("install :pkg", async (ctx, pkg) => {
  console.log('install:', pkg, ctx);
});

app.run(process.argv.slice(2));
