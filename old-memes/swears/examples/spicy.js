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
const __1 = require("../");
(0, tap_1.test)('when engaging with the discourse', (assert) => __awaiter(void 0, void 0, void 0, function* () {
    const topic = (0, __1.discuss)(() => __awaiter(void 0, void 0, void 0, function* () {
        return { spiceLevel: 0 };
    }));
    assert.test('and the discourse gets rowdy', (assert) => __awaiter(void 0, void 0, void 0, function* () {
        const spicierTopic = topic.discuss((discourse) => __awaiter(void 0, void 0, void 0, function* () {
            discourse.spiceLevel++;
            return discourse;
        }));
        assert.test('things get a little spicy', (assert) => __awaiter(void 0, void 0, void 0, function* () {
            yield spicierTopic.swear((discourse) => __awaiter(void 0, void 0, void 0, function* () {
                assert.equal(discourse.spiceLevel, 1);
            }));
        }));
    }));
}));
