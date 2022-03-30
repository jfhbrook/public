/*
 * insert-test.js: Tests for inserting routes into a normalized routing table.
 *
 * (C) 2011, Charlie Robbins, Paolo Fragomeni, & the Contributors.
 * MIT LICENSE
 *
 */

import { test } from 'tap';
import { discuss } from '@jfhbrook/swears';
import { Router } from '../router';

type Ctx = {};

async function route() {}

test('router/insert', async (assert) => {
  assert.test("An instance of director.Router", async (assert) => {
    const topic = discuss(async () => {
      const router = new Router<Ctx>();
      return router
    });

    assert.test("the insert() method", async (assert) => {
      assert.test("'on', ['foo', 'bar']", async (assert) => {
        await topic.swear(async (router) => {
          router.insert('on', ['foo', 'bar'], route);
          assert.equal(router.routes.foo.bar.on, route);
        });
      });

      assert.test("'on', ['foo', 'bar'] again", async (assert) => {
        await topic.swear(async (router) => {
          router.insert('on', ['foo', 'bar'], route);
          assert.type(router.routes.foo.bar.on, Array);
          assert.equal(router.routes.foo.bar.on.length, 2);
        });
      });

      assert.test("'on', ['foo', 'bar'] a third time", async (assert) => {
        await topic.swear(async (router) => {
          router.insert('on', ['foo', 'bar'], route);
          assert.type(router.routes.foo.bar.on, Array);
          assert.equal(router.routes.foo.bar.on.length, 3);
        });
      });

      assert.test("'get', ['fizz', 'buzz']", async (assert) => {
        await topic.swear(async (router) => {
          router.insert('get', ['fizz', 'buzz'], route);
          assert.equal(router.routes.fizz.buzz.get, route);
        });
      });
    });
  });
});
