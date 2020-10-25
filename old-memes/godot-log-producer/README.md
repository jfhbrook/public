# godot-log-producer

This is a [godot producer](https://github.com/nodejitsu/godot#producers) that
emits new lines from tailing a specified logfile.

## Example:

I'm running something similar to this on my VPS to tail nginx logs:

```
var godot = require('godot'),
    logProducer = require('logProducer');

godot.createClient({
  type: 'tcp',
  producers: [
    logProducer({
      host: 'swablu',
      service: 'log/jesusabdullah.net',
      description: 'nginx logs for jesusabdullah.net',
      file: '/var/log/nginx/jesusabdullah.net.log',
      ttl: 10000
    }),
    logProducer({
      host: 'swablu',
      service: 'log/panco-ak.com',
      description: 'nginx logs for panco-ak.com',
      file: '/var/log/nginx/panco-ak.com.log',
      ttl: 10000
    })
  ]
}).connect(1337);
```

I have the server this connects to set up to dump to console with the `console`
reactor, and it looks something like this:

```
josh@swablu:~/dev/swablu-monitor$ node server.js
{ host: 'swablu',
  service: 'log/panco-ak.com',
  state: 'ok',
  time: 1370990811481,
  description: 'nginx logs for panco-ak.com',
  tags: [],
  metric: 1,
  ttl: 10000,
  meta: { logs: [ '24.237.53.237 - - [11/Jun/2013:14:44:12 -0800] "GET /favicon.ico HTTP/1.1" 404 570 "-" "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/28.0.1500.36 Safari/537.36" "-"' ] } }
{ host: 'swablu',
  service: 'log/jesusabdullah.net',
  state: 'ok',
  time: 1370990811482,
  description: 'nginx logs for jesusabdullah.net',
  tags: [],
  metric: 9,
  ttl: 10000,
  meta: 
   { logs: 
      [ '24.237.53.237 - - [11/Jun/2013:14:46:13 -0800] "GET / HTTP/1.1" 304 0 "-" "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/28.0.1500.36 Safari/537.36" "-"',
        '24.237.53.237 - - [11/Jun/2013:14:46:44 -0800] "GET / HTTP/1.1" 200 5235 "-" "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/28.0.1500.36 Safari/537.36" "-"',
        '24.237.53.237 - - [11/Jun/2013:14:46:44 -0800] "GET /css/custom.css HTTP/1.1" 200 176 "http://jesusabdullah.net/" "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/28.0.1500.36 Safari/537.36" "-"',
        '24.237.53.237 - - [11/Jun/2013:14:46:45 -0800] "GET /js/bootstrap.min.js HTTP/1.1" 200 25563 "http://jesusabdullah.net/" "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/28.0.1500.36 Safari/537.36" "-"',
        '24.237.53.237 - - [11/Jun/2013:14:46:45 -0800] "GET /css/bootstrap.min.css HTTP/1.1" 200 98165 "http://jesusabdullah.net/" "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/28.0.1500.36 Safari/537.36" "-"',
        '24.237.53.237 - - [11/Jun/2013:14:46:45 -0800] "GET /img/fire1.gif HTTP/1.1" 200 4972 "http://jesusabdullah.net/" "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/28.0.1500.36 Safari/537.36" "-"',
        '24.237.53.237 - - [11/Jun/2013:14:46:45 -0800] "GET /img/alaska.gif HTTP/1.1" 200 17544 "http://jesusabdullah.net/" "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/28.0.1500.36 Safari/537.36" "-"',  
        '24.237.53.237 - - [11/Jun/2013:14:46:45 -0800] "GET /img/banner.gif HTTP/1.1" 200 100919 "http://jesusabdullah.net/" "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/28.0.1500.36 Safari/537.36" "-"',
        '24.237.53.237 - - [11/Jun/2013:14:46:45 -0800] "GET /img/me.jpg HTTP/1.1" 200 44014 "http://jesusabdullah.net/" "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/28.0.1500.36 Safari/537.36" "-"' ] } }
```

At some point, I will likely investigate writing a reactor that parses nginx
logs. That's a Whole Thing, though, as far as I can tell. If you know of a good
nginx log parser, please let me know. I want it.

## API:

This producer only takes one argument that's not standard for a godot producer,
and that is the `file` argument. This is just a logfile to tail.

## Caveats:

AFAICT, file watching in node is still a bit of a mess. So, I try to be clever
here and use system `tail` when it exists, and
[tailing-stream](github.com/jasontbradshaw/tailing-stream) as a fallback. I
suspect the fallback has promblems even on a system with well-behaving file
watching. YMMV. Would love testing and contributions for those of you on systems
sans-`tail`.

## License:

MIT
