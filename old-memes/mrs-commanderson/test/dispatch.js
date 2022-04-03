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
    assert.test('(the cli version)', (assert) => __awaiter(void 0, void 0, void 0, function* () {
        const topic = (0, swears_1.discuss)(() => __awaiter(void 0, void 0, void 0, function* () {
            const router = new router_1.Router();
            const matched = {
                users: [],
                apps: []
            };
            router.on('users create', () => __awaiter(void 0, void 0, void 0, function* () {
                matched.users.push('on users create');
            }));
            router.on(/apps (\w+\s\w+)/, () => __awaiter(void 0, void 0, void 0, function* () {
                matched.apps.push('on apps (\\w+\\s\\w+)');
            }));
            return {
                matched,
                router
            };
        }));
        assert.test('should have the correct routing table', (assert) => __awaiter(void 0, void 0, void 0, function* () {
            yield topic.swear(({ router }) => __awaiter(void 0, void 0, void 0, function* () {
                assert.ok(router.routes.users.create);
            }));
        }));
        assert.test('the dispatch() method', (assert) => __awaiter(void 0, void 0, void 0, function* () {
            assert.test('users create', (assert) => __awaiter(void 0, void 0, void 0, function* () {
                yield topic.swear(({ router }) => __awaiter(void 0, void 0, void 0, function* () {
                    assert.ok(yield router.dispatch('on', 'users create', {}));
                }));
            }));
            assert.test('apps foo bar', (assert) => __awaiter(void 0, void 0, void 0, function* () {
                yield topic.swear(({ matched, router }) => __awaiter(void 0, void 0, void 0, function* () {
                    assert.ok(yield router.dispatch('on', 'apps foo bar', {}));
                    assert.same(matched.apps, ['on apps (\\w+\\s\\w+)']);
                }));
            }));
            assert.test('not here', (assert) => __awaiter(void 0, void 0, void 0, function* () {
                yield topic.swear(({ router }) => __awaiter(void 0, void 0, void 0, function* () {
                    assert.notOk(yield router.dispatch('on', 'not here', {}));
                }));
            }));
            assert.test('still not here', (assert) => __awaiter(void 0, void 0, void 0, function* () {
                yield topic.swear(({ router }) => __awaiter(void 0, void 0, void 0, function* () {
                    assert.notOk(yield router.dispatch('on', 'still not here', {}));
                }));
            }));
        }));
    }));
    assert.skip('(the core version)', (assert) => __awaiter(void 0, void 0, void 0, function* () {
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
            assert.skip("should have the correct routing table", (assert) => __awaiter(void 0, void 0, void 0, function* () {
                yield routerTopic.swear(({ router }) => __awaiter(void 0, void 0, void 0, function* () {
                    // TODO: the actual data structure in routes is weird, it's like
                    // super flattened, it's not what's supposed to be here. Something is
                    // quite wrong - I think I want to copy-paste the original definitions
                    // back in and look over changes to make sure I'm not being disappointed
                    // anywhere ;)
                    assert.ok(router.routes.foo, 'should have a "foo" route');
                    assert.ok(router.routes.foo.bar, 'should have a "foo bar" route');
                    assert.ok(router.routes.foo.bar.buzz, 'should have a "foo bar buzz" route');
                    assert.ok(router.routes.foo.bar.buzz.on, 'should have an "on" handler on the "foo bar buzz" route');
                }));
            }));
            assert.skip("the dispatch() method", (assert) => __awaiter(void 0, void 0, void 0, function* () {
                assert.skip("<root>", (assert) => __awaiter(void 0, void 0, void 0, function* () {
                    yield routerTopic.swear(({ matched, router }) => __awaiter(void 0, void 0, void 0, function* () {
                        assert.ok(yield router.dispatch('', {}));
                        assert.ok(yield router.dispatch('', {}));
                        assert.same(matched, {
                            '<root>': ['before /', 'on /', 'after /'],
                            'foo': [],
                            'f*': []
                        });
                    }));
                }));
                assert.test("foo bar buzz", (assert) => __awaiter(void 0, void 0, void 0, function* () {
                    yield routerTopic.swear(({ matched, router }) => __awaiter(void 0, void 0, void 0, function* () {
                        assert.ok(yield router.dispatch('foo bar buzz', {}), 'dispatch to "foo bar buzz" is successful');
                        assert.same(matched, {
                            '<root>': [],
                            'foo': ['foo bar buz', 'before foo bar', 'foo bar', 'before foo', 'on foo'],
                            'f*': []
                        });
                    }));
                }));
                assert.skip("foo barbie", (assert) => __awaiter(void 0, void 0, void 0, function* () {
                    yield routerTopic.swear(({ matched, router }) => __awaiter(void 0, void 0, void 0, function* () {
                        assert.ok(yield router.dispatch('foo barbie', {}));
                        assert.same(matched, {
                            '<root>': [],
                            'foo': [''],
                            'f*': ['f* barbie']
                        });
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
}));
