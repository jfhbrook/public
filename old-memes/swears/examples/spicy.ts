import { test } from 'tap';
import { discuss } from '../';

interface Discourse {
  spiceLevel: number;
}

test('when engaging with the discourse', async (assert) => {
  const topic = discuss<Discourse>(async () => {
    return { spiceLevel: 0 };
  });

  assert.test('and the discourse gets rowdy', async (assert) => {
    const spicierTopic = topic.discuss<Discourse>(async (discourse) => {
      discourse.spiceLevel++;
      return discourse;
    });

    assert.test('things get a little spicy', async (assert) => {
      await spicierTopic.swear(async (discourse) => {
        assert.equal(discourse.spiceLevel, 1);
      });
    });
  });
});
