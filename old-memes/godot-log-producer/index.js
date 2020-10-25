var path = require('path'),
    util = require('util');

var producer = require('godot-producer'),
    tail = require('./tail');

var LogProducer = module.exports = producer(
  function constructor(options) {
    var self = this;

    this.logs = [];

    var s = tail(path.resolve(options.file));

    s.on('data', function (lines) {
      lines = lines.toString().split('\n');

      if (lines[lines.length - 1] == '') {
        lines.pop();
      }

      self.logs = self.logs.concat(lines);
    })
  },
  function produce() {
    this.values.metric = 1000 * this.logs.length / this.values.ttl;

    this.emit('data', {
      meta: { logs: this.logs }
    });

    this.logs = [];
  }
);
