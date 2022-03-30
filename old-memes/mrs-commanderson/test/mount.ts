/*
 * mount-test.js: Tests for mounting and normalizing routes into a Router instance.
 *
 * (C) 2011, Charlie Robbins, Paolo Fragomeni, & the Contributors.
 * MIT LICENSE
 *
 */
import * as tap from 'tap';
import { test } from 'tap';
import { discuss } from '@jfhbrook/swears';
import { Router, Handler, RoutingObject } from '../router';

type Test = (typeof tap.Test)["prototype"]

type Ctx = {};

type RouteAssertion = [Handler<Ctx>, string[], RoutingObject<Ctx>];

// jfc typescript
function assertRoutes(assert: Test, assertions: RouteAssertion[]): void {
  function assertRoute(fn: Handler<Ctx>, path: string[], route: RoutingObject<Ctx>): void {
    if (path.length === 1) {
      assert.equal((route as any)[<string>path.shift()], fn);
      return;
    }

    route = (route as any)[<string>path.shift()];
    assert.ok(route);
    assertRoute(fn, path, route);
  };

  for (let assertion of assertions) {
    assertRoute.apply(null, assertion);
  }

}


async function foobar () { }
async function foostar () { }
async function foobazzbuzz () { }
async function foodog () { }
async function root () {}
const fnArray = [foobar, foostar];
async function dogs () { };
async function usaCityZip () { }
async function countryCityZip () { }


test('router/mount', async (assert) => {
  assert.test("An instance of Router", async (assert) => {
    assert.test("with no preconfigured params", async (assert) => {
      const topic = discuss(async () => {
        return new Router<Ctx>();
      });

      assert.test("the mount() method", async (assert) => {
        assert.skip("should sanitize the routes correctly", async (assert) => {
          await topic.swear(async (router) => {

            router.mount({
              ' ': {
                before: root,
                on: root,
                after: root,
                ' nesting': {
                  on: foobar,
                  ' deep': foostar
                }
              },
              ' foo': {
                ' bar': foobar,
                ' *': foostar,
                ' jitsu then': {
                  before: foobar
                }
              },
              ' foo bazz': {
                ' buzz': foobazzbuzz
              },
              ' foo jitsu': {
                ' then': fnArray
              },
              ' foo jitsu then now': foostar,
              ' foo :dog': foodog
            });

            assertRoutes(assert, [
              [root,        ['on'],                                      router.routes],
              [root,        ['after'],                                   router.routes],
              [root,        ['before'],                                  router.routes],
              [foobar,      ['nesting', 'on'],                           router.routes],
              [foostar,     ['nesting', 'deep', 'on'],                   router.routes],
              [foobar,      [ 'foo', 'bar', 'on'],                       router.routes],
              [foostar,     ['foo', '([_.()!\\ %@&a-zA-Z0-9-]+)', 'on'], router.routes],
              [fnArray,     ['foo', 'jitsu', 'then', 'on'],              router.routes],
              [foobar,      ['foo', 'jitsu', 'then', 'before'],          router.routes],
              [foobazzbuzz, ['foo', 'bazz', 'buzz', 'on'],               router.routes],
              [foostar,     ['foo', 'jitsu', 'then', 'now', 'on'],       router.routes],
              [foodog,      ['foo', '([._a-zA-Z0-9-%()]+)', 'on'],     router.routes]
            ]);
          });
        });

        assert.skip("should accept string path", async (assert) => {
          await topic.swear(async (router) => {

            router.mount({
              ' dogs': {
                on: dogs
              }
            },
            ' api');

            assertRoutes(assert, [
              [ dogs, ['api', 'dogs', 'on'], router.routes ]
            ]);
          });
        });
      });
    });

    assert.test("with preconfigured params", async (assert) => {
      const topic = discuss(async () => {
        const router = new Router<Ctx>();
        router.param('city', '([\\w\\-]+)');
        router.param(':country', /([A-Z][A-Za-z]+)/);
        router.param(':zip', /([\d]{5})/);
        return router;
      });

      assert.skip("should sanitize the routes correctly", async (assert) => {
        await topic.swear(async (router) => {

          router.mount({
            ' usa :city :zip': usaCityZip,
            ' world': {
              ' :country': {
                ' :city :zip': countryCityZip
              }
            }
          });

          assertRoutes(assert, [
            [ usaCityZip, ['usa', '([\\w\\-]+)', '([\\d]{5})', 'on'], router.routes ],
            [ countryCityZip, ['world', '([A-Z][A-Za-z]+)', '([\\w\\-]+)', '([\\d]{5})', 'on'], router.routes ]
          ]);
        });
      });
    });
  });
});

