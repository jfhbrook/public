"use strict";
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
// jfc typescript
function assertRoutes(assert, assertions) {
    function assertRoute(fn, path, route) {
        if (path.length === 1) {
            assert.equal(route[path.shift()], fn);
            return;
        }
        route = route[path.shift()];
        assert.ok(route);
        assertRoute(fn, path, route);
    }
    ;
    for (let assertion of assertions) {
        assertRoute.apply(null, assertion);
    }
}
function foobar() {
    return __awaiter(this, void 0, void 0, function* () { });
}
function foostar() {
    return __awaiter(this, void 0, void 0, function* () { });
}
function foobazzbuzz() {
    return __awaiter(this, void 0, void 0, function* () { });
}
function foodog() {
    return __awaiter(this, void 0, void 0, function* () { });
}
function root() {
    return __awaiter(this, void 0, void 0, function* () { });
}
const fnArray = [foobar, foostar];
function dogs() {
    return __awaiter(this, void 0, void 0, function* () { });
}
;
function usaCityZip() {
    return __awaiter(this, void 0, void 0, function* () { });
}
function countryCityZip() {
    return __awaiter(this, void 0, void 0, function* () { });
}
(0, tap_1.test)('router/mount', (assert) => __awaiter(void 0, void 0, void 0, function* () {
    assert.test('(the cli version)', (assert) => __awaiter(void 0, void 0, void 0, function* () {
        const topic = (0, swears_1.discuss)(() => __awaiter(void 0, void 0, void 0, function* () {
            return new router_1.Router({
                apps: () => __awaiter(void 0, void 0, void 0, function* () { }),
                ' users': () => __awaiter(void 0, void 0, void 0, function* () { })
            });
        }));
        assert.test('should create the correct routing table', (assert) => __awaiter(void 0, void 0, void 0, function* () {
            yield topic.swear((router) => __awaiter(void 0, void 0, void 0, function* () {
                assert.ok(router.routes.apps);
                assert.ok(router.routes.users);
                assert.type(router.routes.apps.on, Function);
                assert.type(router.routes.users.on, Function);
            }));
        }));
    }));
    assert.skip("(the core version)", (assert) => __awaiter(void 0, void 0, void 0, function* () {
        assert.test("with no preconfigured params", (assert) => __awaiter(void 0, void 0, void 0, function* () {
            const topic = (0, swears_1.discuss)(() => __awaiter(void 0, void 0, void 0, function* () {
                return new router_1.Router();
            }));
            assert.test("the mount() method", (assert) => __awaiter(void 0, void 0, void 0, function* () {
                assert.skip("should sanitize the routes correctly", (assert) => __awaiter(void 0, void 0, void 0, function* () {
                    yield topic.swear((router) => __awaiter(void 0, void 0, void 0, function* () {
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
                            [root, ['on'], router.routes],
                            [root, ['after'], router.routes],
                            [root, ['before'], router.routes],
                            [foobar, ['nesting', 'on'], router.routes],
                            [foostar, ['nesting', 'deep', 'on'], router.routes],
                            [foobar, ['foo', 'bar', 'on'], router.routes],
                            [foostar, ['foo', '([_.()!\\ %@&a-zA-Z0-9-]+)', 'on'], router.routes],
                            [fnArray, ['foo', 'jitsu', 'then', 'on'], router.routes],
                            [foobar, ['foo', 'jitsu', 'then', 'before'], router.routes],
                            [foobazzbuzz, ['foo', 'bazz', 'buzz', 'on'], router.routes],
                            [foostar, ['foo', 'jitsu', 'then', 'now', 'on'], router.routes],
                            [foodog, ['foo', '([._a-zA-Z0-9-%()]+)', 'on'], router.routes]
                        ]);
                    }));
                }));
                assert.skip("should accept string path", (assert) => __awaiter(void 0, void 0, void 0, function* () {
                    yield topic.swear((router) => __awaiter(void 0, void 0, void 0, function* () {
                        router.mount({
                            ' dogs': {
                                on: dogs
                            }
                        }, ' api');
                        assertRoutes(assert, [
                            [dogs, ['api', 'dogs', 'on'], router.routes]
                        ]);
                    }));
                }));
            }));
        }));
        assert.test("with preconfigured params", (assert) => __awaiter(void 0, void 0, void 0, function* () {
            const topic = (0, swears_1.discuss)(() => __awaiter(void 0, void 0, void 0, function* () {
                const router = new router_1.Router();
                router.param('city', '([\\w\\-]+)');
                router.param(':country', /([A-Z][A-Za-z]+)/);
                router.param(':zip', /([\d]{5})/);
                return router;
            }));
            assert.skip("should sanitize the routes correctly", (assert) => __awaiter(void 0, void 0, void 0, function* () {
                yield topic.swear((router) => __awaiter(void 0, void 0, void 0, function* () {
                    router.mount({
                        ' usa :city :zip': usaCityZip,
                        ' world': {
                            ' :country': {
                                ' :city :zip': countryCityZip
                            }
                        }
                    });
                    assertRoutes(assert, [
                        [usaCityZip, ['usa', '([\\w\\-]+)', '([\\d]{5})', 'on'], router.routes],
                        [countryCityZip, ['world', '([A-Z][A-Za-z]+)', '([\\w\\-]+)', '([\\d]{5})', 'on'], router.routes]
                    ]);
                }));
            }));
        }));
    }));
}));
