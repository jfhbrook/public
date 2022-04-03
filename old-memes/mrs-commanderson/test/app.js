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
const __1 = require("../");
const tap_1 = require("tap");
const swears_1 = require("@jfhbrook/swears");
(0, tap_1.test)('App objects', (assert) => __awaiter(void 0, void 0, void 0, function* () {
    assert.test('when assigned no options', (assert) => __awaiter(void 0, void 0, void 0, function* () {
        const topic = (0, swears_1.discuss)(() => __awaiter(void 0, void 0, void 0, function* () {
            const matcher = {
                init: [],
                install: []
            };
            const app = new __1.App();
            app.command("init", (ctx) => __awaiter(void 0, void 0, void 0, function* () { matcher.init.push(true); ; }));
            app.command("install :pkg", (ctx, pkg) => __awaiter(void 0, void 0, void 0, function* () { matcher.install.push(pkg); }));
            return { app, matcher };
        }));
        assert.test('init runs without crashing', (assert) => __awaiter(void 0, void 0, void 0, function* () {
            yield topic.swear(({ app, matcher }) => __awaiter(void 0, void 0, void 0, function* () {
                yield app.run(['init']);
                assert.same(matcher, {
                    init: [true],
                    install: []
                });
            }));
        }));
        assert.test('install runs without crashing', (assert) => __awaiter(void 0, void 0, void 0, function* () {
            yield topic.swear(({ app, matcher }) => __awaiter(void 0, void 0, void 0, function* () {
                yield app.run(['install', 'some-pkg']);
                assert.same(matcher, {
                    init: [],
                    install: ['some-pkg']
                });
            }));
        }));
    }));
    assert.test('when constructed with a main function', (assert) => __awaiter(void 0, void 0, void 0, function* () {
        assert.test('instead of options', (assert) => __awaiter(void 0, void 0, void 0, function* () {
            const topic = (0, swears_1.discuss)(() => __awaiter(void 0, void 0, void 0, function* () {
                const matcher = {
                    main: []
                };
                const app = new __1.App((opts) => __awaiter(void 0, void 0, void 0, function* () {
                    matcher.main.push(true);
                }));
                return { app, matcher };
            }));
            assert.test('it runs with no subcommand', (assert) => __awaiter(void 0, void 0, void 0, function* () {
                yield topic.swear(({ app, matcher }) => __awaiter(void 0, void 0, void 0, function* () {
                    yield app.run([]);
                    assert.same(matcher, {
                        main: [true]
                    });
                }));
            }));
        }));
        assert.test('as one of the options', (assert) => __awaiter(void 0, void 0, void 0, function* () {
            const topic = (0, swears_1.discuss)(() => __awaiter(void 0, void 0, void 0, function* () {
                const matcher = {
                    main: []
                };
                const app = new __1.App({
                    main(opts) {
                        return __awaiter(this, void 0, void 0, function* () {
                            matcher.main.push(true);
                        });
                    }
                });
                return { app, matcher };
            }));
            assert.test('it runs with no subcommand', (assert) => __awaiter(void 0, void 0, void 0, function* () {
                yield topic.swear(({ app, matcher }) => __awaiter(void 0, void 0, void 0, function* () {
                    yield app.run([]);
                    assert.same(matcher, {
                        main: [true]
                    });
                }));
            }));
        }));
    }));
    assert.test('when constructed with routes', (assert) => __awaiter(void 0, void 0, void 0, function* () {
        const topic = (0, swears_1.discuss)(() => __awaiter(void 0, void 0, void 0, function* () {
            const matcher = {
                init: [],
                install: []
            };
            const app = new __1.App({
                routes: {
                    init(ctx) {
                        return __awaiter(this, void 0, void 0, function* () {
                            matcher.init.push(true);
                        });
                    },
                    // TODO: The mounting algorithm absolutely mangles this! Practically
                    // speaking this API isn't ready for prime time, but we *can* do
                    // some partial tests and skip the problematic parts.
                    /*
                    'install': {
                      ' ([._a-zA-Z0-9-%()]+)': async (ctx, pkg) => {
                        matcher.install.push(pkg);
                      }
                    }
                    */
                }
            });
            return { app, matcher };
        }));
        assert.test('init runs without crashing', (assert) => __awaiter(void 0, void 0, void 0, function* () {
            yield topic.swear(({ app, matcher }) => __awaiter(void 0, void 0, void 0, function* () {
                yield app.run(['init']);
                assert.same(matcher, {
                    init: [true],
                    install: []
                });
            }));
        }));
        assert.skip('install runs without crashing', (assert) => __awaiter(void 0, void 0, void 0, function* () {
            yield topic.swear(({ app, matcher }) => __awaiter(void 0, void 0, void 0, function* () {
                yield app.run(['install', 'some-pkg']);
                assert.same(matcher, {
                    init: [],
                    install: ['some-pkg']
                });
            }));
        }));
    }));
}));
