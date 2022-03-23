import { EventEmitter } from 'events';

export type Logger = (msg: string, ctx?: Object) => void;
export type Formatter = (msg: string, ctx?: Object) => string;
export type Observer = (log: Logger) => void;

interface LogRef {
  (name: string): Logger;
  formatter: Formatter;
  events: EventEmitter;
  loggers: Logger[];
  observe(observer: Observer): void;
  reset(): void; 
}
