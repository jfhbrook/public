process.logging = require('@jfhbrook/logref');

var tap = require('tap');

var loggins = require('../');

function testObserve(level) {
  return function test(t) {
    process.logging.reset();
    process.logging.loggers = [];
    process.logging.events.removeAllListeners();

    var logger = {
      log: function (event) {
        t.same(event, {
          level: level || 'debug',
          message: 'hello world',
          logging: {
            name: 'my-cool-log'
          }
        });
        t.end();
      }
    };

    loggins.observe(logger, level);

    var log = process.logging('my-cool-log');

    log('hello world');
  };
}

tap.test('observe, default level', testObserve());
tap.test('observe, configured level', testObserve('warn'));
