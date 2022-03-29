const fs = require('fs');
const { open } = require('fs/promises');
const { promisify } = require('util');
const close = promisify(fs.close);
const write = promisify(fs.write);

const { test } = require('tap');
const { discuss } = require('../');

test('my first swears test', async (assert) => {
  assert.test('when we open a file', async (assert) => {
    const fileTopic = discuss(async () => {
      const file = await open('/tmp/fakefile', 'w');
      return file.fd;
    }, async (file) => {
      await close(file);
    });

    assert.test('it works', async (assert) => {
      await fileTopic.swear(async (file) => {
        assert.ok(file);
      });
    });

    assert.test('and we write to the file', async (assert) => {
      const writeTopic = fileTopic.discuss(async (file) => {
        await write(file, "My dog has fleas\n");
        return file
      });

      assert.test('it works', async (assert) => {
        await writeTopic.swear(async (file) => {
          assert.ok(file);
        });
      });
    });
  });
});
