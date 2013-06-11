var path = require('path'),
    util = require('util');

var Producer = require('godot').producer.Producer,
    tail = require('./tail');

var LogProducer = module.exports = function (options) {
  if (!(this instanceof LogProducer)) {
    return new LogProducer(options);
  }

  var self = this;

  Producer.call(this, options);

  this.logs = [];

  var s = tail(path.resolve(options.file));

  s.on('data', function (lines) {
    lines = lines.toString().split('\n');

    if (lines[lines.length - 1] == '') {
      lines.pop();
    }

    self.logs = self.logs.concat(lines);
  })
};
util.inherits(LogProducer, Producer);

LogProducer.prototype.produce = function () {

  this.values.metric = this.logs.length;

  this.emit('data', {
    host:        this.values.host,
    service:     this.values.service,
    state:       this.values.state,
    time:        Date.now(),
    description: this.values.description,
    tags:        this.values.tags,
    metric:      this.values.metric,
    ttl:         this.values.ttl,
    meta:        { logs: this.logs }
  });

  this.logs = [];
};
