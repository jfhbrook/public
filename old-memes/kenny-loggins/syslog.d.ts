import { Level } from './core';

export type SyslogLevel = number;

export function toSyslog(level: Level) -> SyslogLevel;
export function fromSyslog(n: SyslogLevel) -> Level;
