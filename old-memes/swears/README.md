# swears
## a fixture generator inspired by [vows](https://github.com/vowsjs/vows)

I found myself porting vows tests to [tap](https://node-tap.org/). vows was the
test framework that we used at nodejitsu, and all of the old code from then is
tested with it. the truth is that we all hated it - we thought it was clunky
and baroque as compared to tap (or heaven forbid [mocha](https://mochajs.org/)).
but I also thought the core abstraction was being lost on us. perhaps that was
having faith in our architects ;) but being in those tests today, I think I've
identified the part of vows that's of not *good*, then at least *ok, sometimes.*

vows structures its tests as batches of assertion suites executed against
"topics" - `given ${topic},` yadda yadda. these topis can have child topics,
and the topics all have hooks for setup and teardown.

for the most part, tap has you covered for concurrency patterns. it does all
sorts of scary shit if you let it, but is happy to execute boring coroutines
too. but it doesn't necessarily handle creating fixtures themselves.

ok, so fine, we can create an object with a factory. in swears, the start of
that might look like this (loosely ported from the vows example):

```javascript
const { readFile } = require('fs/promises');

const { test } = require('tap');
const { when } = require('@jfhbrook/swears');

test('when we read a file', async (assert) => {
  const topic = when(async () => {
    const file = await readFile('/tmp/fakefile');
  });

  assert.test('it works', async (assert) => {
    await topic.swear(async (file) => {
      assert.ok(file);
    });
  });
});
```

like vows, you can also make child topics:

```javascript
const { test } = require('tap');
const { when } = require('@jfhbrook/swears');

test('when Engaging with the Discourse, Online,,', async (test) => {
  const topic = when(async () => {
    return { spiceLevel: 0 };
  });

  test('when the discourse gets rowdy', async (assert) => {
    const spicierTopic = await topic.when(async (discourse) => {
      discourse.spiceLevel++;
      return discourse;
    });

    test('things get a little spicy', async (assert) => {
      await spicierTopic.swear(async (discourse) => {
        assert.equal(discourse.spiciness, 1);
      });
    });
  });
});
```

TODO: like vows, these will also support teardown :)

TODO: finish writing this

## license

MIT
