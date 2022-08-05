"use strict";
/*
 * router.ts: Base functionality for the router.
 *
 * (C) 2022 Josh Holbrook.
 * (C) 2021 pastelmind <https://github.com/pastelmind>.
 * (C) 2011, Charlie Robbins, Paolo Fragomeni, & the Contributors.
 * MIT LICENSE - See NOTICE file for details.
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
exports.Router = void 0;
const util_1 = require("./util");
//
// ### class Router (routes)
// #### @routes {Object} **Optional** Routing table for this instance.
// The Router object class responsible for building and dispatching from a
// given routing table.
//
class Router {
    constructor(routes = {}) {
        this.params = {};
        this.routes = {};
        this.methods = ['on', 'after', 'before', 'help'];
        this.scope = [];
        this._methods = new Set();
        this._invoked = false;
        this.last = [];
        // TODO: This is repeated in the _getConfig and configure() routes in
        // order to make typescript happy. Is there an actual use case for calling
        // configure() after the fact? or can we delete that method?
        const { recurse, delimiter, strict, notfound, resource, every, } = this._getConfig();
        this._initMethods();
        this.recurse = recurse;
        this.delimiter = delimiter;
        this.strict = strict;
        this.notfound = notfound;
        this.resource = resource;
        this.every = every;
        this.mount(routes);
    }
    _getConfig(options = {}) {
        const recurse = typeof options.recurse === 'undefined' ? this.recurse || false : options.recurse;
        const delimiter = options.delimiter || '\\s';
        const strict = typeof options.strict === 'undefined' ? true : options.strict;
        const notfound = options.notfound || null;
        const resource = options.resource || {};
        //
        // TODO: Global once
        //
        const every = {
            after: options.after,
            before: options.before,
            on: options.on
        };
        return {
            recurse,
            delimiter,
            strict,
            notfound,
            resource,
            every,
        };
    }
    // TODO: Get rid of this
    _initMethods() {
        for (let i = 0; i < this.methods.length; i++) {
            this._methods.add(this.methods[i]);
        }
    }
    //
    // ### method configure (options)
    // #### @options {Object} **Optional** Options to configure this instance with
    // Configures this instance with the specified `options`.
    //
    configure(options) {
        const { recurse, delimiter, strict, notfound, resource, every, } = this._getConfig(options);
        this._initMethods();
        this.recurse = recurse;
        this.delimiter = delimiter;
        this.strict = strict;
        this.notfound = notfound;
        this.resource = resource;
        this.every = every;
        return this;
    }
    //
    // ### method param (token, regex)
    // #### @token {string} Token which to replace (e.g. `:dog`, 'cat')
    // #### @matcher {string|RegExp} Target to replace the token with.
    // Setups up a `params` function which replaces any instance of `token`,
    // inside of a given `str` with `matcher`. This is very useful if you
    // have a common regular expression throughout your code base which
    // you wish to be more DRY.
    //
    param(token, matcher) {
        if (token[0] !== ':') {
            token = ':' + token;
        }
        var compiled = new RegExp(token, 'g');
        this.params[token] = (str) => {
            if (matcher instanceof RegExp) {
                return str.replace(compiled, matcher.source);
            }
            return str.replace(compiled, matcher);
        };
        return this;
    }
    // ### method isMethod (maybeMethod)
    // ### @maybeMethod {string} A string which may potentially be a method
    // Checks if the argument is a registered method on the router.
    isMethod(maybeMethod) {
        return this._methods.has(maybeMethod);
    }
    on(pathOrMethod, routeOrPath, maybeRoute) {
        const method = maybeRoute ? pathOrMethod : "on";
        let path = maybeRoute ? routeOrPath : pathOrMethod;
        const route = maybeRoute ? maybeRoute : routeOrPath;
        const self = this;
        if (Array.isArray(path)) {
            return path.forEach(function (p) {
                self.on(method, p, route);
            });
        }
        if (path instanceof RegExp) {
            path = path.source.replace(/\\\//ig, '/');
        }
        //
        // ### Split the route up by the delimiter.
        //
        let split = path.split(new RegExp(this.delimiter));
        //
        // ### Fix unterminated groups. Fixes #59
        //
        split = (0, util_1.terminator)(split, this.delimiter);
        this.insert(method, this.scope.concat(split), route);
    }
    //
    // ### method path (path, routesFn)
    // #### @path {string|RegExp} Nested scope in which to path
    // #### @routesFn {function} Function to evaluate in the new scope
    // Evalutes the `routesFn` in the given path scope.
    //
    path(_path, routesFn) {
        let length = this.scope.length;
        const path = (_path.source ? _path.source.replace(/\\\//ig, '/') : _path);
        //
        // ### Split the route up by the delimiter.
        //
        let split = path.split(new RegExp(this.delimiter));
        //
        // ### Fix unterminated groups.
        //
        split = (0, util_1.terminator)(split, this.delimiter);
        this.scope = this.scope.concat(path);
        routesFn.call(this);
        this.scope.splice(length, split.length);
    }
    // the type signature of dispatch is incredibly hairy and we have to do
    // a lot of checks to keep it safe, so we push them into a private method
    // here
    _parseDispatchArguments(pathOrMethod, ctxOrPath, maybeCtx) {
        if ((pathOrMethod === 'on' || pathOrMethod === 'before' || pathOrMethod === 'after')
            && typeof ctxOrPath === 'string'
            && typeof maybeCtx !== 'undefined') {
            return [pathOrMethod, ctxOrPath, maybeCtx];
        }
        if (typeof maybeCtx === 'undefined' && typeof ctxOrPath !== 'string') {
            return ['on', pathOrMethod, ctxOrPath];
        }
        throw new Error(`unexpected dispatch arguments: ${pathOrMethod}, ${ctxOrPath}, ${maybeCtx}`);
    }
    dispatch(pathOrMethod, ctxOrPath, maybeCtx) {
        return __awaiter(this, void 0, void 0, function* () {
            let [method, path, ctx] = this._parseDispatchArguments(pathOrMethod, ctxOrPath, maybeCtx);
            //
            // Prepend a single space onto the path so that the traversal
            // algorithm will recognize it. This is because we always assume
            // that the `path` begins with `this.delimiter`.
            //
            path = ' ' + path;
            let fns = this.traverse(method, path.replace(util_1.QUERY_SEPARATOR, ''), this.routes, '');
            const invoked = this._invoked;
            this._invoked = true;
            if (!fns || fns.length === 0) {
                this.last = [];
                if (typeof this.notfound === 'function') {
                    yield this.invoke([this.notfound], ctx);
                }
                return false;
            }
            if (this.recurse === 'forward') {
                fns = fns.reverse();
            }
            const updateAndInvoke = () => __awaiter(this, void 0, void 0, function* () {
                this.last = fns.after;
                // TODO: Typescript things the context may be set to null - but the types
                // should rule that out?
                yield this.invoke(this.runlist(fns), ctx);
            });
            //
            // Builds the list of functions to invoke from this call
            // to dispatch conforming to the following order:
            //
            // 1. Global after (if any)
            // 2. After functions from the last call to dispatch
            // 3. Global before (if any)
            // 4. Global on (if any)
            // 5. Matched functions from routing table (`['before', 'on'], ['before', 'on`], ...]`)
            //
            // TODO: Can we actually trust at this point that `this.last` is defined?
            const after = (this.every && this.every.after
                ? [this.every.after].concat(this.last)
                : [this.last]);
            if (after && after.length > 0 && invoked) {
                yield this.invoke(after, ctx);
                updateAndInvoke();
                return true;
            }
            updateAndInvoke();
            return true;
        });
    }
    //
    // ### method runlist (fns)
    // #### @fns {Array} List of functions to include in the runlist
    // Builds the list of functions to invoke from this call
    // to dispatch conforming to the following order:
    //
    // 1. Global before (if any)
    // 2. Global on (if any)
    // 3. Matched functions from routing table (`['before', 'on'], ['before', 'on`], ...]`)
    //
    runlist(fns) {
        const runlist = this.every && this.every.before
            ? [this.every.before].concat(fns.flat())
            : fns.flat();
        if (this.every && this.every.on) {
            runlist.push(this.every.on);
        }
        // TODO: The type required here is an Array which also has these fields -
        // either optionally or through a cast. Are things passed to runlist
        // definitely handlers? or RouteEntries?
        runlist.captures = fns.captures;
        runlist.source = fns.source;
        return runlist;
    }
    //
    // ### method invoke (fns, thisArg)
    // #### @fns {Array} Set of functions to invoke in order.
    // #### @thisArg {Object} `thisArg` for each function.
    // Invokes the `fns` and awaits the results. Each function must **not**
    // return (or respond) with false, or evaluation will short circuit.
    //
    invoke(fns, ctx) {
        return __awaiter(this, void 0, void 0, function* () {
            const self = this;
            function apply(fn) {
                return __awaiter(this, void 0, void 0, function* () {
                    if (Array.isArray(fn)) {
                        for (let f of fn) {
                            yield apply(f);
                        }
                    }
                    else if (typeof fn === 'function') {
                        return yield fn(ctx, ...fns.captures || []);
                    }
                    else if (typeof fn === 'string' && self.resource) {
                        // NOTE: You *can too* index a resource by method lol
                        yield self.resource[fn](ctx, ...(fns.captures || []));
                    }
                });
            }
            yield apply(fns);
        });
    }
    //
    // ### method traverse (method, path, routes, regexp)
    // #### @method {string} Method to find in the `routes` table.
    // #### @path {string} Path to find in the `routes` table.
    // #### @routes {Object} Partial routing table to match against
    // #### @regexp {string} Partial regexp representing the path to `routes`.
    // #### @filter {function} Filter function for filtering routes (expensive).
    // Core routing logic for `director.Router`: traverses the
    // specified `path` within `this.routes` looking for `method`
    // returning any `fns` that are found.
    //
    traverse(method, path, routes, regexp, filter) {
        let fns = [];
        let current;
        let exact;
        let match;
        let next = null;
        function filterRoutes(routes) {
            if (!filter) {
                return routes;
            }
            function deepCopy(source) {
                var result = [];
                for (var i = 0; i < source.length; i++) {
                    result[i] = Array.isArray(source[i]) ? deepCopy(source[i]) : source[i];
                }
                return result;
            }
            // TODO: This is actually a handler (a Fn | FnList) OR
            // a nested version of this thing.
            function applyFilter(fns) {
                for (let i = fns.length - 1; i >= 0; i--) {
                    if (Array.isArray(fns[i])) {
                        // NOTE: typescript erroneously doesn't recognize Array.isArray
                        // as a guard
                        applyFilter(fns[i]);
                        if (fns[i].length === 0) {
                            fns.splice(i, 1);
                        }
                    }
                    else {
                        // NOTE: A few lines up, outside this closure, we exited early
                        // when filter is undefined. We know it doesn't get defined
                        // elsewhere, so this is safe.
                        //
                        // in addition, the Array.isArray check tells us that fns must
                        // be a Fn, not a FnList.
                        if (!filter(fns[i])) {
                            fns.splice(i, 1);
                        }
                    }
                }
            }
            const newRoutes = deepCopy(routes);
            newRoutes.matched = routes.matched;
            newRoutes.captures = routes.captures;
            // TODO: This casting seems a lil sketch
            newRoutes.after = routes.after.filter(filter);
            applyFilter(newRoutes);
            return newRoutes;
        }
        //
        // Base Case #1:
        // If we are dispatching from the root
        // then only check if the method exists.
        //
        if (path === this.delimiter && routes.on) {
            const _routes = routes;
            // NOTE: The filter step removes any undefined values so this is good to go
            next = [[_routes.before, _routes.on].filter(Boolean)];
            next.after = [_routes.after].filter(Boolean);
            next.matched = true;
            next.captures = [];
            return filterRoutes(next);
        }
        for (let r of Object.keys(routes)) {
            //
            // We dont have an exact match, lets explore the tree
            // in a depth-first, recursive, in-order manner where
            // order is defined as:
            //
            //    ['before', 'on', '<method>', 'after']
            //
            // Remember to ignore keys (i.e. values of `r`) which
            // are actual methods (e.g. `on`, `before`, etc), but
            // which are not actual nested route (i.e. JSON literals).
            //
            // NOTE: This particular check is ensuring that the "r" is a /route/,
            // not a method - in other words, if this check passes then "routes"
            // is a RoutingTable, not a Resource.
            if (!this._methods.has(r) ||
                this._methods.has(r) && typeof routes[r] === 'object' && !Array.isArray(routes[r])) {
                //
                // Attempt to make an exact match for the current route
                // which is built from the `regexp` that has been built
                // through recursive iteration.
                //
                current = exact = regexp + this.delimiter + r;
                if (!this.strict) {
                    exact += '[' + this.delimiter + ']?';
                }
                match = path.match(new RegExp('^' + exact));
                if (!match) {
                    //
                    // If there isn't a `match` then continue. Here, the
                    // `match` is a partial match. e.g.
                    //
                    //    '/foo/bar/buzz'.match(/^\/foo/)   // ['/foo']
                    //    '/no-match/route'.match(/^\/foo/) // null
                    //
                    continue;
                }
                // NOTE: If these types are as we suggest, then that expression will
                // return true :)
                if (match[0] && match[0] == path && routes[r][method]) {
                    // See? I proved it.
                    const _routes = routes;
                    //
                    // ### Base case 2:
                    // If we had a `match` and the capture is the path itself,
                    // then we have completed our recursion.
                    //
                    next = [[_routes[r].before, _routes[r][method]].filter(Boolean)];
                    next.after = [_routes[r].after].filter(Boolean);
                    next.matched = true;
                    next.captures = match.slice(1);
                    if (this.recurse && routes === this.routes) {
                        next.push([_routes.before, _routes.on].filter(Boolean));
                        next.after = next.after.concat([_routes.after].filter(Boolean));
                    }
                    return filterRoutes(next);
                }
                //
                // ### Recursive case:
                // If we had a match, but it is not yet an exact match then
                // attempt to continue matching against the next portion of the
                // routing table.
                //
                // TODO: this.traverse *may* return null - can we justify why we
                // don't need to check this more explicitly?
                next = this.traverse(method, path, routes[r], current);
                //
                // `next.matched` will be true if the depth-first search of the routing
                // table from this position was successful.
                //
                if (next && next.matched) {
                    //
                    // Build the in-place tree structure representing the function
                    // in the correct order.
                    //
                    if (next.length > 0) {
                        fns = fns.concat(next);
                    }
                    if (this.recurse) {
                        const _routes = routes;
                        fns.push([_routes[r].before, _routes[r][method]].filter(Boolean));
                        next.after = next.after.concat([_routes[r].after].filter(Boolean));
                        if (routes === this.routes) {
                            fns.push([_routes['before'], _routes['on']].filter(Boolean));
                            next.after = next.after.concat([_routes['after']].filter(Boolean));
                        }
                    }
                    fns.matched = true;
                    fns.captures = next.captures;
                    fns.after = next.after;
                    //
                    // ### Base case 2:
                    // Continue passing the partial tree structure back up the stack.
                    // The caller for `dispatch()` will decide what to do with the functions.
                    //
                    return filterRoutes(fns);
                }
            }
        }
        return null;
    }
    //
    // ### method insert (method, path, route, context)
    // #### @method {string} Method to insert the specific `route`.
    // #### @path {Array} Parsed path to insert the `route` at.
    // #### @route {Array|function} Route handlers to insert.
    // #### @parent {Object} **Optional** Parent "routes" to insert into.
    // Inserts the `route` for the `method` into the routing table for
    // this instance at the specified `path` within the `context` provided.
    // If no context is provided then `this.routes` will be used.
    //
    insert(method, path, route, parent_) {
        let methodType;
        path = path.filter(function (p) {
            return p && p.length > 0;
        });
        const parent = parent_ || this.routes;
        let part = path.shift();
        // Note: javascript will take undefined in these methods just fine -_-;
        if (/\:|\*/.test(part) && !/\\d|\\w/.test(part)) {
            part = (0, util_1.regifyString)(part, this.params);
        }
        if (path.length > 0) {
            // NOTE: this is safe because this implicitly checks that part is
            // defined
            //
            // If this is not the last part left in the `path`
            // (e.g. `['cities', 'new-york']`) then recurse into that
            // child
            //
            parent[part] = parent[part] || {};
            return this.insert(method, path, route, parent[part]);
        }
        //
        // If there is no part and the path has been exhausted
        // and the parent is the root of the routing table,
        // then we are inserting into the root and should
        // only dive one level deep in the Routing Table.
        //
        if (!part && !path.length && parent === this.routes) {
            methodType = typeof parent[method];
            // TODO: These casts are making a *lot* of bold assumptions - let's
            // see if they pan out
            switch (methodType) {
                case 'function':
                    parent[method] = [parent[method], route];
                    return;
                case 'object':
                    parent[method].push(route);
                    return;
                case 'undefined':
                    parent[method] = route;
                    return;
            }
            return;
        }
        //
        // Otherwise, we are at the end of our insertion so we should
        // insert the `route` based on the `method` after getting the
        // `parent` of the last `part`.
        //
        let parentType = typeof parent[part];
        let isArray = Array.isArray(parent[part]);
        if (parent[part] && !isArray && parentType == 'object') {
            // NOTE: If we found the path part, then we definitely have a
            // RoutingTable! If we grab the property, it's either a fn or
            // another RoutingTable. If it's a routing a table it may
            // have the method defined on it, and if it's a function then it'll
            // be undefined either way.
            methodType = typeof parent[part][method];
            switch (methodType) {
                case 'function':
                    // replace the raw function with a FnList
                    parent[part][method] = [parent[part][method], route];
                    return;
                case 'object':
                    // it's an array, push the inserted route onto it
                    parent[part][method].push(route);
                    return;
                case 'undefined':
                    // well, define it lol
                    parent[part][method] = route;
                    return;
            }
        }
        else if (parentType == 'undefined') {
            const nested = {};
            nested[method] = route;
            parent[part] = nested;
            return;
        }
        throw new Error('Invalid route context: ' + parentType);
    }
    //
    // ### method extend (methods)
    // #### @methods {Array} List of method names to extend this instance with
    // Extends this instance with simple helper methods to `this.on`
    // for each of the specified `methods`
    //
    // TODO: This is *not* type safe lol!!
    extend(methods) {
        const self = this;
        let len = methods.length;
        let i = 0;
        function extend(method) {
            self._methods.add(method);
            self[method] = function (ctx, ...args) {
                let extra = args.length === 1
                    ? [method, '']
                    : [method];
                self.on.apply(self, extra.concat(Array.from(args)));
            };
        }
        for (i = 0; i < len; i++) {
            extend(methods[i]);
        }
    }
    //
    // ### method mount (routes, context)
    // #### @routes {Object} Routes to mount onto this instance
    // Mounts the sanitized `routes` onto the root context for this instance.
    //
    // e.g.
    //
    //    new Router().mount({ '/foo': { '/bar': function foobar() {} } })
    //
    // yields
    //
    //    { 'foo': { 'bar': function foobar() {} } }
    //
    mount(routes, path = []) {
        if (!routes || typeof routes !== "object" || Array.isArray(routes)) {
            return;
        }
        const _path = path instanceof Array ? path : path.split(this.delimiter);
        function isTable(maybeTable) {
            return typeof maybeTable === 'object' && !Array.isArray(maybeTable);
        }
        const insertOrMount = (route) => {
            let parts = route.split(this.delimiter), event = this.isMethod(route) ? route : "on", pathToInsert = _path.concat(parts);
            if (isTable(routes[route])) {
                this.mount(routes[route], pathToInsert);
                return;
            }
            if (!this.isMethod(route)) {
                pathToInsert = (0, util_1.terminator)(pathToInsert, this.delimiter);
            }
            // it's a handler, so insert it
            this.insert(event, pathToInsert, routes[route]);
        };
        for (let route of Object.keys(routes)) {
            insertOrMount(route);
        }
    }
}
exports.Router = Router;
