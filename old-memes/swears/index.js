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
exports.discuss = exports.Topic = void 0;
class Topic {
    constructor(factory, teardown) {
        this.factory = factory;
        this.teardown = teardown;
        this.t = null;
    }
    discuss(scenario, teardown) {
        return new Topic(() => __awaiter(this, void 0, void 0, function* () {
            const t = yield this.factory();
            this.t = t;
            return scenario(t);
        }), (u) => __awaiter(this, void 0, void 0, function* () {
            if (teardown) {
                yield teardown(u);
            }
            if (this.t && this.teardown) {
                yield this.teardown(this.t);
            }
        }));
    }
    swear(fn) {
        return __awaiter(this, void 0, void 0, function* () {
            const o = yield this.factory();
            yield fn(o);
            if (this.teardown) {
                yield this.teardown(o);
            }
        });
    }
}
exports.Topic = Topic;
function discuss(fn, teardown) {
    return new Topic(fn, teardown);
}
exports.discuss = discuss;
