var godot = require('godot'),
    npmPublishProducer = require('./index');

godot.createClient({
  type: 'tcp',
  producers: [
    npmPublishProducer({
      service: 'npm/publish/stream',
      description: 'npm publish events',
      startTime: (function () {
        var ago = new Date;
        ago.setHours(ago.getHours() - 12);
     
        return ago;
      })(),
      ttl: 5000
    })
  ]
}).connect(1337);
