#!/usr/bin/env node

import * as director from "director";
import dotenv from "dotenv";
import { createLogger, Logger } from "kenny-loggins";
import minimist, { Opts, ParsedArgs } from "minimist";

type RouterContext = director.cli.CliRouterContext<Router>;
type Path = director.BaseOrArray<string | RegExp>;

// lolsob
interface RouteEntry {
  (this: RouterContext, ...args: any[]): Promise<any>
}

interface Options {
  routes: director.RoutingTable<RouterContext>;
  routingOptions: director.RoutingOptions<Router>;
  minimistOpts: Opts;
}

function asyncRoute(route: RouteEntry): director.RouteEntry<RouterContext> {
  return function wrapped(this: RouterContext, ...args: any[]) {
    let next: ((err?: any) => void) | null = null;

    if (args.length && typeof args[args.length - 1] === 'function') {
      next = args.pop();
    }

    route.call(this, ...args).then(() => {
      if (next) {
        next();
      }
    }, (err) => {
      if (next) {
        next(err);
      } else {
        throw err;
      }
    });
  };
}

export class Router {
  router: director.cli.Router<Router>;

  constructor(options: Options) {
    this.router = new director.cli.Router(options.routes);
  }

  on(path: Path, route: RouteEntry) : void {
    this.router.on(path, asyncRoute(route));
  }

  dispatch(path: string): Promise<boolean> {
    return new Promise((resolve, reject) => {
      const rv: boolean = this.router.dispatch('', path, this, (err) => {
        if (err) {
          reject(err);
          return;
        }
        // if it gets here, the route fired
        resolve(true);
      });

      if (!rv) {
        // if it didn't match, we'll need to resolve it ourselves
        resolve(false);
      }
    });
  }
}

/* to make director behave correctly w/ async functions:
 * 1. set async to true
 * 2. wrap handlers to call next
 */
