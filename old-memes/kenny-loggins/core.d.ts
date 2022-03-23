export type Level = string;
export type Priority = number;
export type Levels = { [level: Level]: Priority };
export type Priorities = Level[];
export type Color = string;
export type Colors = { [level: Level]: Color };

export const levels: Levels;
export const colors: Colors;
export const MIN_LEVEL: Level;
export const MAX_LEVEL: Level;
export const priorities: Priorities;
