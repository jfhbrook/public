/*
 * path-test.ts: Tests for the core `.path()` method.
 *
 * (C) 2022, Josh Holbrook.
 * (C) 2011, Charlie Robbins, Paolo Fragomeni, & the Contributors.
 * MIT LICENSE
 *
 */

import { test } from "tap";
import { discuss } from "@jfhbrook/swears";
import { Router } from '../router';

test('director/core/path', async (assert) => {
  assert.test("An instance of director.Router", async (assert) => {
    const routerTopic = discuss(async () => {
      const matched = {
        foo: [],
        newyork: []
      };

      const router = new Router<any>({
        '/foo': async () => { matched['foo'].push('foo'); }
      });

      return {
        matched,
        router
      }
    });

    const pathTopic = routerTopic.discuss(async ({ matched, router }) => {
      router.path('/regions', async () => {
        router.on('/:state', async (country: any) => {
          matched['newyork'].push('new york');
        });
      });

      return { matched, router };
    });

    assert.test("the path() method", async (assert) => {
      assert.test("should create the correct nested routing table", async (assert) => {
        await pathTopic.swear(async ({ matched, router }) => {
          assert.ok(router.routes.foo.on);
          assert.ok(router.routes.regions);
          assert.ok(router.routes.regions['([._a-zA-Z0-9-%()]+)'].on);
        });
      });

      assert.test("should dispatch the function correctly", async (assert) => {
        await pathTopic.swear(async ({ matched, router}) => {
          await router.dispatch('on', '/regions/newyork')
          await router.dispatch('on', '/foo');
          assert.equal(matched['foo'].length, 1);
          assert.equal(matched['newyork'].length, 1);
          assert.equal(matched['foo'][0], 'foo');
          assert.equal(matched['newyork'][0], 'new york');
        });
      });
    });
  });
});
