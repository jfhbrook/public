/*
 * dispatch-test.ts: Tests for the core dispatch method.
 *
 * (C) 2022, Josh Holbrook.
 * (C) 2011, Charlie Robbins, Paolo Fragomeni, & the Contributors.
 * MIT LICENSE
 *
 */

import { test } from 'tap';
import { Router } from '../router';

test('director/core/dispatch', async (assert) => {
  assert.test("An instance of director.Router", async (assert) => {
    const matched: any = {};
    matched['/'] = [];
    matched['foo'] = [];
    matched['f*'] = []

    const router = new Router({
      '/': {
        before: function () { matched['/'].push('before /') },
        on: function () { matched['/'].push('on /') },
        after: function () { matched['/'].push('after /') }
      },
      '/foo': {
        before: function () { matched.foo.push('before foo') },
        on: function () { matched.foo.push('on foo') },
        after: function () { matched.foo.push('after foo') },
        '/bar': {
          before: function () { matched.foo.push('before foo bar') },
          on: function () { matched.foo.push('foo bar') },
          after: function () { matched.foo.push('after foo bar') },
          '/buzz': function () { matched.foo.push('foo bar buzz') }
        }
      },
      '/f*': {
        '/barbie': function () { matched['f*'].push('f* barbie') }
      }
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

    router.configure({
      recurse: 'backward'
    });

    assert.test("should have the correct routing table", async (assert) => {
      assert.ok(router.routes.foo);
      assert.ok(router.routes.foo.bar);
      assert.ok(router.routes.foo.bar.buzz);
      assert.isFunction(router.routes.foo.bar.buzz.on);
    });

    assert.test("the dispatch() method", async (assert) => {
      assert.test("/", async (assert) => {
        assert.ok(await router.dispatch('on', '/'));
        assert.ok(await router.dispatch('on', '/'));

        assert.ok(matched['/'][0], 'before /');
        assert.equal(matched['/'][1], 'on /');
        assert.equal(matched['/'][2], 'after /');
      });

      assert.test("/foo/bar/buzz", async (assert) => {
        assert.ok(await router.dispatch('on', '/foo/bar/buzz'));

        assert.equal(matched.foo[0], 'foo bar buzz');
        assert.equal(matched.foo[1], 'before foo bar');
        assert.equal(matched.foo[2], 'foo bar');
        assert.equal(matched.foo[3], 'before foo');
        assert.equal(matched.foo[4], 'on foo');
      });

      assert.test("/foo/barbie", async (assert) => {
        assert.ok(await router.dispatch('on', '/foo/barbie'));
        assert.equal(matched['f*'][0], 'f* barbie');
      });

      assert.test("/foo/barbie/", async (assert) => {
        assert.notOk(await router.dispatch('on', '/foo/barbie/'));
      });

      assert.test("/foo/BAD", async (assert) => {
        assert.notOk(await router.dispatch('on', '/foo/BAD'));
      });

      assert.test("/bar/bar", function (assert) => {
        assert.notOk(await router.dispatch('on', '/bar/bar'));
      });
      
      assert.test("with the strict option disabled", async (assert) => {
        // TODO: These "topics are actually running as before hooks to
        // stand up a new fixture every time - this one builds on top of
        // the prior fixture.
        router.configure({
          recurse: 'backward',
          strict: false
        });

        assert.test("should have the proper configuration set", async (assert) => {
          assert.notOk(router.strict);
        });
        
        assert.test("/foo/barbie/", async (assert) => {
          assert.ok(await router.dispatch('on', '/foo/barbie/'));
          assert.equal(matched['f*'][0], 'f* barbie');
        });

        assert.test("/foo/bar/buzz", async (assert) => {
          assert.ok(await router.dispatch('on', '/foo/bar/buzz'));

          assert.equal(matched.foo[0], 'foo bar buzz');
          assert.equal(matched.foo[1], 'before foo bar');
          assert.equal(matched.foo[2], 'foo bar');
          assert.equal(matched.foo[3], 'before foo');
          assert.equal(matched.foo[4], 'on foo');
        });
      });
    });

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
  });
});
