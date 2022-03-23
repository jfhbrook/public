var tap = require('tap');

var logging = require('.');

tap.test('scenarios', function (t) {
  var scenarios = [
    ['%start with', {start: 'starts'}, 'starts with'],
    ['in %the middle', {the: 'the'}, 'in the middle'],
    ['at %end', {end: 'end'}, 'at end'],
    [
      '%has %many %reps',
      {has: 'has', many: 'many', reps: 'reps'},
      'has many reps'
    ],
    ['has no reps', undefined, 'has no reps']
  ];

  t.plan(scenarios.length);

  scenarios.forEach(function (scenario) {
    t.equal(logging.formatter(scenario[0], scenario[1]), scenario[2]);
  });
});

tap.test('observe', function (t) {
  t.plan(6);

  function observer(logger) {
    t.equal(logger.name, 'test');
    logger.on('log', function (msg, ctx) {
      t.equal(msg, 'hello %world');
      t.same(ctx, {world: 'world'});
    });
  }

  // before there are any loggers
  logging.observe(observer);

  var log = logging('test');

  // after there are any loggers
  logging.observe(observer);

  // should get observed twice
  log('hello %world', {world: 'world'});

  logging.reset();
});

tap.test('reset', function (t) {
  t.plan(3);
  var logger = logging('test-logger');

  // expect this to get called once
  logging.observe(function (logger) {
    t.pass('this handler was called');
  });

  t.equal(logging.loggers.length, 1, 'the test logger was added');

  logging.reset();

  t.equal(logging.loggers.length, 0, 'no more loggers');

  // will emit an extra unplanned event
  logging.events.emit('log');

  t.end();
});
