declare module '@entropic/bole' {
  interface Bole {
    (name: string): Bole;
    output(...config: any[]): void;
    info(...args: any[]): void;
    debug(...args: any[]): void;
    error(...args: any[]): void;
    warn(...args: any[]): void;
  }

  declare const bole: Bole;
  export = bole;
}

