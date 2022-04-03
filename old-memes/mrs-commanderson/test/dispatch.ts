/*
 * dispatch-test.ts: Tests for the core dispatch method.
 *
 * (C) 2022, Josh Holbrook.
 * (C) 2011, Charlie Robbins, Paolo Fragomeni, & the Contributors.
 * MIT LICENSE
 *
 */

import { test } from 'tap';
import { discuss } from '@jfhbrook/swears';
import { Router } from '../router';

type Ctx = {};

/*
 * The router object is a combination of director's core router and the
 * CLI router subclass. As such, its behavior deviates significantly from the
 * core router! As far as I can tell that new behavior is sighificantly
 * simplified. Therefore, I run the (passing) CLI tests for now, with getting
 * the more general tests to pass being a bit of a TODO.
 */
type CliMatched = {
  users: string[];
  apps: string[];
};

type CoreMatched = {
  '<root>': string[];
  'foo': string[];
  'f*': string[];
};

test('router/dispatch', async (assert) => {
  assert.test('(the cli version)', async (assert) => {
    const topic = discuss(async () => {
      const router = new Router<Ctx>();

      const matched: CliMatched = {
        users: [],
        apps: []
      };

      router.on('users create', async () => {
        matched.users.push('on users create');
      });

      router.on(/apps (\w+\s\w+)/, async () => {
        matched.apps.push('on apps (\\w+\\s\\w+)');
      });

      return {
        matched,
        router
      };
    });

    assert.test('should have the correct routing table', async (assert) => {
      await topic.swear(async ({ router }) => {
        assert.ok(router.routes.users.create);
      });
    });

    assert.test('the dispatch() method', async (assert) => {
      assert.test('users create', async (assert) => {
        await topic.swear(async ({ router }) => {
          assert.ok(await router.dispatch('on', 'users create', {}));
        });
      });

      assert.test('apps foo bar', async (assert) => {
        await topic.swear(async ({ matched, router }) => {
          assert.ok(await router.dispatch('on', 'apps foo bar', {}));
          assert.same(matched.apps, ['on apps (\\w+\\s\\w+)']);
        });
      });

      assert.test('not here', async (assert) => {
        await topic.swear(async ({ router }) => {
          assert.notOk(await router.dispatch('on', 'not here', {}));
        });
      });

      assert.test('still not here', async (assert) => {
        await topic.swear(async ({ router }) => {
          assert.notOk(await router.dispatch('on', 'still not here', {}));
        });
      });
    });
  });

  assert.skip('(the core version)', async (assert) => {
    assert.test("An instance of Router", async (assert) => {
      const routerTopic = discuss(async () => {
        const matched: CoreMatched = {
          '<root>': [],
          'foo': [],
          'f*': []
        }

        // TODO: these spaces are a wart, how do I fix them?
        const router = new Router<Ctx>({
          '': {
            before: async () => { matched['<root>'].push('before /') },
            on: async () => { matched['<root>'].push('on /') },
            after: async () => { matched['<root>'].push('after /') }
          },
          'foo': {
            before: async () => { matched.foo.push('before foo') },
            on: async () => { matched.foo.push('on foo') },
            after: async () => { matched.foo.push('after foo') },
            'bar': {
              before: async () => { matched.foo.push('before foo bar') },
              on: async () => { matched.foo.push('foo bar') },
              after: async () => { matched.foo.push('after foo bar') },
              'buzz': async () => { matched.foo.push('foo bar buzz') }
            }
          },
          'f*': {
            'barbie': async () => { matched['f*'].push('f* barbie') }
          }
        });

        router.configure({
          recurse: 'backward'
        });

        return {
          matched,
          router
        };
      });

      assert.skip("should have the correct routing table", async (assert) => {
        await routerTopic.swear(async ({ router }) => {
          // TODO: the actual data structure in routes is weird, it's like
          // super flattened, it's not what's supposed to be here. Something is
          // quite wrong - I think I want to copy-paste the original definitions
          // back in and look over changes to make sure I'm not being disappointed
          // anywhere ;)
          assert.ok(router.routes.foo, 'should have a "foo" route');
          assert.ok(router.routes.foo.bar, 'should have a "foo bar" route');
          assert.ok(router.routes.foo.bar.buzz, 'should have a "foo bar buzz" route');
          assert.ok(router.routes.foo.bar.buzz.on, 'should have an "on" handler on the "foo bar buzz" route');
        });
      });

      assert.skip("the dispatch() method", async (assert) => {
        assert.skip("<root>", async (assert) => {
          await routerTopic.swear(async ({ matched, router }) => {
            assert.ok(await router.dispatch('', {}));
            assert.ok(await router.dispatch('', {}));

            assert.same(matched, {
              '<root>': ['before /', 'on /', 'after /'],
              'foo': [],
              'f*': []
            });
          });
        });

        assert.test("foo bar buzz", async (assert) => {
          await routerTopic.swear(async ({ matched, router }) => {
            assert.ok(await router.dispatch('foo bar buzz', {}), 'dispatch to "foo bar buzz" is successful');

            assert.same(matched, {
              '<root>': [],
              'foo': ['foo bar buz', 'before foo bar', 'foo bar', 'before foo', 'on foo' ],
              'f*': []
            });
          });
        });

        assert.skip("foo barbie", async (assert) => {
          await routerTopic.swear(async ({ matched, router }) => {
            assert.ok(await router.dispatch('foo barbie', {}));

            assert.same(matched, {
              '<root>': [],
              'foo': [''],
              'f*': ['f* barbie']
            });
          });
        });

        assert.skip("foo barbie ", async (assert) => {
          await routerTopic.swear(async ({ router }) => {
            assert.notOk(await router.dispatch('foo barbie ', {}));
          });
        });

        assert.skip("foo BAD", async (assert) => {
          await routerTopic.swear(async ({ router }) => {
            assert.notOk(await router.dispatch('foo BAD', {}));
          });
        });

        assert.skip("bar bar", async (assert) => {
          await routerTopic.swear(async ({ router }) => {
            assert.notOk(await router.dispatch('bar bar', {}));
          });
        });
        
        assert.skip("with the strict option disabled", async (assert) => {
          const nonStrictTopic = routerTopic.discuss(async ({ matched, router }) => {
            router.configure({
              recurse: 'backward',
              strict: false
            });

            return { matched, router };
          });

          assert.test("should have the proper configuration set", async (assert) => {
            await nonStrictTopic.swear(async ({router}) => {
              assert.notOk(router.strict);
            });
          });
          
          assert.test("foo barbie ", async (assert) => {
            await nonStrictTopic.swear(async ({ matched, router }) => {
              assert.ok(await router.dispatch('on', 'foo barbie '));
              assert.equal(matched['f*'][0], 'f* barbie');
            });
          });

          assert.test("foo bar buzz", async (assert) => {
            await nonStrictTopic.swear(async ({ matched, router }) => {
              assert.ok(await router.dispatch('on', 'foo bar buzz'));

              assert.equal(matched.foo[0], 'foo bar buzz');
              assert.equal(matched.foo[1], 'before foo bar');
              assert.equal(matched.foo[2], 'foo bar');
              assert.equal(matched.foo[3], 'before foo');
              assert.equal(matched.foo[4], 'on foo');
            });
          });
        });
      });
    });
  });
});
