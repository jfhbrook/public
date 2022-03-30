/*
 * router.ts: Base functionality for the router.
 *
 * This code combines router.js from https://github.com/flatiron/director
 * with the types from https://github.com/DefinitelyTyped/DefinitelyTyped
 * and updated to use TypeScript.
 *
 * (C) 2022 Josh Holbrook.
 * (C) 2021 the DefinitelyTyped Contributors.
 * (C) 2011, Charlie Robbins, Paolo Fragomeni, & the Contributors.
 * MIT LICENSE - See NOTICE file for details.
 *
 */

import { Every, Resource, Path, Fn, FnList, Handler, RoutingTable, Matcher, RoutingOptions, RoutingConfig, Filter } from './types';

import { QUERY_SEPARATOR, paramifyString, regifyString, terminator } from './util';

export type PathFn<Ctx> = (this: Router<Ctx>) => Promise<void>;

// TODO: trying to pin down some internal interfaces
export type FnNode<Ctx> = FnList<Ctx> | Fn<Ctx>;

interface RunListProps<Ctx> {
}

export type RunList<Ctx> = Array<Handler<Ctx>> & RunListProps<Ctx>;

// TODO: what is this for?
type Params = Record<string, any>;

//
// ### class Router (routes)
// #### @routes {Object} **Optional** Routing table for this instance.
// The Router object class responsible for building and dispatching from a
// given routing table.
//
export class Router<Ctx> {
  params: Params;
  routes: Record<string, any>;
  methods: string[];
  scope: any[];
  private _methods: Record<string, boolean>;
  private _invoked: boolean;
  private last: Handler<Ctx>;

  recurse: "forward" | "backward" | false;
  delimiter: string;
  strict: boolean;
  notfound: Handler<Ctx> | null;
  resource: Resource<Ctx>;
  every: Every<Ctx>;

  constructor (routes?: RoutingTable<Ctx> = {}) {
    this.params   = {};
    this.routes   = {};
    this.methods  = ['on', 'after', 'before'];
    this.scope    = [];
    // methods which have already been added
    this._methods = {};
    this._invoked = false;
    this.last = [];

    // TODO: This is repeated in the _getConfig and configure() routes in
    // order to make typescript happy. Is there an actual use case for calling
    // configure() after the fact? or can we delete that method?
    const {
      recurse,
      delimiter,
      strict,
      notfound,
      resource,
      every,
    } = this._getConfig();

    this._initMethods()
    this.recurse = recurse;
    this.delimiter = delimiter;
    this.strict = strict;
    this.notfound = notfound;
    this.resource = resource;
    this.every = every;

    this.mount(routes);
  }

  private _getConfig(options: RoutingOptions<Ctx> = {}): RoutingConfig<Ctx> {
    const recurse: 'forward' | 'backward' | false   = typeof options.recurse === 'undefined' ? this.recurse || false : options.recurse;
    const delimiter: string  = options.delimiter || '\\s';
    const strict: boolean    = typeof options.strict === 'undefined' ? true : options.strict;
    const notfound  = options.notfound || null;
    const resource  = options.resource || {};

    //
    // TODO: Global once
    //
    const every: Every<Ctx> = {
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

  private _initMethods(): void {
    for (let i = 0; i < this.methods.length; i++) {
      this._methods[this.methods[i]] = true;
    }
  }

  //
  // ### method configure (options)
  // #### @options {Object} **Optional** Options to configure this instance with
  // Configures this instance with the specified `options`.
  //
  configure(options?: RoutingOptions<Ctx>) {
    const {
      recurse,
      delimiter,
      strict,
      notfound,
      resource,
      every,
    } = this._getConfig(options);

    this._initMethods()
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
  param(token: string, matcher: Matcher) {
    if (token[0] !== ':') {
      token = ':' + token;
    }

    var compiled = new RegExp(token, 'g');
    this.params[token] = (str: string) => {
      if (matcher instanceof RegExp) {
        return str.replace(compiled, matcher.source);
      }
      return str.replace(compiled, matcher);
    };
    return this;
  }

  //
  // ### method on (method, path, route)
  // #### @method {string} **Optional** Method to use
  // #### @path {Array|string} Path to set this route on.
  // #### @route {Array|function} Handler for the specified method and path.
  // Adds a new `route` to this instance for the specified `method`
  // and `path`.
  //
  command(path: Path, route: Handler<Ctx>): void {
    const self = this;

    if (Array.isArray(path)) {
      return path.forEach(function(p) {
        self.command(p, route);
      });
    }

    if (<any>path instanceof RegExp) {
      path = (<RegExp><unknown>path).source.replace(/\\\//ig, '/');
    }

    //
    // ### Split the route up by the delimiter.
    //
    let split = path.split(new RegExp(this.delimiter));

    //
    // ### Fix unterminated groups. Fixes #59
    //
    split = terminator(split, this.delimiter);

    this.insert(method, this.scope.concat(split), route);
  }

  //
  // ### method path (path, routesFn)
  // #### @path {string|RegExp} Nested scope in which to path
  // #### @routesFn {function} Function to evaluate in the new scope
  // Evalutes the `routesFn` in the given path scope.
  //
  path(_path: Matcher, routesFn: PathFn<Ctx>) {
    let length = this.scope.length;

    // TODO: What is _path.source??
    const path = <string>(_path.source ? _path.source.replace(/\\\//ig, '/') : _path);

    //
    // ### Split the route up by the delimiter.
    //
    let split = path.split(new RegExp(this.delimiter));

    //
    // ### Fix unterminated groups.
    //
    split = terminator(split, this.delimiter);
    this.scope = this.scope.concat(path);

    // TODO: lol!!
    routesFn.call(this, this);
    this.scope.splice(length, split.length);
  }

  //
  // ### method dispatch (method, path)
  // #### @method {string} Method to dispatch
  // #### @path {string} Path to dispatch
  // Finds a set of functions on the traversal towards
  // `method` and `path` in the core routing table then
  // invokes them based on settings in this instance.
  //
  async dispatch(method: string, path: string, tty: Ctx) {
    //
    // Prepend a single space onto the path so that the traversal
    // algorithm will recognize it. This is because we always assume
    // that the `path` begins with `this.delimiter`.
    //
    path = ' ' + path;

    let fns = this.traverse(method, path.replace(QUERY_SEPARATOR, ''), this.routes, '');
    const invoked = this._invoked;
    let after;

    this._invoked = true;
    if (!fns || fns.length === 0) {
      this.last = [];
      if (typeof this.notfound === 'function') {
        // TODO: Do we really want "tty" to be the this type?
        await this.invoke([this.notfound], ctx);
      }

      return false;
    }

    if (this.recurse === 'forward') {
      fns = fns.reverse();
    }

    const updateAndInvoke = async () {
      this.last = fns.after;
      await this.invoke(this.runlist(fns), ctx);
    }

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
    after = this.every && this.every.after
      ? [this.every.after].concat(this.last)
      : [this.last];

    if (after && after.length > 0 && invoked) {
      await this.invoke(after, this);
      updateAndInvoke();

      return true;
    }

    updateAndInvoke();
    return true;
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
  runlist(fns: FnList<Ctx>): RunList<Ctx> {
    // So here, "every" is a Handler, so we'd have a List<Handler>, but fns is a list of fn's
    const runlist: RunList<Ctx> = this.every && this.every.before
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
  async invoke(fns: FnList<Ctx>, ctx: Ctx) {
    const self = this;
    async function apply (fn) {
      if (Array.isArray(fn)) {
        for (let f of fn) {
          await apply(f);
        }
      } else if (typeof fn === 'function') {
        return await fn(ctx, fns.captures || []);
      } else if (typeof fn === 'string' && self.resource) {
        await self.resource[fn](ctx, ...(fns.captures || []));
      }
    }

    await apply(fns);
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
  traverse(method: string, path: string, routes: RoutingTable<Router>, regexp: Matcher, filter?: (fn: any) => boolean): FnList<Router> {
    let fns: any[] = [];
    let current;
    let exact;
    let match;
    let next;

    function filterRoutes(routes: RoutingTable<Ctx>) {
      if (!filter) {
        return routes;
      }

      // - it's a list
      // - the list may have arrays that may be deep-copied again, or
      // - or it's a function and that's it
      function deepCopy<T>(source: Array<T | Array<T>>): RoutingTable<Ctx> {
        var result = [];
        for (var i = 0; i < source.length; i++) {
          result[i] = Array.isArray(source[i]) ? deepCopy(source[i]) : source[i];
        }
        return <T>result;
      }

      // TODO: This is actually a handler (a Fn | FnList) OR
      // a nested version of this thing.
      function applyFilter(fns: Handler<Ctx>[]) {
        for (let i = fns.length - 1; i >= 0; i--) {
          if (Array.isArray(fns[i])) {
            applyFilter(fns[i]);
            if (fns[i].length === 0) {
              fns.splice(i, 1);
            }
          }
          else {
            if (!(filter)(fns[i])) {
              fns.splice(i, 1);
            }
          }
        }
      }

      const newRoutes = deepCopy(routes);
      newRoutes.matched = routes.matched;
      newRoutes.captures = routes.captures;
      newRoutes.after = routes.after.filter(filter);

      applyFilter(newRoutes);

      return newRoutes;
    }

    //
    // Base Case #1:
    // If we are dispatching from the root
    // then only check if the method exists.
    //
    if (path === this.delimiter && routes.command) {
      next = [[routes.before, routes.command].filter(Boolean)];
      next.after = [routes.after].filter(Boolean);
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
      if (routes.hasOwnProperty(r) && (!this._methods[r] ||
        this._methods[r] && typeof routes[r] === 'object' && !Array.isArray(routes[r]))) {
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

        if (match[0] && match[0] == path && routes[r][method]) {
          //
          // ### Base case 2:
          // If we had a `match` and the capture is the path itself,
          // then we have completed our recursion.
          //
          next = [[routes[r].before, routes[r][method]].filter(Boolean)];
          next.after = [routes[r].after].filter(Boolean);
          next.matched = true;
          next.captures = match.slice(1);

          if (this.recurse && routes === this.routes) {
            next.push([routes.before, routes.on].filter(Boolean));
            next.after = next.after.concat([routes.after].filter(Boolean));
          }

          return filterRoutes(next);
        }

        //
        // ### Recursive case:
        // If we had a match, but it is not yet an exact match then
        // attempt to continue matching against the next portion of the
        // routing table.
        //
        next = this.traverse(method, path, routes[r], current);

        //
        // `next.matched` will be true if the depth-first search of the routing
        // table from this position was successful.
        //
        if (next.matched) {
          //
          // Build the in-place tree structure representing the function
          // in the correct order.
          //
          if (next.length > 0) {
            fns = fns.concat(next);
          }

          if (this.recurse) {
            fns.push([routes[r].before, routes[r][method]].filter(Boolean));
            next.after = next.after.concat([routes[r].after].filter(Boolean));

            if (routes === this.routes) {
              fns.push([routes['before'], routes['on']].filter(Boolean));
              next.after = next.after.concat([routes['after']].filter(Boolean));
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

    return false;
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
  insert(method: string, path: string[], route: Handler<Router>, parent?: Handler<Router>[]) {
    let methodType;
    let parentType;
    let isArray;
    let nested;
    let part;

    path = path.filter(function (p) {
      return p && p.length > 0;
    });

    parent = parent || this.routes;
    part = path.shift();
    if (/\:|\*/.test(part) && !/\\d|\\w/.test(part)) {
      part = regifyString(part, this.params);
    }

    if (path.length > 0) {
      // NOTE: this is safe because this implicitly checks that part is
      // defined
      //
      // If this is not the last part left in the `path`
      // (e.g. `['cities', 'new-york']`) then recurse into that
      // child
      //
      parent[<string>part] = parent[<string>part] || {};
      return this.insert(path, route, parent[<string>part]);
    }

    //
    // If there is no part and the path has been exhausted
    // and the parent is the root of the routing table,
    // then we are inserting into the root and should
    // only dive one level deep in the Routing Table.
    //
    if (!part && !path.length && parent === this.routes) {
      methodType = typeof parent[method];

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
    parentType = typeof parent[part];
    isArray = Array.isArray(parent[part]);

    if (parent[part] && !isArray && parentType == 'object') {
      methodType = typeof parent[part][method];

      switch (methodType) {
        case 'function':
          parent[part][method] = [parent[part][method], route];
          return;
        case 'object':
          parent[part][method].push(route);
          return;
        case 'undefined':
          parent[part][method] = route;
          return;
      }
    }
    else if (parentType == 'undefined') {
      nested = {};
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
  extend(methods: string[]) {
    var self = this,
        len = methods.length,
        i;

    function extend(method: string) {
      self._methods[method] = true;
      self[method] = function (...args) {
        let extra = args.length === 1
          ? [method, '']
          : [method];

        // TODO: jesus christ
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
  //    { 'foo': 'bar': function foobar() {} } }
  //
  mount(routes: RoutingTable<Ctx> | Handler<Ctx>, path: Path = []) {
    if (!routes || typeof routes !== "object" || Array.isArray(routes)) {
      return;
    }

    const _path: string[] = path instanceof Array ? path : path.split(this.delimiter);

    const insertOrMount = (route: string, local: string[]) => {
      var rename = route,
          parts = route.split(this.delimiter),
          routeType = typeof routes[route],
          isRoute = parts[0] === "" || !this._methods[parts[0]],
          event = isRoute ? "on" : rename;

      if (isRoute) {
        rename = rename.slice((rename.match(new RegExp('^' + this.delimiter)) || [''])[0].length);
        parts.shift();
      }

      if (isRoute && routeType === 'object' && !Array.isArray(routes[route])) {
        local = local.concat(parts);
        this.mount(routes[route], local);
        return;
      }

      if (isRoute) {
        local = local.concat(rename.split(self.delimiter));
        local = terminator(local, self.delimiter);
      }

      this.insert(event, local, routes[route]);
    }

    for (let route of Object.keys(routes)) {
      insertOrMount(route, _path.slice(0));
    }
  }
}

