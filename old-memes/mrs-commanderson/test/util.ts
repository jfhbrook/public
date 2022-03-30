import { test } from 'tap';
import { discuss } from '@jfhbrook/swears';
import { Router } from '../router';

type Ctx = {};

function testRoute(path: string) {
  return async () => {
    const router = new Router<Ctx>();
    router.on(path, async () => {});
    return (path: string) => router.dispatch('on', path);
  };
};

test('router/regifyString', async (assert) => {

  assert.test('When using "/home(.*)"', async (assert) => {
    const topic = discuss(testRoute('/home(.*)'));

    assert.test('Should match "/homepage"', async (assert) => {
      await topic.swear(async (dispatch) => {
        assert.ok(await dispatch('/homepage'));
      });
    });

    assert.test('Should match "/home/page"', async (assert) => {
      await topic.swear(async (dispatch) => {
        assert.ok(await dispatch('/home/page'));
      });
    });

    assert.test('Should not match "/foo-bar"', async (assert) => {
      await topic.swear(async (dispatch) => {
        assert.notOk(await dispatch('/foo-bar'));
      });
    });
  });

  assert.test('When using "/home.*"', async (assert) => {
    const topic = discuss(testRoute('/home.*'));

    assert.test('Should match "/homepage"', async (assert) => {
      await topic.swear(async (dispatch) => {
        assert.ok(await dispatch('/homepage'));
      });
    });

    assert.test('Should match "/home/page"', async (assert) => {
      await topic.swear(async (dispatch) => {
        assert.ok(await dispatch('/home/page'));
      });
    });

    assert.test('Should not match "/foo-bar"', async (assert) => {
      await topic.swear(async (dispatch) => {
        assert.notOk(await dispatch('/foo-bar'));
      });
    });
  });

  assert.test('When using "/home(page[0-9])*"', async (assert) => {
    const topic = discuss(testRoute('/home(page[0-9])*'));

    assert.test('Should match "/home"', async (assert) => {
      await topic.swear(async (dispatch) => {
        assert.ok(await dispatch('/home'));
      });
    });

    assert.test('Should match "/homepage0", "/homepage1", etc.', async (assert) => {
      await topic.swear(async (dispatch) => {
        for (let i = 0; i < 10; i++) {
          assert.ok(await dispatch('/homepage' + i));
        }
      });
    });

    assert.test('Should not match "/home_page"', async (assert) => {
      await topic.swear(async (dispatch) => {
        assert.notOk(await dispatch('/home_page'));
      });
    });

    assert.test('Should not match "/home/page"', async (assert) => {
      await topic.swear(async (dispatch) => {
        assert.notOk(await dispatch('/home/page'));
      });
    });
  });

  assert.test('When using "/home*"', async (assert) => {
    const topic = discuss(testRoute('/home*'));

    assert.test('Should match "/homepage"', async (assert) => {
      await topic.swear(async (dispatch) => {
        assert.ok(await dispatch('/homepage'));
      });
    });

    assert.test('Should match "/home_page"', async (assert) => {
      await topic.swear(async (dispatch) => {
        assert.ok(await dispatch('/home_page'));
      });
    });

    assert.test('Should match "/home-page"', async (assert) => {
      await topic.swear(async (dispatch) => {
        assert.ok(await dispatch('/home-page'));
      });
    });

    assert.test('Should not match "/home/page"', async (assert) => {
      await topic.swear(async (dispatch) => {
        assert.ok(await dispatch('/home/page'));
      });
    });
  });

  assert.test('When using "/folder/::home"', async (assert) => {
    const topic = discuss(testRoute('/folder/::home'));

    assert.test('Should match "/folder/:home"', async (assert) => {
      await topic.swear(async (dispatch) => {
        assert.ok(await dispatch('/folder/:home'));
      });
    });

    assert.test('Should not match "/folder/::home"', async (assert) => {
      await topic.swear(async (dispatch) => {
        assert.notOk(await dispatch('/folder/::home'));
      });
    });

    assert.test('Should not match "/folder/abc" (the catchall regexp)"', async (assert) => {
      await topic.swear(async (dispatch) => {
        assert.notOk(await dispatch('/folder/abc'));
      });
    });
  });
});
