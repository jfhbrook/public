# godot-npm-publish-producer

This is a [godot producer](https://github.com/nodejitsu/godot#producers) that
wraps [npm-publish-stream](https://github.com/rvagg/node-npm-publish-stream).

## Example:

```
var godot = require('godot'),
    NpmPublishProducer = require('./index');

godot.createClient({
  type: 'tcp',
  producers: [
    new NpmPublishProducer({
      service: 'npm/publish/stream',
      description: 'npm publish events',
      ttl: 5000
    })
  ]
}).connect(1337);
```

## API:

### NpmPublishProducer(options)

Returns a producer. Options are passed to both godot and npm-publish stream.

Using npm-publish-stream's "startTime" is not recommended, since there is
currently not a good way to detect when the stream has "caught-up" with
real-time, meaning that the metric, which is publishes per second, will be
wildly inaccurate.

## License:

MIT
