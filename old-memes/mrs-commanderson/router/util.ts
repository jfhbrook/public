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

import { Resource, Path, Fn, FnList, Handler, RoutingTable, Matcher, RoutingOptions, RoutingConfig, Filter } from './types';

export const QUERY_SEPARATOR = /\?.*/;

//
// Helper function for expanding "named" matches
// (e.g. `:dog`, etc.) against the given set
// of params:
//
//    {
//      ':dog': function (str) {
//        return str.replace(/:dog/, 'TARGET');
//      }
//      ...
//    }
//
export function paramifyString(str: string | undefined, params: any, mod?: string): string | undefined {
  mod = str;
  for (var param in params) {
    if (params.hasOwnProperty(param)) {
      mod = params[param](str);
      if (mod !== str) { break; }
    }
  }

  return mod === str
    ? '([._a-zA-Z0-9-%()]+)'
    : mod;
}

//
// Helper function for expanding wildcards (*) and
// "named" matches (:whatever)
//
export function regifyString(str: string, params: any): string {
  let matches;
  let last = 0;
  let out = '';

  while (matches = str.substring(last).match(/[^\w\d\- %@&]*\*[^\w\d\- %@&]*/)) {
    if (matches.index == null) {
      throw new Error('assert: matches.index should be defined');
    }
    last = matches.index + matches[0].length;
    matches[0] = matches[0].replace(/^\*/, '([_\.\(\)!\\ %@&a-zA-Z0-9-]+)');
    out += str.substring(0, matches.index) + matches[0];
  }

  str = out += str.substring(last);

  let captures = str.match(/:([^\/]+)/ig);
  let capture;
  let length;

  if (captures) {
    length = captures.length;
    for (var i = 0; i < length; i++) {
      capture = captures[i];
      if ( capture.slice(0, 2) === "::" ) {
        // This parameter was escaped and should be left in the url as a literal
        // Remove the escaping : from the beginning
        str = capture.slice( 1 );
      } else {
        const paramified = paramifyString(capture, params);
        if (!paramified) {
          throw new Error('assert: string should paramify');
        }
        str = str.replace(capture, paramified);
      }
    }
  }

  return str;
}

//
// ### Fix unterminated RegExp groups in routes.
//
export function terminator(routes: string[], delimiter: string, start?: string | number, stop?: string | number): string[] {
  let last = 0;
  let left = 0;
  let right = 0;
  const _start: string = (start || '(').toString();
  const _stop: string = (stop || ')').toString();

  for (let i = 0; i < routes.length; i++) {
    var chunk = routes[i];

    if ((chunk.indexOf(_start, last) > chunk.indexOf(_stop, last)) ||
        (~chunk.indexOf(_start, last) && !~chunk.indexOf(_stop, last)) ||
        (!~chunk.indexOf(_start, last) && ~chunk.indexOf(_stop, last))) {

      left = chunk.indexOf(_start, last);
      right = chunk.indexOf(_stop, last);

      if ((~left && !~right) || (!~left && ~right)) {
        var tmp = routes.slice(0, (i || 1) + 1).join(delimiter);
        routes = [tmp].concat(routes.slice((i || 1) + 1));
      }

      last = (right > left ? right : left) + 1;
      i = 0;
    }
    else {
      last = 0;
    }
  }

  return routes;
}
