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
const _1 = require(".");
(0, tap_1.test)('a boring ol topic', (assert) => __awaiter(void 0, void 0, void 0, function* () {
    const topic = (0, _1.discuss)(() => __awaiter(void 0, void 0, void 0, function* () {
        return { a: true };
    }));
    assert.test('can execute swears', (assert) => __awaiter(void 0, void 0, void 0, function* () {
        yield topic.swear((a) => __awaiter(void 0, void 0, void 0, function* () {
            assert.ok(a.a);
            assert.notOk(a.b);
        }));
    }));
    assert.test('can execute child swears', (assert) => __awaiter(void 0, void 0, void 0, function* () {
        const spicierTopic = topic.discuss((a) => __awaiter(void 0, void 0, void 0, function* () {
            // Doing a side effect to test that we create a new instance
            // every swear
            const ctx = a;
            ctx.b = true;
            return ctx;
        }));
        yield spicierTopic.swear((b) => __awaiter(void 0, void 0, void 0, function* () {
            assert.ok(b.a);
            assert.ok(b.b);
        }));
        assert.test("executing child swears doesn't mutate the parent", (assert) => __awaiter(void 0, void 0, void 0, function* () {
            yield topic.swear((a) => __awaiter(void 0, void 0, void 0, function* () {
                assert.ok(a.a);
                assert.notOk(a.b);
            }));
        }));
    }));
}));
