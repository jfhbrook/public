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

type Matched = {
  '<root>': string[];
  'foo': string[];
  'f*': string[];
};

test('router/dispatch', async (assert) => {
  assert.test("An instance of Router", async (assert) => {
    const routerTopic = discuss(async () => {
      const matched: Matched = {
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

    assert.test("should have the correct routing table", async (assert) => {
      await routerTopic.swear(async ({ router }) => {
        assert.ok(router.routes.foo, 'should have a "foo" route');
        assert.ok(router.routes.foo.bar, 'should have a "foo bar" route');
        assert.ok(router.routes.foo.bar.buzz, 'should have a "foo bar buzz" route');
        assert.ok(router.routes.foo.bar.buzz.on, 'should have an "on" handler on the "foo bar buzz" route');
      });
    });

    assert.test("the dispatch() method", async (assert) => {
      assert.skip("<root>", async (assert) => {
        await routerTopic.swear(async ({ matched, router }) => {
          assert.ok(await router.dispatch('', {}));
          assert.ok(await router.dispatch('', {}));

          assert.ok(matched['<root>'][0], 'before /');
          assert.equal(matched['<root>'][1], 'on /');
          assert.equal(matched['<root>'][2], 'after /');
        });
      });

      assert.test("foo bar buzz", async (assert) => {
        await routerTopic.swear(async ({ matched, router }) => {
          assert.ok(await router.dispatch('foo bar buzz', {}), 'dispatch to "foo bar buzz" is successful');

          assert.equal(matched.foo[0], 'foo bar buzz', 'first match for "foo" is "foo bar buzz"');
          assert.equal(matched.foo[1], 'before foo bar', 'second match for "foo" is "before foo bar"');
          assert.equal(matched.foo[2], 'foo bar', 'third match for "foo" is "foo bar"');
          assert.equal(matched.foo[3], 'before foo', 'fourth match for "foo" is "before foo"');
          assert.equal(matched.foo[4], 'on foo', 'fifth match for "foo" is "on foo"');
        });
      });

      assert.skip("foo barbie", async (assert) => {
        await routerTopic.swear(async ({ matched, router }) => {
          assert.ok(await router.dispatch('foo barbie', {}));
          assert.equal(matched['f*'][0], 'f* barbie');
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
