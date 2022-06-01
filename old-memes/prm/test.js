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

skip('parseFile', async (assert) => {
  assert.fail('TODO: write a parseFile test or two');
});

skip('parseArgs', async (assert) => {
  assert.fail('TODO: write tests for --only flags');
});

skip('createEnv', async (assert) => {
  assert.fail('TODO: write a createEnv test');
});
