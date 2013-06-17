var tap = require('tap'),
    producer = require('./index');

var Expression, expression;

tap.test('create a producer', function (t) {
  t.doesNotThrow(function () {
    TestProducer = producer(
      function ctor(options) {
        this.happy = options.happy;
        this.disappoint = 'ಠ_ಠ';
      },
      function produce() {
        this.emit('data', { meta: {
          happy: this.happy,
          disappoint: this.disappoint
        }});
      }
    );
  }, 'create a producer constructor');

  t.doesNotThrow(function () {
    producer = new TestProducer({
      happy: '^__^',
      ttl: 1000
    });
  }, 'create a producer instance');

  t.equal(producer.happy, '^__^', 'producer.happy is ^__^');
  t.equal(producer.disappoint, 'ಠ_ಠ', 'producer.disappoint is ಠ_ಠ');

  t.end();
});

tap.test('receive events', function (t) {
  var time;

  producer.once('data', function (data) {

    t.ok(true, 'producer fired once');

    time = new Date;
    t.type(data.meta, 'object', 'data.meta is an object');
    t.equal(data.meta.happy, '^__^', 'data.meta.happy is ^__^');
    t.equal(data.meta.disappoint, 'ಠ_ಠ', 'data.meta.disappoint is ಠ_ಠ');
    t.type(data.host, 'string', 'data.host is a string');
    t.equal(data.state, 'ok', 'data.state is ok');
    t.type(data.description, 'string', 'data.description is a string');
    t.type(data.tags, Array, 'data.tags is an array');
    t.equal(data.ttl, 1000, 'data.ttl is 1000');

    producer.once('data', function (data) {

      t.ok(true, 'producer fired twice');

      var dT = Date.now() - time,
          inaccuracy = dT - 1000;

      t.ok(inaccuracy < 50, 'time interval is vaguely 1000', {
        found: '~1000', wanted: dT
      });
      t.end();
    });
  });
});

tap.test('clear producer interval', function (t) {
  clearInterval(producer.ttlId);

  t.end();
});

