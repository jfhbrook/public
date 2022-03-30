"use strict";
/*
 * on.ts: Tests for the on/route method.
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
function noop() {
    return __awaiter(this, void 0, void 0, function* () { });
}
;
(0, tap_1.test)('router/insert', (assert) => __awaiter(void 0, void 0, void 0, function* () {
    assert.test("An instance of Router", (assert) => __awaiter(void 0, void 0, void 0, function* () {
        const topic = (0, swears_1.discuss)(() => __awaiter(void 0, void 0, void 0, function* () {
            return new router_1.Router();
        }));
        assert.test("the on() method", (assert) => __awaiter(void 0, void 0, void 0, function* () {
            assert.test("['foo', 'bar']", (assert) => __awaiter(void 0, void 0, void 0, function* () {
                yield topic.swear((router) => __awaiter(void 0, void 0, void 0, function* () {
                    router.on(['foo', 'bar'], noop);
                    assert.equal(router.routes.foo.on, noop);
                    assert.equal(router.routes.bar.on, noop);
                }));
            }));
            assert.test("'baz'", (assert) => __awaiter(void 0, void 0, void 0, function* () {
                yield topic.swear((router) => __awaiter(void 0, void 0, void 0, function* () {
                    router.on('baz', noop);
                    assert.equal(router.routes.baz.on, noop);
                }));
            }));
            assert.test("'after', 'baz'", (assert) => __awaiter(void 0, void 0, void 0, function* () {
                yield topic.swear((router) => __awaiter(void 0, void 0, void 0, function* () {
                    router.on('after', 'boo', noop);
                    assert.equal(router.routes.boo.after, noop);
                }));
            }));
        }));
    }));
}));
