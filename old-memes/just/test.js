const path = require('path');

const { test } = require('tap');

const { Just } = require('.');

const JUSTFILE = path.join(__dirname, 'justfile');

const DUMP = require('./dump.json');

const just = new Just(JUSTFILE);

test('running commands', async (assert) => {
  assert.doesNotThrow(async () => await just.run('hello', 'world'), "can execute a just recipe with a parameter")
});

test('dumping the justfile', async (assert) => {
  assert.same(await just.dump(), DUMP, 'can get a dump of the justfile');
  assert.same(just.dumpSync(), DUMP, 'can get a dump of the justfile synchronously');
});

test('gulp registry', async (assert) => {
  assert.doesNotThrow(async () => await just.run('test'), 'can expose tasks to gulp');
});
