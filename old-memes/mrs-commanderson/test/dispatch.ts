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

test('director/core/dispatch', async (assert) => {
  assert.test("An instance of director.Router", async (assert) => {
    const routerTopic = discuss(async () => {
      const matched = {
        '/': [],
        'foo': [],
        'f*': []
      }

      const router = new Router<typeof this>({
        '/': {
          before: async () => { matched['/'].push('before /') },
          on: async () => { matched['/'].push('on /') },
          after: async () => { matched['/'].push('after /') }
        },
        '/foo': {
          before: async () => { matched.foo.push('before foo') },
          on: async () => { matched.foo.push('on foo') },
          after: async () => { matched.foo.push('after foo') },
          '/bar': {
            before: async () => { matched.foo.push('before foo bar') },
            on: async () => { matched.foo.push('foo bar') },
            after: async () => { matched.foo.push('after foo bar') },
            '/buzz': async () { matched.foo.push('foo bar buzz') }
          }
        },
        '/f*': {
          '/barbie': async () => { matched['f*'].push('f* barbie') }
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


    /*
      matched = {};
      matched['users'] = [];
      matched['apps'] = []

      router.on('users create', function () {
        that.matched['users'].push('on users create');
      });

      router.on(/apps (\w+\s\w+)/, function () {
        assert.equal(arguments.length, 1);
        that.matched['apps'].push('on apps (\\w+\\s\\w+)');
      });
     */

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

          assert.ok(matched['/'][0], 'before /');
          assert.equal(matched['/'][1], 'on /');
          assert.equal(matched['/'][2], 'after /');
        });
      });

      assert.test("/foo/bar/buzz", async (assert) => {
        await routerTopic.swear(async ({ matched, router }) => {
          assert.ok(await router.dispatch('on', '/foo/bar/buzz'));

          assert.equal(matched.foo[0], 'foo bar buzz');
          assert.equal(matched.foo[1], 'before foo bar');
          assert.equal(matched.foo[2], 'foo bar');
          assert.equal(matched.foo[3], 'before foo');
          assert.equal(matched.foo[4], 'on foo');
        });
      });

      assert.test("/foo/barbie", async (assert) => {
        await routerTopic.swear(async ({ matched, router }) => {
          assert.ok(await router.dispatch('on', '/foo/barbie'));
          assert.equal(matched['f*'][0], 'f* barbie');
        });
      });

      assert.test("/foo/barbie/", async (assert) => {
        await routerTopic.swear(async ({ router }) => {
          assert.notOk(await router.dispatch('on', '/foo/barbie/'));
        });
      });

      assert.test("/foo/BAD", async (assert) => {
        await routerTopic.swear(async ({ router }) => {
          assert.notOk(await router.dispatch('on', '/foo/BAD'));
        });
      });

      assert.test("/bar/bar", async (assert) => {
        await routerTopic.swear(async ({ router }) => {
          assert.notOk(await router.dispatch('on', '/bar/bar'));
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
        
        assert.test("/foo/barbie/", async (assert) => {
          await nonStrictTopic.swear(async ({ matched, router }) => {
            assert.ok(await router.dispatch('on', '/foo/barbie/'));
            assert.equal(matched['f*'][0], 'f* barbie');
          });
        });

        assert.test("/foo/bar/buzz", async (assert) => {
          await nonStrictTopic.swear(async ({ matched, router }) => {
            assert.ok(await router.dispatch('on', '/foo/bar/buzz'));

            assert.equal(matched.foo[0], 'foo bar buzz');
            assert.equal(matched.foo[1], 'before foo bar');
            assert.equal(matched.foo[2], 'foo bar');
            assert.equal(matched.foo[3], 'before foo');
            assert.equal(matched.foo[4], 'on foo');
          });
        });
      });
    });

    /*
    assert.skip("should have the correct routing table (old cli tests)", async (assert) => {
      assert.ok(router.routes.users);
      assert.ok(router.routes.users.create);
    });

    assert.skip("the dispatch() method (old cli tests)", async (assert) => {
      assert.test("users create", async (assert) => {
        assert.ok(await router.dispatch('on', 'users create'));
        assert.equal(matched.users[0], 'on users create');
      });

      assert.test("apps foo bar", async (assert) => {
        assert.ok(await router.dispatch('on', 'apps foo bar'));
        assert.equal(matched['apps'][0], 'on apps (\\w+\\s\\w+)');
      });

      assert.test("not here", async (assert) => {
        assert.notOk(await router.dispatch('on', 'not here'));
      });

      assert.test("still not here", async (assert) => {
        assert.notOk(await router.dispatch('on', 'still not here'));
      });
    });
    */
  });
});
