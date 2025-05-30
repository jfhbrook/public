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

type Ctx = {};

type Matched = {
  foo: string[];
  newyork: string[];
};

test('router/path', async (assert) => {
  assert.test("(the cli version)", async (assert) => {
    const topic = discuss(async () => {
      const router = new Router<Ctx>();

      router.path(/apps/, function () {
        router.path(/foo/, function () {
          router.on(/bar/, async () => {});
        });

        router.on(/list/, async () => {});
      });

      router.on(/users/, async () => {});

      return router;
    });

    assert.test("should create the correct nested routing table", async (assert) => {
      await topic.swear(async (router) => {
        assert.ok(router.routes.apps);
        assert.type(router.routes.apps.list.on, Function);
        assert.ok(router.routes.apps.foo);
        assert.type(router.routes.apps.foo.bar.on, Function);
        assert.type(router.routes.users.on, Function);
      });
    });
  });

  assert.skip("(the core version)", async (assert) => {
    const routerTopic = discuss(async () => {
      const matched: Matched = {
        foo: [],
        newyork: []
      };

      const router = new Router<Ctx>({
        '/foo': async () => { matched['foo'].push('foo'); }
      });

      return {
        matched,
        router
      }
    });

    const pathTopic = routerTopic.discuss(async ({ matched, router }) => {
      router.path('regions', function() {
        // Testing that "this" is Router
        this.on('on', ':state', async (ctx: Ctx, country: string) => {
          matched['newyork'].push('new york');
        });
      });

      return { matched, router };
    });

    assert.skip("the path() method", async (assert) => {
      assert.test("should create the correct nested routing table", async (assert) => {
        await pathTopic.swear(async ({ router }) => {
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
