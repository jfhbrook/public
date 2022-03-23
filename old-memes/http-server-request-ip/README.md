# http-server-request-ip

## example

```js
var getIP = require('@jfhbrook/http-server-request-ip');

var server = http.createServer(function (req, res) {
    res.end('Request IP address is: ' + getIP(req));
});

server.listen(8000);
```
