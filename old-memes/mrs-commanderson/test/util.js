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
function testRoute(path) {
    return () => __awaiter(this, void 0, void 0, function* () {
        const router = new router_1.Router();
        router.on(path, () => __awaiter(this, void 0, void 0, function* () { }));
        return (path) => router.dispatch('on', path);
    });
}
;
(0, tap_1.test)('router/regifyString', (assert) => __awaiter(void 0, void 0, void 0, function* () {
    assert.test('When using "/home(.*)"', (assert) => __awaiter(void 0, void 0, void 0, function* () {
        const topic = (0, swears_1.discuss)(testRoute('/home(.*)'));
        assert.test('Should match "/homepage"', (assert) => __awaiter(void 0, void 0, void 0, function* () {
            yield topic.swear((dispatch) => __awaiter(void 0, void 0, void 0, function* () {
                assert.ok(yield dispatch('/homepage'));
            }));
        }));
        assert.test('Should match "/home/page"', (assert) => __awaiter(void 0, void 0, void 0, function* () {
            yield topic.swear((dispatch) => __awaiter(void 0, void 0, void 0, function* () {
                assert.ok(yield dispatch('/home/page'));
            }));
        }));
        assert.test('Should not match "/foo-bar"', (assert) => __awaiter(void 0, void 0, void 0, function* () {
            yield topic.swear((dispatch) => __awaiter(void 0, void 0, void 0, function* () {
                assert.notOk(yield dispatch('/foo-bar'));
            }));
        }));
    }));
    assert.test('When using "/home.*"', (assert) => __awaiter(void 0, void 0, void 0, function* () {
        const topic = (0, swears_1.discuss)(testRoute('/home.*'));
        assert.test('Should match "/homepage"', (assert) => __awaiter(void 0, void 0, void 0, function* () {
            yield topic.swear((dispatch) => __awaiter(void 0, void 0, void 0, function* () {
                assert.ok(yield dispatch('/homepage'));
            }));
        }));
        assert.test('Should match "/home/page"', (assert) => __awaiter(void 0, void 0, void 0, function* () {
            yield topic.swear((dispatch) => __awaiter(void 0, void 0, void 0, function* () {
                assert.ok(yield dispatch('/home/page'));
            }));
        }));
        assert.test('Should not match "/foo-bar"', (assert) => __awaiter(void 0, void 0, void 0, function* () {
            yield topic.swear((dispatch) => __awaiter(void 0, void 0, void 0, function* () {
                assert.notOk(yield dispatch('/foo-bar'));
            }));
        }));
    }));
    assert.test('When using "/home(page[0-9])*"', (assert) => __awaiter(void 0, void 0, void 0, function* () {
        const topic = (0, swears_1.discuss)(testRoute('/home(page[0-9])*'));
        assert.test('Should match "/home"', (assert) => __awaiter(void 0, void 0, void 0, function* () {
            yield topic.swear((dispatch) => __awaiter(void 0, void 0, void 0, function* () {
                assert.ok(yield dispatch('/home'));
            }));
        }));
        assert.test('Should match "/homepage0", "/homepage1", etc.', (assert) => __awaiter(void 0, void 0, void 0, function* () {
            yield topic.swear((dispatch) => __awaiter(void 0, void 0, void 0, function* () {
                for (let i = 0; i < 10; i++) {
                    assert.ok(yield dispatch('/homepage' + i));
                }
            }));
        }));
        assert.test('Should not match "/home_page"', (assert) => __awaiter(void 0, void 0, void 0, function* () {
            yield topic.swear((dispatch) => __awaiter(void 0, void 0, void 0, function* () {
                assert.notOk(yield dispatch('/home_page'));
            }));
        }));
        assert.test('Should not match "/home/page"', (assert) => __awaiter(void 0, void 0, void 0, function* () {
            yield topic.swear((dispatch) => __awaiter(void 0, void 0, void 0, function* () {
                assert.notOk(yield dispatch('/home/page'));
            }));
        }));
    }));
    assert.test('When using "/home*"', (assert) => __awaiter(void 0, void 0, void 0, function* () {
        const topic = (0, swears_1.discuss)(testRoute('/home*'));
        assert.test('Should match "/homepage"', (assert) => __awaiter(void 0, void 0, void 0, function* () {
            yield topic.swear((dispatch) => __awaiter(void 0, void 0, void 0, function* () {
                assert.ok(yield dispatch('/homepage'));
            }));
        }));
        assert.test('Should match "/home_page"', (assert) => __awaiter(void 0, void 0, void 0, function* () {
            yield topic.swear((dispatch) => __awaiter(void 0, void 0, void 0, function* () {
                assert.ok(yield dispatch('/home_page'));
            }));
        }));
        assert.test('Should match "/home-page"', (assert) => __awaiter(void 0, void 0, void 0, function* () {
            yield topic.swear((dispatch) => __awaiter(void 0, void 0, void 0, function* () {
                assert.ok(yield dispatch('/home-page'));
            }));
        }));
        assert.test('Should not match "/home/page"', (assert) => __awaiter(void 0, void 0, void 0, function* () {
            yield topic.swear((dispatch) => __awaiter(void 0, void 0, void 0, function* () {
                assert.ok(yield dispatch('/home/page'));
            }));
        }));
    }));
    assert.test('When using "/folder/::home"', (assert) => __awaiter(void 0, void 0, void 0, function* () {
        const topic = (0, swears_1.discuss)(testRoute('/folder/::home'));
        assert.test('Should match "/folder/:home"', (assert) => __awaiter(void 0, void 0, void 0, function* () {
            yield topic.swear((dispatch) => __awaiter(void 0, void 0, void 0, function* () {
                assert.ok(yield dispatch('/folder/:home'));
            }));
        }));
        assert.test('Should not match "/folder/::home"', (assert) => __awaiter(void 0, void 0, void 0, function* () {
            yield topic.swear((dispatch) => __awaiter(void 0, void 0, void 0, function* () {
                assert.notOk(yield dispatch('/folder/::home'));
            }));
        }));
        assert.test('Should not match "/folder/abc" (the catchall regexp)"', (assert) => __awaiter(void 0, void 0, void 0, function* () {
            yield topic.swear((dispatch) => __awaiter(void 0, void 0, void 0, function* () {
                assert.notOk(yield dispatch('/folder/abc'));
            }));
        }));
    }));
}));
