#!/usr/bin/env node

import minimist, { Opts, ParsedArgs } from "minimist";
import {
  Handler as RouteHandler,
  Matcher,
  Path,
  PathFn as RoutePathFn,
  Router,
  RoutingOptions,
  RoutingTable as BaseRoutingTable,
} from './router';

export {
  Matcher,
  Path
}

export type Handler<Ctx> = RouteHandler<Ctx & ParsedArgs>;
export type PathFn<Ctx> = RoutePathFn<Ctx & ParsedArgs>;
export type RoutingTable<Ctx> = BaseRoutingTable<Ctx & ParsedArgs>;

export interface AppOptions<Ctx> {
  // options passed to minimist. types are more strict, but it's otherwise
  // the same api.
  string?: string[];
  boolean?: string[];
  alias?: { [key: string]: string[] };
  default?: { [key: string]: any };
  stopEarly?: boolean;
  unknown?: (arg: string) => boolean;
  '--'?: boolean;

  // raw routes passed to the router's constructor
  routes?: RoutingTable<Ctx>;

  // options passed to the router's configure method
  recurse?: "forward" | "backward" | false;
  notfound?: Handler<Ctx>;
  before?: Handler<Ctx>;
  after?: Handler<Ctx>;

  // options specific to application.
  main?: Handler<Ctx>;
}

// TODO: if config object is a function, put it on the root route and call it good

export class App<Ctx> {
  public opts: Opts;
  public main: Handler<Ctx> | undefined;
  public router: Router<Ctx & ParsedArgs>;

  constructor(
    options?: AppOptions<Ctx> | Handler<Ctx>
  ) {
    this.main = (typeof options === 'function' || options instanceof Array) ? options : undefined;
    const opts: Opts = {};
    const routingOptions: RoutingOptions<Ctx & ParsedArgs> = {};
    const routes: RoutingTable<Ctx> = (
      typeof options !== 'undefined'
        && typeof options !== 'function'
        && !(options instanceof Array)
      )
        ? (options.routes || {})
        : {}
    this.router = new Router(routes);

    if (
      typeof options !== 'undefined'
        && typeof options !== 'function'
        && !(options instanceof Array)
    ) {
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

  command(path: Path | Matcher, route: Handler<Ctx>): void {
    this.router.on(path, route);
  }

  path(path: Matcher, routesFn: PathFn<Ctx>): void {
    this.router.path(path, routesFn);
  }

  async run(argv: typeof process.argv): Promise<void> {
    const opts: ParsedArgs = minimist(argv, this.opts);
    const path = opts._.join(" ");

    // TODO: the main route *should* work when set as the '' route in our
    // router - however, that *doesn't* work, so we fake it here.
    if (this.main) {
      for (let fn of this.main instanceof Array ? this.main : [this.main]) {
        await fn(<Ctx & ParsedArgs>opts);
      }
    }

    this.router.dispatch(path, <Ctx & ParsedArgs>opts);
  }
}

export async function app<Ctx>(
  argv: typeof process.argv,
  options?: AppOptions<Ctx>
): Promise<void> {
  const app = new App<Ctx>(options);

  await app.run(argv);
}
