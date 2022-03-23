import { Level } from './core';


export interface Options {
  v?: boolean;
  verbose?: boolean;
  'log-level'?: Level;
};

export function verbosity(opts: Options, defaultLevel: Level) -> Level;
