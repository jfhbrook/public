declare module 'honeycomb-beeline' {
  interface Fn {
    (...args: any[]): any
  }

  interface Beeline {
    (config: Record<string, unknown>): void
    startSpan: (opts?: Record<string, unknown>) => string
    unmarshalTraceContext(string): any
    finishSpan: (_: string) => void
    startTrace: (opts?: Record<string, unknown>, _?: string, _?: string, _?: string) => string
    finishTrace: (_: string) => void
    bindFunctionToTrace<T extends Fn>(...args: Parameters<T>): ReturnType<T>
    addContext: (opts?: Record<string, unknown>) => void
    addTraceContext: (opts?: Record<string, unknown>) => void
  }

  declare const beeline: Beeline;
  export = beeline;
}
