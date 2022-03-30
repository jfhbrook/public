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
  ' ': string[];
  'foo': string[];
  'f*': string[];
};

test('router/dispatch', async (assert) => {
  assert.test("An instance of Router", async (assert) => {
    const routerTopic = discuss(async () => {
      const matched: Matched = {
        ' ': [],
        'foo': [],
        'f*': []
      }

      // TODO: these spaces are a wart, how do I fix them?
      const router = new Router<Ctx>({
        ' ': {
          before: async () => { matched[' '].push('before /') },
          on: async () => { matched[' '].push('on /') },
          after: async () => { matched[' '].push('after /') }
        },
        ' foo': {
          before: async () => { matched.foo.push('before foo') },
          on: async () => { matched.foo.push('on foo') },
          after: async () => { matched.foo.push('after foo') },
          ' bar': {
            before: async () => { matched.foo.push('before foo bar') },
            on: async () => { matched.foo.push('foo bar') },
            after: async () => { matched.foo.push('after foo bar') },
            ' buzz': async () => { matched.foo.push('foo bar buzz') }
          }
        },
        ' f*': {
          ' barbie': async () => { matched['f*'].push('f* barbie') }
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
        assert.ok(router.routes.foo);
        assert.ok(router.routes.foo.bar);
        assert.ok(router.routes.foo.bar.buzz);
        assert.ok(router.routes.foo.bar.buzz.on);
      });
    });

    assert.test("the dispatch() method", async (assert) => {
      assert.test("/", async (assert) => {
        await routerTopic.swear(async ({ matched, router }) => {
          assert.ok(await router.dispatch('on', '/'));
          assert.ok(await router.dispatch('on', '/'));

          assert.ok(matched[' '][0], 'before /');
          assert.equal(matched[' '][1], 'on /');
          assert.equal(matched[' '][2], 'after /');
        });
      });

      assert.test(" foo bar buzz", async (assert) => {
        await routerTopic.swear(async ({ matched, router }) => {
          assert.ok(await router.dispatch('on', ' foo bar buzz'));

          assert.equal(matched.foo[0], 'foo bar buzz');
          assert.equal(matched.foo[1], 'before foo bar');
          assert.equal(matched.foo[2], 'foo bar');
          assert.equal(matched.foo[3], 'before foo');
          assert.equal(matched.foo[4], 'on foo');
        });
      });

      assert.test(" foo barbie", async (assert) => {
        await routerTopic.swear(async ({ matched, router }) => {
          assert.ok(await router.dispatch('on', ' foo barbie'));
          assert.equal(matched['f*'][0], 'f* barbie');
        });
      });

      assert.test(" foo barbie ", async (assert) => {
        await routerTopic.swear(async ({ router }) => {
          assert.notOk(await router.dispatch('on', ' foo barbie '));
        });
      });

      assert.test(" foo BAD", async (assert) => {
        await routerTopic.swear(async ({ router }) => {
          assert.notOk(await router.dispatch('on', ' foo BAD'));
        });
      });

      assert.test(" bar bar", async (assert) => {
        await routerTopic.swear(async ({ router }) => {
          assert.notOk(await router.dispatch('on', ' bar bar'));
        });
      });
      
      assert.test("with the strict option disabled", async (assert) => {
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
        
        assert.test(" foo barbie ", async (assert) => {
          await nonStrictTopic.swear(async ({ matched, router }) => {
            assert.ok(await router.dispatch('on', ' foo barbie '));
            assert.equal(matched['f*'][0], 'f* barbie');
          });
        });

        assert.test(" foo bar buzz", async (assert) => {
          await nonStrictTopic.swear(async ({ matched, router }) => {
            assert.ok(await router.dispatch('on', ' foo bar buzz'));

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
