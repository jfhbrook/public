/*
 * mount-test.js: Tests for mounting and normalizing routes into a Router instance.
 *
 * (C) 2011, Charlie Robbins, Paolo Fragomeni, & the Contributors.
 * MIT LICENSE
 *
 */

var assert = require('assert'),
    vows = require('vows'),
    director = require('../../../lib/director');

function assertRoute (fn, path, route) {
  if (path.length === 1) {
    return assert.strictEqual(route[path.shift()], fn);
  }

  route = route[path.shift()];
  assert.isObject(route);
  assertRoute(fn, path, route);
}

vows.describe('director/core/mount').addBatch({
  "An instance of director.Router": {
    "with no preconfigured params": {
      topic: new director.Router(),
      "the mount() method": {
        "should sanitize the routes correctly": function (router) {
          function foobar () { }
          function foostar () { }
          function foobazzbuzz () { }
          function foodog () { }
          function root () {}
          var fnArray = [foobar, foostar];

          router.mount({
            '/': {
              before: root,
              on: root,
              after: root,
              '/nesting': {
                on: foobar,
                '/deep': foostar
              }
            },
            '/foo': {
              '/bar': foobar,
              '/*': foostar,
              '/jitsu/then': {
                before: foobar
              }
            },
            '/foo/bazz': {
              '/buzz': foobazzbuzz
            },
            '/foo/jitsu': {
              '/then': fnArray
            },
            '/foo/jitsu/then/now': foostar,
            '/foo/:dog': foodog
          });

          assertRoute(root,        ['on'],                                      router.routes);
          assertRoute(root,        ['after'],                                   router.routes);
          assertRoute(root,        ['before'],                                  router.routes);
          assertRoute(foobar,      ['nesting', 'on'],                           router.routes);
          assertRoute(foostar,     ['nesting', 'deep', 'on'],                   router.routes);
          assertRoute(foobar,      [ 'foo', 'bar', 'on'],                       router.routes);
          assertRoute(foostar,     ['foo', '([_.()!\\ %@&a-zA-Z0-9-]+)', 'on'], router.routes);
          assertRoute(fnArray,     ['foo', 'jitsu', 'then', 'on'],              router.routes);
          assertRoute(foobar,      ['foo', 'jitsu', 'then', 'before'],          router.routes);
          assertRoute(foobazzbuzz, ['foo', 'bazz', 'buzz', 'on'],               router.routes);
          assertRoute(foostar,     ['foo', 'jitsu', 'then', 'now', 'on'],       router.routes);
          assertRoute(foodog,      ['foo', '([._a-zA-Z0-9-%()]+)', 'on'],     router.routes);
        },

        "should accept string path": function(router) {
          function dogs () { }

          router.mount({
            '/dogs': {
              on: dogs
            }
          },
          '/api');

          assertRoute(dogs, ['api', 'dogs', 'on'], router.routes);
        }
      }
    },
    "with preconfigured params": {
      topic: function () {
        var router = new director.Router();
        router.param('city', '([\\w\\-]+)');
        router.param(':country', /([A-Z][A-Za-z]+)/);
        router.param(':zip', /([\d]{5})/);
        return router;
      },
      "should sanitize the routes correctly": function (router) {
        function usaCityZip () { }
        function countryCityZip () { }

        router.mount({
          '/usa/:city/:zip': usaCityZip,
          '/world': {
            '/:country': {
              '/:city/:zip': countryCityZip
            }
          }
        });

        assertRoute(usaCityZip, ['usa', '([\\w\\-]+)', '([\\d]{5})', 'on'], router.routes);
        assertRoute(countryCityZip, ['world', '([A-Z][A-Za-z]+)', '([\\w\\-]+)', '([\\d]{5})', 'on'], router.routes);
      }
    }
  }
}).export(module);
/*
 * mount-test.js: Tests for the core mount method.
 *
 * (C) 2011, Charlie Robbins, Paolo Fragomeni, & the Contributors.
 * MIT LICENSE
 *
 */

var assert = require('assert'),
    vows = require('vows'),
    director = require('../../../lib/director');

vows.describe('director/cli/path').addBatch({
  "An instance of director.cli.Router with routes": {
    topic: new director.cli.Router({
      'apps': function () {
        console.log('apps');
      },
      ' users': function () {
        console.log('users');
      }
    }),
    "should create the correct nested routing table": function (router) {
      assert.isObject(router.routes.apps);
      assert.isFunction(router.routes.apps.on);
      assert.isObject(router.routes.users);
      assert.isFunction(router.routes.users.on);
    }
  }
}).export(module);
