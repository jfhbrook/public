"use strict";
/*
 * path-test.ts: Tests for the core `.path()` method.
 *
 * (C) 2022, Josh Holbrook.
 * (C) 2011, Charlie Robbins, Paolo Fragomeni, & the Contributors.
 * MIT LICENSE
 *
 */
var __awaiter = (this && this.__awaiter) || function (thisArg, _arguments, P, generator) {
    function adopt(value) { return value instanceof P ? value : new P(function (resolve) { resolve(value); }); }
    return new (P || (P = Promise))(function (resolve, reject) {
        function fulfilled(value) { try { step(generator.next(value)); } catch (e) { reject(e); } }
        function rejected(value) { try { step(generator["throw"](value)); } catch (e) { reject(e); } }
        function step(result) { result.done ? resolve(result.value) : adopt(result.value).then(fulfilled, rejected); }
        step((generator = generator.apply(thisArg, _arguments || [])).next());
    });
};
Object.defineProperty(exports, "__esModule", { value: true });
const tap_1 = require("tap");
const swears_1 = require("@jfhbrook/swears");
const router_1 = require("../router");
(0, tap_1.test)('router/path', (assert) => __awaiter(void 0, void 0, void 0, function* () {
    assert.test("(the cli version)", (assert) => __awaiter(void 0, void 0, void 0, function* () {
        const topic = (0, swears_1.discuss)(() => __awaiter(void 0, void 0, void 0, function* () {
            const router = new router_1.Router();
            router.path(/apps/, function () {
                router.path(/foo/, function () {
                    router.on(/bar/, () => __awaiter(this, void 0, void 0, function* () { }));
                });
                router.on(/list/, () => __awaiter(this, void 0, void 0, function* () { }));
            });
            router.on(/users/, () => __awaiter(void 0, void 0, void 0, function* () { }));
            return router;
        }));
        assert.test("should create the correct nested routing table", (assert) => __awaiter(void 0, void 0, void 0, function* () {
            yield topic.swear((router) => __awaiter(void 0, void 0, void 0, function* () {
                assert.ok(router.routes.apps);
                assert.type(router.routes.apps.list.on, Function);
                assert.ok(router.routes.apps.foo);
                assert.type(router.routes.apps.foo.bar.on, Function);
                assert.type(router.routes.users.on, Function);
            }));
        }));
    }));
    assert.skip("(the core version)", (assert) => __awaiter(void 0, void 0, void 0, function* () {
        const routerTopic = (0, swears_1.discuss)(() => __awaiter(void 0, void 0, void 0, function* () {
            const matched = {
                foo: [],
                newyork: []
            };
            const router = new router_1.Router({
                '/foo': () => __awaiter(void 0, void 0, void 0, function* () { matched['foo'].push('foo'); })
            });
            return {
                matched,
                router
            };
        }));
        const pathTopic = routerTopic.discuss(({ matched, router }) => __awaiter(void 0, void 0, void 0, function* () {
            router.path('regions', function () {
                // Testing that "this" is Router
                this.on('on', ':state', (ctx, country) => __awaiter(this, void 0, void 0, function* () {
                    matched['newyork'].push('new york');
                }));
            });
            return { matched, router };
        }));
        assert.skip("the path() method", (assert) => __awaiter(void 0, void 0, void 0, function* () {
            assert.test("should create the correct nested routing table", (assert) => __awaiter(void 0, void 0, void 0, function* () {
                yield pathTopic.swear(({ router }) => __awaiter(void 0, void 0, void 0, function* () {
                    assert.ok(router.routes.foo.on);
                    assert.ok(router.routes.regions);
                    assert.ok(router.routes.regions['([._a-zA-Z0-9-%()]+)'].on);
                }));
            }));
            assert.test("should dispatch the function correctly", (assert) => __awaiter(void 0, void 0, void 0, function* () {
                yield pathTopic.swear(({ matched, router }) => __awaiter(void 0, void 0, void 0, function* () {
                    yield router.dispatch('on', '/regions/newyork');
                    yield router.dispatch('on', '/foo');
                    assert.equal(matched['foo'].length, 1);
                    assert.equal(matched['newyork'].length, 1);
                    assert.equal(matched['foo'][0], 'foo');
                    assert.equal(matched['newyork'][0], 'new york');
                }));
            }));
        }));
    }));
}));
