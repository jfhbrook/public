"use strict";
/*
 * insert-test.js: Tests for inserting routes into a normalized routing table.
 *
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
function route() {
    return __awaiter(this, void 0, void 0, function* () { });
}
(0, tap_1.test)('router/insert', (assert) => __awaiter(void 0, void 0, void 0, function* () {
    assert.test("An instance of Router", (assert) => __awaiter(void 0, void 0, void 0, function* () {
        const topic = (0, swears_1.discuss)(() => __awaiter(void 0, void 0, void 0, function* () {
            const router = new router_1.Router();
            return router;
        }));
        assert.skip("the insert() method", (assert) => __awaiter(void 0, void 0, void 0, function* () {
            assert.test("'on', ['foo', 'bar']", (assert) => __awaiter(void 0, void 0, void 0, function* () {
                yield topic.swear((router) => __awaiter(void 0, void 0, void 0, function* () {
                    router.insert('on', ['foo', 'bar'], route);
                    assert.equal(router.routes.foo.bar.on, route);
                }));
            }));
            assert.test("'on', ['foo', 'bar'] again", (assert) => __awaiter(void 0, void 0, void 0, function* () {
                yield topic.swear((router) => __awaiter(void 0, void 0, void 0, function* () {
                    router.insert('on', ['foo', 'bar'], route);
                    assert.type(router.routes.foo.bar.on, Array);
                    assert.equal(router.routes.foo.bar.on.length, 2);
                }));
            }));
            assert.test("'on', ['foo', 'bar'] a third time", (assert) => __awaiter(void 0, void 0, void 0, function* () {
                yield topic.swear((router) => __awaiter(void 0, void 0, void 0, function* () {
                    router.insert('on', ['foo', 'bar'], route);
                    assert.type(router.routes.foo.bar.on, Array);
                    assert.equal(router.routes.foo.bar.on.length, 3);
                }));
            }));
            assert.test("'get', ['fizz', 'buzz']", (assert) => __awaiter(void 0, void 0, void 0, function* () {
                yield topic.swear((router) => __awaiter(void 0, void 0, void 0, function* () {
                    router.insert('get', ['fizz', 'buzz'], route);
                    assert.equal(router.routes.fizz.buzz.get, route);
                }));
            }));
        }));
    }));
}));
