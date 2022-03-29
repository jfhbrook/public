export interface Factory<T> {
  (): Promise<T>
}

export interface Scenario<T, U> {
  (ctx: T): Promise<U>
}

export interface Swear<T> {
  (ctx: T): Promise<void>
}

export class Topic<T> {
  constructor(private factory: Factory<T>) {
  }

  async discuss<U>(fn: Scenario<T, U>): Promise<Topic<U>> {
    return new Topic(async ()  => {
      return fn(await this.factory());
    });
  }

  async swear(fn: Swear<T>): Promise<void> {
    await fn(await this.factory());
  }
}

export function discuss<T>(fn: Factory<T>) {
  return new Topic<T>(fn);
}
