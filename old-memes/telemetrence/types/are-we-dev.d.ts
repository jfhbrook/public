declare module 'are-we-dev' {
  interface IsDev {
    (): boolean
  }

  declare const isDev: IsDev;
  export = isDev;
}
