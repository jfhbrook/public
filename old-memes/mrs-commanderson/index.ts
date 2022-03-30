#!/usr/bin/env node

import dotenv from "dotenv";
import { createLogger, Logger } from "kenny-loggins";
import minimist, { Opts, ParsedArgs } from "minimist";
import {
  Handler,
  Path,
  PathFn,
  Matcher,
  Router,
  RoutingOptions,
  RoutingTable,
} from './router';

export interface AppContext {
  opts: ParsedArgs;
  logger: Logger;
}

// TODO: if config object is a function, put it on the root route and call it good

export class App {
  private router: Router<AppContext>;

  // TODO: Create a bespoke config format and actually use some sense when
  // constructing these - just becaues the types work doesn't mean we're done!!
  constructor(
    public opts?: Opts,
    routes?: RoutingTable<AppContext>,
    routingOptions?: RoutingOptions<AppContext>
  ) {
    this.router = new Router(routes);
    this.router.configure(routingOptions);
  }

  command(path: Path, route: Handler<AppContext>): void {
    this.router.on(path, route);
  }

  path(path: Matcher, routesFn: PathFn<AppContext>): void {
    this.router.path(path, routesFn);
  }

  async run(argv: typeof process.argv): Promise<void> {
    dotenv.config();

    const opts: ParsedArgs = minimist(argv, this.opts);

    const logger: Logger = createLogger();

    this.router.dispatch(opts._.join(" "), { logger, opts });
  }
}

export async function app(
  argv: typeof process.argv,
  opts?: Opts,
  routes?: RoutingTable<AppContext>,
  routingOptions?: RoutingOptions<AppContext>
): Promise<void> {
  const app = new App(opts, routes, routingOptions);

  await app.run(argv);
}
