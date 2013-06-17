var producer = require('godot-producer'),
    PublishStream = require('npm-publish-stream');
 
var NpmProducer = module.exports = producer(
  function constructor(options) {

    var self = this;

    this.pubs = [];

    var pub = new PublishStream(options);

    pub.on('data', function (data) {
      self.pubs.push(data.doc);
    });
  },
  function produce() {
    this.values.metric = 1000 * this.pubs.length / this.values.ttl;

    this.emit('data', {
      meta: { publishes: this.pubs }
    });

    this.pubs = [];
  }
);
