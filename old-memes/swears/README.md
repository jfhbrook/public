# swears
## a fixture generator inspired by [vows](https://github.com/vowsjs/vows)

## background

I found myself porting vows tests to [tap](https://node-tap.org/). vows was the
test framework that we used at nodejitsu, and all of the old code from then is
tested with it. the truth is that we all hated it - we thought it was clunky
and baroque as compared to tap (or heaven forbid [mocha](https://mochajs.org/)).
but I also thought the core abstraction was being lost on us. perhaps that was
having faith in our architects ;) but being in those tests today, I think I've
identified the part of vows that's, if not *good*, then at least *ok, sometimes.*

vows structures its tests as **batches** of assertion suites executed against
**topics**. these topics are effectively fixture generators, and the batches
are effectively a group of tests that operate on the test's fixture.
this is a structure common with behavior-driven development - 
"given ${TOPIC}, ${X} and ${Y}".

vows is extremely opinionated about this test structure, and if your mental
model for your tests doesn't map to BDD very well then you'll have a bad time.
this is really the core to why people got grouchy about vows. truth be told,
the `this`-oriented DSL didn't age well either [1].

but suppose you *are* in a situation where you want to stand up a fixture or
two and run a suite of tests against instances of that fixture. you could
create and tear down the fixture using
[before/after hooks in your test framework](https://node-tap.org/docs/api/test-lifecycle-events/),
but I find that sort of thing is a little clunky when used to manage fixtures.

this is the thing that vows really shines at. it's able to specify how to
create a test fixture, and the test harness manages creating and tearing
down that fixture for each batch of tests. the problem, as it were, is that
vows couples fixture creation with test suites and test harnesses.

what I did here was write a very lightweight abstraction which implements a
2022 spin of the idea of vows' topics, without the test harness. instead, you
may use your test framework of choice - such as tap. this gets me the benefits
of the vows setup/teardown DSL, while using my favored test framework, and
in what counts as idiomatic javascript today.

## enough blabbing, what does this look like?

ok - here's the [first vows example](https://github.com/vowsjs/vows#example)
ported to use swears:

```javascript
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

```

this example first creates a parent topic by opening a file (with surprisingly
low-level APIs which must've been all they had when cloudhead was writing node),
and the first test asserts that the file handle was successfully returned.
then, a child topic writes to the file, and a child test asserts that it was
successful. the fixture is created anew with each "swear" block, and the
teardown hook is run after such blocks are run. this all happens without
coupling the fixtures to the test harness, and without using a `this`-oriented
DSL.

if you use typescript (like I do, on occasion), you might appreciate this
example as well:

```typescript
import { test } from 'tap';
import { discuss } from '../';

interface Discourse {
  spiceLevel: number;
}

test('when engaging with the discourse', async (assert) => {
  const topic = discuss<Discourse>(async () => {
    return { spiceLevel: 0 };
  });

  assert.test('and the discourse gets rowdy', async (assert) => {
    const spicierTopic = topic.discuss<Discourse>(async (discourse) => {
      discourse.spiceLevel++;
      return discourse;
    });

    assert.test('things get a little spicy', async (assert) => {
      await spicierTopic.swear(async (discourse) => {
        assert.equal(discourse.spiceLevel, 1);
      });
    });
  });
});

```

scenario aside, this is very similar to the file example. Note that `discuss`
and `Topic.discuss` are parameterized by a type `T`, and that a child topic
may return a topic of a different type `U`. in other words, swears should be
type safe.

## development

swears is written in typescript, but that should have minimal effect on this
project, as run-scripts generally start by calling `tsx`. even so, be prepared
for thinking in types!

### install

nothing surprising here - `npm i` will do the trick!

### test

`npm test` will run `tsx` and then execute `test.ts` and the examples with
tap. you shouldn't ever accidentally run tests against old typescript, and the
examples shouldn't break on accident.

### build

most npm run-scripts will automatically call `tsx` as appropriate, but if you
want to run it yourself, try `npx tsx`.

### docs

I'm using [exercise-bike](https://npm.im/exercise-bike) to generate the README
through a nunjucks template, which copies in the examples from the `examples`
folder. basically: edit `README.md.njk`, then run `npm run doc` to update the
README. note that this will automatically run before a publish.

## license

swears is being released under an MIT license. for more info, check out the
LICENSE file.

## footnotes

[1] when vows was written, ruby-based DSLs were *all the rage* and everyone
working in dynamic languages was trying to emulate them. it sure seemed like
chainable APIs and binding `this` in callbacks was a similar trick to ruby's
`do` syntax. vows, like almost every library from its time, discovered the hard
way that this is a worse idea than it sounds. we live and learn!

