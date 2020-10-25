var util = require('util');

var Producer = require('./vendor/producer'),
    merge = require('xtend');

module.exports = function producer(ctor, produce) {
  var CustomProducer = function (options) {
    if (!(this instanceof CustomProducer)) {
      return new CustomProducer(options);
    }

    if (ctor) {
      ctor.call(this, options);
    }

    Producer.call(this, options);
  };
  util.inherits(CustomProducer, Producer);

  CustomProducer.prototype._emit = CustomProducer.prototype.emit;
  CustomProducer.prototype.emit = function (ev, data) {
    //
    // On data events, merge on top of defaults
    //
    this._emit(ev, ev === 'data'
      ? merge({
          host:        this.values.host,
          service:     this.values.service,
          state:       this.values.state,
          time:        Date.now(),
          description: this.values.description,
          tags:        this.values.tags,
          metric:      this.values.metric,
          ttl:         this.values.ttl
        }, data || {})
      : data
    );
  };

  if (produce) {
    CustomProducer.prototype.produce = produce;
  }

  return CustomProducer;
};
