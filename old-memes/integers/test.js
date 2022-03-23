var integers = require('./index'),
    tap = require('tap'),
    util = require('util');

tap.test('integers(5)', async (t) => {
  t.same(integers(5), [0, 1, 2, 3, 4]);
});

tap.test('integers(1, 5)', async (t) => {
  t.same(integers(1, 5), [1, 2, 3, 4]);
});

tap.test('integers(1, 5, 2)', async (t) => {
  t.same(integers(1, 5, 2), [1, 3]);
});
