# http-server-request-accept

## example

```js
var getAccept = require('@jfhbrook/http-server-request-accept');

var server = http.createServer(function (req, res) {
    res.end('Request accepted content types are: ' + getAccept(req));
});

server.listen(8000);
```

## license

MIT!
