const { readFile } = require('fs/promises');
const path = require('path');

const { skip, test } = require('tap');

const { createEnv, parseFile, getActions, getFeatures, parseArgs } = require('./prm');

// TODO: these tests may be too volatile - after all, if they're static, why
// would I get reflecty with it?

test('getFeatures', async (assert) => {
  const features = await getFeatures();
  assert.same(features, [
    "copr",
    "npm"
  ]);
});

test('getActions', async (assert) => {
  const actions = await getActions();
  assert.same(actions, {
    "copr-get": {  
      name: "copr-get", 
      feature: "copr",  
      verb: "get",      
    },                    
    "copr-set": {  
      name: "copr-set", 
      feature: "copr",  
      verb: "set",      
    },                    
    "npm-set": {   
      name: "npm-set",  
      feature: "npm",   
      verb: "set",      
    }
  });
});

test('parseFile', async (assert) => {
  const file = await readFile(path.join(path.dirname(__filename), 'prm.sh'), 'utf8');
  assert.ok(parseFile(file), 'example parses without crashing');
});

test('parseArgs', async (assert) => {
  const opts = await parseArgs(['apply', '--copr-only']);
  assert.ok(opts, 'apply --copr-only parses without crashing');
});

skip('createEnv', async (assert) => {
  // TODO: once parseArgs tests has some fixtures, pass them to createEnv and
  // ensure the right result
});
