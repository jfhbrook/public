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
                '<root>': [],
                'foo': [],
                'f*': []
            };
            // TODO: these spaces are a wart, how do I fix them?
            const router = new router_1.Router({
                '': {
                    before: () => __awaiter(void 0, void 0, void 0, function* () { matched['<root>'].push('before /'); }),
                    on: () => __awaiter(void 0, void 0, void 0, function* () { matched['<root>'].push('on /'); }),
                    after: () => __awaiter(void 0, void 0, void 0, function* () { matched['<root>'].push('after /'); })
                },
                'foo': {
                    before: () => __awaiter(void 0, void 0, void 0, function* () { matched.foo.push('before foo'); }),
                    on: () => __awaiter(void 0, void 0, void 0, function* () { matched.foo.push('on foo'); }),
                    after: () => __awaiter(void 0, void 0, void 0, function* () { matched.foo.push('after foo'); }),
                    'bar': {
                        before: () => __awaiter(void 0, void 0, void 0, function* () { matched.foo.push('before foo bar'); }),
                        on: () => __awaiter(void 0, void 0, void 0, function* () { matched.foo.push('foo bar'); }),
                        after: () => __awaiter(void 0, void 0, void 0, function* () { matched.foo.push('after foo bar'); }),
                        'buzz': () => __awaiter(void 0, void 0, void 0, function* () { matched.foo.push('foo bar buzz'); })
                    }
                },
                'f*': {
                    'barbie': () => __awaiter(void 0, void 0, void 0, function* () { matched['f*'].push('f* barbie'); })
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
                assert.ok(router.routes.foo, 'should have a "foo" route');
                assert.ok(router.routes.foo.bar, 'should have a "foo bar" route');
                assert.ok(router.routes.foo.bar.buzz, 'should have a "foo bar buzz" route');
                assert.ok(router.routes.foo.bar.buzz.on, 'should have an "on" handler on the "foo bar buzz" route');
            }));
        }));
        assert.test("the dispatch() method", (assert) => __awaiter(void 0, void 0, void 0, function* () {
            assert.skip("<root>", (assert) => __awaiter(void 0, void 0, void 0, function* () {
                yield routerTopic.swear(({ matched, router }) => __awaiter(void 0, void 0, void 0, function* () {
                    assert.ok(yield router.dispatch('', {}));
                    assert.ok(yield router.dispatch('', {}));
                    assert.ok(matched['<root>'][0], 'before /');
                    assert.equal(matched['<root>'][1], 'on /');
                    assert.equal(matched['<root>'][2], 'after /');
                }));
            }));
            assert.test("foo bar buzz", (assert) => __awaiter(void 0, void 0, void 0, function* () {
                yield routerTopic.swear(({ matched, router }) => __awaiter(void 0, void 0, void 0, function* () {
                    assert.ok(yield router.dispatch('foo bar buzz', {}), 'dispatch to "foo bar buzz" is successful');
                    assert.equal(matched.foo[0], 'foo bar buzz', 'first match for "foo" is "foo bar buzz"');
                    assert.equal(matched.foo[1], 'before foo bar', 'second match for "foo" is "before foo bar"');
                    assert.equal(matched.foo[2], 'foo bar', 'third match for "foo" is "foo bar"');
                    assert.equal(matched.foo[3], 'before foo', 'fourth match for "foo" is "before foo"');
                    assert.equal(matched.foo[4], 'on foo', 'fifth match for "foo" is "on foo"');
                }));
            }));
            assert.skip("foo barbie", (assert) => __awaiter(void 0, void 0, void 0, function* () {
                yield routerTopic.swear(({ matched, router }) => __awaiter(void 0, void 0, void 0, function* () {
                    assert.ok(yield router.dispatch('foo barbie', {}));
                    assert.equal(matched['f*'][0], 'f* barbie');
                }));
            }));
            assert.skip("foo barbie ", (assert) => __awaiter(void 0, void 0, void 0, function* () {
                yield routerTopic.swear(({ router }) => __awaiter(void 0, void 0, void 0, function* () {
                    assert.notOk(yield router.dispatch('foo barbie ', {}));
                }));
            }));
            assert.skip("foo BAD", (assert) => __awaiter(void 0, void 0, void 0, function* () {
                yield routerTopic.swear(({ router }) => __awaiter(void 0, void 0, void 0, function* () {
                    assert.notOk(yield router.dispatch('foo BAD', {}));
                }));
            }));
            assert.skip("bar bar", (assert) => __awaiter(void 0, void 0, void 0, function* () {
                yield routerTopic.swear(({ router }) => __awaiter(void 0, void 0, void 0, function* () {
                    assert.notOk(yield router.dispatch('bar bar', {}));
                }));
            }));
            assert.skip("with the strict option disabled", (assert) => __awaiter(void 0, void 0, void 0, function* () {
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
                assert.test("foo barbie ", (assert) => __awaiter(void 0, void 0, void 0, function* () {
                    yield nonStrictTopic.swear(({ matched, router }) => __awaiter(void 0, void 0, void 0, function* () {
                        assert.ok(yield router.dispatch('on', 'foo barbie '));
                        assert.equal(matched['f*'][0], 'f* barbie');
                    }));
                }));
                assert.test("foo bar buzz", (assert) => __awaiter(void 0, void 0, void 0, function* () {
                    yield nonStrictTopic.swear(({ matched, router }) => __awaiter(void 0, void 0, void 0, function* () {
                        assert.ok(yield router.dispatch('on', 'foo bar buzz'));
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
