#!/usr/bin/env node
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
var __importDefault = (this && this.__importDefault) || function (mod) {
    return (mod && mod.__esModule) ? mod : { "default": mod };
};
Object.defineProperty(exports, "__esModule", { value: true });
exports.app = exports.App = void 0;
const dotenv_1 = __importDefault(require("dotenv"));
const kenny_loggins_1 = require("kenny-loggins");
const minimist_1 = __importDefault(require("minimist"));
const router_1 = require("./router");
// TODO: if config object is a function, put it on the root route and call it good
class App {
    // TODO: Create a bespoke config format and actually use some sense when
    // constructing these - just becaues the types work doesn't mean we're done!!
    constructor(opts, routes, routingOptions) {
        this.opts = opts;
        this.router = new router_1.Router(routes);
        this.router.configure(routingOptions);
    }
    command(path, route) {
        this.router.on(path, route);
    }
    path(path, routesFn) {
        this.router.path(path, routesFn);
    }
    run(argv) {
        return __awaiter(this, void 0, void 0, function* () {
            dotenv_1.default.config();
            const opts = (0, minimist_1.default)(argv, this.opts);
            const logger = (0, kenny_loggins_1.createLogger)();
            this.router.dispatch(opts._.join(" "), { logger, opts });
        });
    }
}
exports.App = App;
function app(argv, opts, routes, routingOptions) {
    return __awaiter(this, void 0, void 0, function* () {
        const app = new App(opts, routes, routingOptions);
        yield app.run(argv);
    });
}
exports.app = app;
