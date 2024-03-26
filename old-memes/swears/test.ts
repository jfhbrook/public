import { test } from 'tap';
import { discuss } from '.';

interface A {
  a: true;
}

interface B extends A {
  b: true
}

test('a boring ol topic', async (assert) => {
  const topic = discuss<A>(async () => {
    return { a: true };
  }, async () => {});

  assert.test('can execute swears', async (assert) => {
    await topic.swear(async (a: A) => {
      assert.ok(a.a);
      assert.notOk((a as any).b);
    });
  });

  assert.test('can execute child swears', async (assert) => {
    const spicierTopic = topic.discuss<B>(async (a: A) => {
      // Doing a side effect to test that we create a new instance
      // every swear
      const ctx: B = <any>a;
      ctx.b = true;

      return ctx;
    });

    await spicierTopic.swear(async (b: B) => {
      assert.ok(b.a);
      assert.ok(b.b);
    });

    assert.test("executing child swears doesn't mutate the parent", async (assert) => {
      await topic.swear(async (a: A) => {
        assert.ok(a.a);
        assert.notOk((a as any).b);
      });
    });
  });
});
