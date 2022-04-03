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
const minimist_1 = __importDefault(require("minimist"));
const router_1 = require("./router");
// TODO: if config object is a function, put it on the root route and call it good
class App {
    constructor(options) {
        this.main = (typeof options === 'function' || options instanceof Array) ? options : undefined;
        const opts = {};
        const routingOptions = {};
        const routes = (typeof options !== 'undefined'
            && typeof options !== 'function'
            && !(options instanceof Array))
            ? (options.routes || {})
            : {};
        this.router = new router_1.Router(routes);
        if (typeof options !== 'undefined'
            && typeof options !== 'function'
            && !(options instanceof Array)) {
            // minimist options
            if (typeof options.string !== 'undefined') {
                opts.string = options.string;
            }
            if (typeof options.boolean !== 'undefined') {
                opts.boolean = options.boolean;
            }
            if (typeof options.alias !== 'undefined') {
                opts.alias = options.alias;
            }
            if (typeof options.stopEarly !== 'undefined') {
                opts.stopEarly = options.stopEarly;
            }
            if (typeof options.unknown !== 'undefined') {
                opts.unknown = options.unknown;
            }
            if (typeof options['--'] !== 'undefined') {
                opts['--'] = options['--'];
            }
            // router configuration
            if (typeof options.recurse !== 'undefined') {
                routingOptions.recurse = options.recurse;
            }
            if (typeof options.notfound !== 'undefined') {
                routingOptions.notfound = options.notfound;
            }
            if (typeof options.before !== 'undefined') {
                routingOptions.before = options.before;
            }
            if (typeof options.after !== 'undefined') {
                routingOptions.after = options.after;
            }
            // main
            if (typeof options.main !== 'undefined') {
                this.main = options.main;
            }
        }
        this.router.configure(routingOptions);
        this.opts = opts;
    }
    command(path, route) {
        this.router.on(path, route);
    }
    path(path, routesFn) {
        this.router.path(path, routesFn);
    }
    run(argv) {
        return __awaiter(this, void 0, void 0, function* () {
            const opts = (0, minimist_1.default)(argv, this.opts);
            const path = opts._.join(" ");
            // TODO: the main route *should* work when set as the '' route in our
            // router - however, that *doesn't* work, so we fake it here.
            if (this.main) {
                for (let fn of this.main instanceof Array ? this.main : [this.main]) {
                    yield fn(opts);
                }
            }
            this.router.dispatch(path, opts);
        });
    }
}
exports.App = App;
function app(argv, options) {
    return __awaiter(this, void 0, void 0, function* () {
        const app = new App(options);
        yield app.run(argv);
    });
}
exports.app = app;
