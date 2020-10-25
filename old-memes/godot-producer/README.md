# godot-producer

This is a library for creating third-party
[godot producers](https://github.com/nodejitsu/godot#producers) without too
much rigamarole. It vendors the 'producer' library to keep the dependency tree
down.

## Example:

[Here's a library I wrote that uses this.](https://github.com/jesusabdullah/godot-log-producer/blob/master/index.js)

## API:

```
var ProducerStream = godotProducer(ctor, produce);
```

`ctor` is called inside the returned constructor with `this` being contextualized
as your instantiated producer. `produce` is called when the "produce" method is
called. Emit is monkey punched so that default production values are added
automatically. ProducerStream has the added bonus of the ol'
"if (!(this instanceof ProducerStream))" trick so you don't have to call it with
the 'new' keyword (unless you want to).

## License:

MIT
