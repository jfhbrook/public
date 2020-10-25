# clf-parser

A little parser for getting useful stuff out of apache/nginx-style "common log
format" log lines.

## Example

```
josh@onix:/tmp/clf-parser$ node
> var parse = require('./index');
> parse('127.0.0.1 - frank [10/Oct/2000:13:55:36 -0700] "GET /apache_pb.gif HTTP/1.0" 200 2326');
{ remote_addr: '127.0.0.1',
  remote_user: 'frank',
  time_local: Mon Oct 09 2000 22:55:36 GMT-0800 (AKDT),
  request: 'GET /apache_pb.gif HTTP/1.0',
  status: 200,
  body_bytes_sent: 2326 }
> 
```

You get the idea.

## License

WTFPL
