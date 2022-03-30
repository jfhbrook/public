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

// path-likes - strings and splitted strings, potentially with attached properties
interface PathProps {
}

export type Path = (string | string[]) & PathProps;


// a straightforward route handling function, potentially with attached properties
export interface Fn<Ctx> {
  (ctx: Ctx, ...params: string[]): Promise<any>;
}

// an array of route-handling functions, potentially with attached properties
interface FnListProps<Ctx> {
}

export type FnList<Ctx> = Array<Fn<Ctx>> & FnListProps<Ctx>;

// a handler is either a function list or a function
export type Handler<Ctx> = FnList<Ctx> | Fn<Ctx>;

// it's possible through the API to add other method types, but in my project
// I'm just using the 3 so I type them here
export interface Resource<Ctx> {
  on?: Handler<Ctx>;
  before?: Handler<Ctx>;
  after?: Handler<Ctx>;
}

// a routing table - this is what may be passed into the constructor, but
// it's also a node type
export interface RoutingTable<Ctx> {
    [route: string]: RoutingObject<Ctx>;
}

export type RoutingObject<Ctx> = RoutingTable<Ctx> | Resource<Ctx> | Handler<Ctx>;

export type RoutingLeaf<Ctx> = Fn<Ctx>;

export type RoutingNode<Ctx> = Array<RoutingNode<Ctx>> | RoutingLeaf<Ctx>

export type RoutingStem<Ctx> = Array<RoutingNode<Ctx>>

// a type to capture "string or RegExp", though attempting to better handle
// the codebase detecting RegExps by checking the "source" property :)
interface MatcherProps {
  source?: string
}

export type Matcher = (string & MatcherProps) | (RegExp & MatcherProps);
/**
 * Router options object
 */
export interface RoutingOptions<Ctx> {
    /**
     * Controls route recursion.
     * Default is `false` client-side, and `"backward"` server-side.
     */
    recurse?: "forward" | "backward" | false | undefined;
    /**
     * If set to `false`, then trailing slashes (or other delimiters) are
     * allowed in routes. Default is `true`.
     */
    strict?: boolean | undefined;
    /**
     * Character separator between route fragments. Default is `/`.
     */
    delimiter?: string | undefined;
    /**
     * Function to call if no route is found on a call to `router.dispatch()`.
     */
    notfound?: Fn<Ctx> | undefined;
    /**
     * A function (or list of functions) to call on every call to
     * `router.dispatch()` when a route is found.
     */
    on?: Handler<Ctx> | undefined;
    /**
     *  A function (or list of functions) to call before every call to
     * `router.dispatch()` when a route is found.
     */
    before?: Handler<Ctx> | undefined;

    /**
     * A function (or list of functions) to call after every call to
     * `router.dispatch()` when a route is found.
     */
    after?: Handler<Ctx> | undefined;

    resource?: Resource<Ctx> | undefined;
}

// An internal object containing before/after/on functions
export interface Every<ThisType> {
  before?: Handler<ThisType> | undefined;
  after?: Handler<ThisType> | undefined;
  on?: Handler<ThisType> | undefined;
}

/**
 * The return type of Router._getConfig, which gets mixed in with the instance
 */
export interface RoutingConfig<Ctx> {
    recurse: "forward" | "backward" | false;
    strict: boolean;
    delimiter: string;
    notfound: Fn<Ctx> | null;
    resource: Resource<Ctx>;
    every: Every<Ctx>;
}

// a filter argument for route-finding
export type Filter<Ctx> = (fn: Fn<Ctx>) => boolean;
