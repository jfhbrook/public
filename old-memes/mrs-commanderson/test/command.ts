/*
 * on-test.js: Tests for the on/route method.
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
      return new Router();
    });

    assert.test("the on() method", async (assert) => {
      assert.test("['foo', 'bar']", async (assert) => {
        await topic.swear(async (router) => {
          function noop () { }

          router.on(['foo', 'bar'], noop);
          assert.equal(router.routes.foo.on, noop);
          assert.equal(router.routes.bar.on, noop);
        });
      });

      assert.test("'baz'", async (assert) => {
        await topic.swear(async (router) => {
          function noop () { }

          router.on('baz', noop);
          assert.equal(router.routes.baz.on, noop);
        });
      });

      assert.test("'after', 'baz'", async (assert) => {
        await topic.swear(async (router) => {
          function noop () { }

          router.on('after', 'boo', noop);
          assert.equal(router.routes.boo.after, noop);
        });
      });
    });
  });
});
