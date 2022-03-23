import * as winston from "winston";

import * as core from './core';

export import Color = core.Color;
export import Colors = core.Colors;
export import Level = core.Level;
export import Levels = core.Levels;
export import Priority = core.Priority;
export import Priorities = core.Priorities;

export import Logger = winston.Logger;
export import LoggerOptions = winston.LoggerOptions;
export import Format = winston.Format;

export import levels = core.levels;
export import colors = core.colors;
export import MIN_LEVEL = core.MIN_LEVEL;
export import MAX_LEVEL = core.MAX_LEVEL;

export interface Options {
  meta?: any;
  level?: core.Level;
  logrefLevel?: core.Level;
};

export const formatter: winston.Format;

export function observe(logger: winston.Logger, level: Level): void;
export function createLogger(opts?: Options): winston.Logger;
