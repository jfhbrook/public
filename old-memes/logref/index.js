var EventEmitter = require('events').EventEmitter;

// this module is an implementation of mikeal's proposal for a global
// module logging hook from ~2011, alternately called 'process.logging' and
// logref. for the original email thread, see:
//
//     https://groups.google.com/g/nodejs/c/2NcBM7eXD94/m/jnk5nXkcG5YJ
//
// as well as mikeal's proof-of-concept, on which most of this is based:
//
// https://github.com/mikeal/logref

// this formatter is really similar to the one that's in mikeal's
// implementation but with a bugfix for one of my old projects - I forget the
// details now but I've used this one in practice without too much heartache.
function formatter(msg, ctx) {
  Object.keys(ctx || {}).forEach(function (k) {
    var start = msg.indexOf('%'),
      end = k.length,
      slice = msg.slice(start + 1, start + end + 1);
    if (slice === k) {
      msg = msg.slice(0, start) + ctx[k] + msg.slice(start + k.length + 1);
    }
  });
  return msg;
}

// the main event!
var exports = (module.exports = function logging(name) {
  // mikeal's logging implementation uses util.inherits to subclass
  // EventEmitter, but the only place where these are created is here so
  // I skip the whole thing and make the object I need in-place.
  var logger = new EventEmitter();
  logger.name = name;

  // mikeal's proof-of-concept and a mailing list thread isn't the same thing
  // as a spec, but basically this interface is where the spec - as it were -
  // ends. everything else is up to me.
  function log(msg, ctx) {
    logger.emit('log', msg, ctx || {});
  }

  // save the logger for later
  exports.loggers.push(logger);
  // emit the logger for existing observers
  exports.events.emit('logger', logger);

  return log;
});

exports.formatter = formatter;
exports.events = new EventEmitter();
exports.loggers = [];

// mikeal's logref implementation just dumped to stdout, but this one will
// let you iterate and observe every logger that has been or will be created.
// what you do with that is up to you. in my case, I have an observer that
// cross-posts the logs to a winston logger.
exports.observe = function observe(observer) {
  exports.loggers.forEach(observer);
  exports.events.on('logger', observer);
};

exports.reset = function reset() {
  exports.loggers = [];
  exports.events.removeAllListeners();
};
