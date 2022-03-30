"use strict";
/*
 * dispatch-test.ts: Tests for the core dispatch method.
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
(0, tap_1.test)('router/dispatch', (assert) => __awaiter(void 0, void 0, void 0, function* () {
    assert.test("An instance of Router", (assert) => __awaiter(void 0, void 0, void 0, function* () {
        const routerTopic = (0, swears_1.discuss)(() => __awaiter(void 0, void 0, void 0, function* () {
            const matched = {
                ' ': [],
                'foo': [],
                'f*': []
            };
            // TODO: these spaces are a wart, how do I fix them?
            const router = new router_1.Router({
                ' ': {
                    before: () => __awaiter(void 0, void 0, void 0, function* () { matched[' '].push('before /'); }),
                    on: () => __awaiter(void 0, void 0, void 0, function* () { matched[' '].push('on /'); }),
                    after: () => __awaiter(void 0, void 0, void 0, function* () { matched[' '].push('after /'); })
                },
                ' foo': {
                    before: () => __awaiter(void 0, void 0, void 0, function* () { matched.foo.push('before foo'); }),
                    on: () => __awaiter(void 0, void 0, void 0, function* () { matched.foo.push('on foo'); }),
                    after: () => __awaiter(void 0, void 0, void 0, function* () { matched.foo.push('after foo'); }),
                    ' bar': {
                        before: () => __awaiter(void 0, void 0, void 0, function* () { matched.foo.push('before foo bar'); }),
                        on: () => __awaiter(void 0, void 0, void 0, function* () { matched.foo.push('foo bar'); }),
                        after: () => __awaiter(void 0, void 0, void 0, function* () { matched.foo.push('after foo bar'); }),
                        ' buzz': () => __awaiter(void 0, void 0, void 0, function* () { matched.foo.push('foo bar buzz'); })
                    }
                },
                ' f*': {
                    ' barbie': () => __awaiter(void 0, void 0, void 0, function* () { matched['f*'].push('f* barbie'); })
                }
            });
            router.configure({
                recurse: 'backward'
            });
            return {
                matched,
                router
            };
        }));
        assert.test("should have the correct routing table", (assert) => __awaiter(void 0, void 0, void 0, function* () {
            yield routerTopic.swear(({ router }) => __awaiter(void 0, void 0, void 0, function* () {
                assert.ok(router.routes.foo);
                assert.ok(router.routes.foo.bar);
                assert.ok(router.routes.foo.bar.buzz);
                assert.ok(router.routes.foo.bar.buzz.on);
            }));
        }));
        assert.test("the dispatch() method", (assert) => __awaiter(void 0, void 0, void 0, function* () {
            assert.test("/", (assert) => __awaiter(void 0, void 0, void 0, function* () {
                yield routerTopic.swear(({ matched, router }) => __awaiter(void 0, void 0, void 0, function* () {
                    assert.ok(yield router.dispatch('on', '/'));
                    assert.ok(yield router.dispatch('on', '/'));
                    assert.ok(matched[' '][0], 'before /');
                    assert.equal(matched[' '][1], 'on /');
                    assert.equal(matched[' '][2], 'after /');
                }));
            }));
            assert.test(" foo bar buzz", (assert) => __awaiter(void 0, void 0, void 0, function* () {
                yield routerTopic.swear(({ matched, router }) => __awaiter(void 0, void 0, void 0, function* () {
                    assert.ok(yield router.dispatch('on', ' foo bar buzz'));
                    assert.equal(matched.foo[0], 'foo bar buzz');
                    assert.equal(matched.foo[1], 'before foo bar');
                    assert.equal(matched.foo[2], 'foo bar');
                    assert.equal(matched.foo[3], 'before foo');
                    assert.equal(matched.foo[4], 'on foo');
                }));
            }));
            assert.test(" foo barbie", (assert) => __awaiter(void 0, void 0, void 0, function* () {
                yield routerTopic.swear(({ matched, router }) => __awaiter(void 0, void 0, void 0, function* () {
                    assert.ok(yield router.dispatch('on', ' foo barbie'));
                    assert.equal(matched['f*'][0], 'f* barbie');
                }));
            }));
            assert.test(" foo barbie ", (assert) => __awaiter(void 0, void 0, void 0, function* () {
                yield routerTopic.swear(({ router }) => __awaiter(void 0, void 0, void 0, function* () {
                    assert.notOk(yield router.dispatch('on', ' foo barbie '));
                }));
            }));
            assert.test(" foo BAD", (assert) => __awaiter(void 0, void 0, void 0, function* () {
                yield routerTopic.swear(({ router }) => __awaiter(void 0, void 0, void 0, function* () {
                    assert.notOk(yield router.dispatch('on', ' foo BAD'));
                }));
            }));
            assert.test(" bar bar", (assert) => __awaiter(void 0, void 0, void 0, function* () {
                yield routerTopic.swear(({ router }) => __awaiter(void 0, void 0, void 0, function* () {
                    assert.notOk(yield router.dispatch('on', ' bar bar'));
                }));
            }));
            assert.test("with the strict option disabled", (assert) => __awaiter(void 0, void 0, void 0, function* () {
                const nonStrictTopic = routerTopic.discuss(({ matched, router }) => __awaiter(void 0, void 0, void 0, function* () {
                    router.configure({
                        recurse: 'backward',
                        strict: false
                    });
                    return { matched, router };
                }));
                assert.test("should have the proper configuration set", (assert) => __awaiter(void 0, void 0, void 0, function* () {
                    yield nonStrictTopic.swear(({ router }) => __awaiter(void 0, void 0, void 0, function* () {
                        assert.notOk(router.strict);
                    }));
                }));
                assert.test(" foo barbie ", (assert) => __awaiter(void 0, void 0, void 0, function* () {
                    yield nonStrictTopic.swear(({ matched, router }) => __awaiter(void 0, void 0, void 0, function* () {
                        assert.ok(yield router.dispatch('on', ' foo barbie '));
                        assert.equal(matched['f*'][0], 'f* barbie');
                    }));
                }));
                assert.test(" foo bar buzz", (assert) => __awaiter(void 0, void 0, void 0, function* () {
                    yield nonStrictTopic.swear(({ matched, router }) => __awaiter(void 0, void 0, void 0, function* () {
                        assert.ok(yield router.dispatch('on', ' foo bar buzz'));
                        assert.equal(matched.foo[0], 'foo bar buzz');
                        assert.equal(matched.foo[1], 'before foo bar');
                        assert.equal(matched.foo[2], 'foo bar');
                        assert.equal(matched.foo[3], 'before foo');
                        assert.equal(matched.foo[4], 'on foo');
                    }));
                }));
            }));
        }));
    }));
}));
