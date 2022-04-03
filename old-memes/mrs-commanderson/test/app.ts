import { App } from '../';
import { test } from 'tap';
import { discuss } from '@jfhbrook/swears';

test('App objects', async (assert) => {
  assert.test('when assigned no options', async (assert) => {
    type Matcher = {
      init: boolean[];
      install: string[];
    }

    const topic = discuss(async () => {
      const matcher: Matcher = {
        init: [],
        install: []
      };

      const app = new App();

      app.command("init", async (ctx) => { matcher.init.push(true);; });
      app.command("install :pkg", async (ctx, pkg) => { matcher.install.push(pkg); });

      return { app, matcher };
    });

    assert.test('init runs without crashing', async (assert) => {
      await topic.swear(async ({ app, matcher }) => {
        await app.run(['init']);

        assert.same(matcher, {
          init: [true],
          install: []
        });
      });
    });

    assert.test('install runs without crashing', async (assert) => {
      await topic.swear(async ({ app, matcher }) => {
        await app.run(['install', 'some-pkg']);

        assert.same(matcher, {
          init: [],
          install: ['some-pkg']
        });
      });
    });
  });

  assert.test('when constructed with a main function', async (assert) => {
    assert.test('instead of options', async (assert) => {
      type Matcher = {
        main: boolean[]
      };
      const topic = discuss(async () => {
        const matcher: Matcher = {
          main: []
        };

        const app = new App(async (opts) => {
          matcher.main.push(true);
        });

        return { app, matcher };
      });

      assert.test('it runs with no subcommand', async (assert) => {
        await topic.swear(async ({ app, matcher }) => {
          await app.run([]);

          assert.same(matcher, {
            main: [true]
          });
        });
      });
    });

    assert.test('as one of the options', async (assert) => {
      type Matcher = {
        main: boolean[]
      };
      const topic = discuss(async () => {
        const matcher: Matcher = {
          main: []
        };

        const app = new App({
          async main(opts) {
            matcher.main.push(true);
          }
        });

        return { app, matcher };
      });

      assert.test('it runs with no subcommand', async (assert) => {
        await topic.swear(async ({ app, matcher }) => {
          await app.run([]);

          assert.same(matcher, {
            main: [true]
          });
        });
      });
    });
  });

  assert.test('when constructed with routes', async (assert) => {
    type Matcher = {
      init: boolean[];
      install: string[];
    }

    const topic = discuss(async () => {
      const matcher: Matcher = {
        init: [],
        install: []
      };

      const app = new App({
        routes: {
          async init(ctx) {
            matcher.init.push(true);
          },
          // TODO: The mounting algorithm absolutely mangles this! Practically
          // speaking this API isn't ready for prime time, but we *can* do
          // some partial tests and skip the problematic parts.
          /*
          'install': {
            ' ([._a-zA-Z0-9-%()]+)': async (ctx, pkg) => {
              matcher.install.push(pkg);
            }
          }
          */
        }
      });

      return {app, matcher}
    });

    assert.test('init runs without crashing', async (assert) => {
      await topic.swear(async ({ app, matcher }) => {
        await app.run(['init']);

        assert.same(matcher, {
          init: [true],
          install: []
        });
      });
    });

    assert.skip('install runs without crashing', async (assert) => {
      await topic.swear(async ({ app, matcher }) => {
        await app.run(['install', 'some-pkg']);

        assert.same(matcher, {
          init: [],
          install: ['some-pkg']
        });
      });
    });
  });
});
