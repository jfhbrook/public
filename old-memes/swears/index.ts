export interface Factory<T> {
  (): Promise<T>
}

export interface Teardown<T> {
  (o: T): Promise<void>
}

export interface Scenario<T, U> {
  (ctx: T): Promise<U>
}

export interface Swear<T> {
  (ctx: T): Promise<void>
}

export class Topic<T> {
  private t: T | null;

  constructor(private factory: Factory<T>, private teardown?: Teardown<T>) {
    this.t = null;
  }

  discuss<U>(scenario: Scenario<T, U>, teardown?: Teardown<U>): Topic<U> {
    return new Topic(async ()  => {
      const t = await this.factory();

      this.t = t;

      return scenario(t);
    }, async (u: U) => {
      if (teardown) {
        await teardown(u);
      }
      if (this.t && this.teardown) {
        await this.teardown(this.t);
      }
    });
  }

  async swear(fn: Swear<T>): Promise<void> {
    const o = await this.factory();

    await fn(o);

    if (this.teardown) {
      await this.teardown(o);
    }
  }
}

export function discuss<T>(fn: Factory<T>) {
  return new Topic<T>(fn);
}
