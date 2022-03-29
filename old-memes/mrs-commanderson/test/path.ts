/*
 * path-test.ts: Tests for the core `.path()` method.
 *
 * (C) 2022, Josh Holbrook.
 * (C) 2011, Charlie Robbins, Paolo Fragomeni, & the Contributors.
 * MIT LICENSE
 *
 */

import { test } from "tap";
import { Router } from '../router';

test('director/core/path', async (assert) => {
  assert.test("An instance of director.Router", async (assert) => {
    const matched: any = {};
    matched['foo'] = [];
    matched['newyork'] = [];

    const router = new Router<any>({
      '/foo': async () => { matched['foo'].push('foo'); }
    });

    assert.test("the path() method", async (assert) => {
      assert.test("should create the correct nested routing table", async (assert) => {
        router.path('/regions', function () {
          router.on('/:state', function(country: any) {
            matched['newyork'].push('new york');
          });
        });

        assert.isFunction(router.routes.foo.on);
        assert.ok(router.routes.regions);
        assert.isFunction(router.routes.regions['([._a-zA-Z0-9-%()]+)'].on);
      });

      assert.test("should dispatch the function correctly", async (assert) => {
        await router.dispatch('on', '/regions/newyork')
        await router.dispatch('on', '/foo');
        assert.same(matched['foo'].length, 1);
        assert.same(matched['newyork'].length, 1);
        assert.same(matched['foo'][0], 'foo');
        assert.same(matched['newyork'][0], 'new york');
      });

      assert.test("should create the correct nested routing table", async (assert) => {
        function noop () {}

        router.path(/apps/, function () {
          router.path(/foo/, function () {
            router.on(/bar/, noop);
          });

          router.on(/list/, noop);
        });

        router.on(/users/, noop);

        assert.ok(router.routes.apps);
        assert.isFunction(router.routes.apps.list.on);
        assert.isObject(router.routes.apps.foo);
        assert.isFunction(router.routes.apps.foo.bar.on);
        assert.isFunction(router.routes.users.on);
    });
  });
});
