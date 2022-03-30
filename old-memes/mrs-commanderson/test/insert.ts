/*
 * insert-test.js: Tests for inserting routes into a normalized routing table.
 *
 * (C) 2011, Charlie Robbins, Paolo Fragomeni, & the Contributors.
 * MIT LICENSE
 *
 */

import { test } from 'tap';
import { discuss } from '@jfhbrook/swears';
import { Router } from '../';

test('director/core/insert', async (assert) => {
  assert.test("An instance of director.Router", async (assert) => {
    const topic = discuss(async () => {
      const router = new Router();
      return router
    });

    assert.test("the insert() method", async (assert) => {
      assert.test("'on', ['foo', 'bar']", async (assert) => {
        await topic.swear(async (router) => {
          function route () { }

          router.insert('on', ['foo', 'bar'], route);
          assert.equal(router.routes.foo.bar.on, route);
        });
      });

      assert.test("'on', ['foo', 'bar'] again", async (assert) => {
        await topic.swear(async (router) => {
          function route () { }

          router.insert('on', ['foo', 'bar'], route);

          assert.isArray(router.routes.foo.bar.on);
          assert.equal(router.routes.foo.bar.on.length, 2);
        });
      });

      assert.test("'on', ['foo', 'bar'] a third time", async (assert) => {
        await topic.swear(async (router) => {
          function route () { }

          router.insert('on', ['foo', 'bar'], route);
          assert.isArray(router.routes.foo.bar.on);
          assert.equal(router.routes.foo.bar.on.length, 3);
        });
      });

      assert.test("'get', ['fizz', 'buzz']", async (assert) => {
        await topic.swear(async (router) => {
          function route () { }

          router.insert('get', ['fizz', 'buzz'], route);
          assert.equal(router.routes.fizz.buzz.get, route);
        });
      });
    });
  });
});
