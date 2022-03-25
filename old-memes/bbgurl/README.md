# bbgurl

a command line http client built on top of [undici](https://npm.im/undici).

## install

bbgurl is distributed on npm. you can install it with `npm i -g bbgurl`, or
use it with npx:

```bash
npx bbgurl https://google.com
```

## examples

### hit an endpoint

```
$ bbgurl https://google.com
[♥] Downloading: ======================================== 100% (220/220)
<HTML><HEAD><meta http-equiv="content-type" content="text/html;charset=utf-8">
<TITLE>301 Moved</TITLE></HEAD><BODY>
<H1>301 Moved</H1>
The document has moved
<A HREF="https://www.google.com/">here</A>.
</BODY></HTML>
```

### set some headers

(this example does *not* work and will be updated as soon as I write tests.
the api is still like this though!)

```
$ bbgurl http://whatismyip.jit.su -H '{ "accept": "application/json" }'
{ "ip": "71.198.76.200" }
```

### do some basic auth

(this example also needs to be updated, but the functionality hasn't changed
here at all so it should work!)

```
$ bbgurl -u josh:supersekritpw http://localhost:8080
{ "success": true, "message": "Welcome to the inner sanctum." }
```

### download a tarball

(yes, this ancient url still works!! this is an up-to-date example!)

```
$ bbgurl --verbose http://nodejs.org/dist/v0.8.4/node-v0.8.4.tar.gz -o node-v0.8.4.tar.gz 
[♥] data written to /home/josh/joshiverse/old-memes/bbgurl/node-v0.8.4.tar.gz
```

## usage

here's the current output of the help, which I think is uncharacteristically
comprehensive:

```
[♥] bbgurl: a cli http client using undici
[♥] 
[♥] USAGE: bbgurl [URL]
[♥] 
[♥] make an HTTP request using undici.request.
[♥] 
[♥] most undici options are bled straight through the args, using conventions
[♥] from the optimist and minimist libraries.
[♥] 
[♥] for more information on undici, see: https://npm.im/undici
[♥] 
[♥] OPTIONS:
[♥]     --help                   print this message.
[♥] 
[♥]     -Q/--quiet               suppress logging.
[♥] 
[♥]     -X/--method METHOD       an http method. defaults to GET.
[♥] 
[♥]     --body BODY              the request body. if the first character is a @,
[♥]                              will read from file. defaults to stdin.
[♥] 
[♥]     --headers HEADERS        a JSON blob representing an undici headers
[♥]                              argument. defaults to null.
[♥] 
[♥]     --upgrade UPGRADE        optionally upgrade the request with the specified
[♥]                              upgrade type.
[♥] 
[♥]     --bodyTimeout MILLIS     how long to wait for the body before timing out.
[♥]                              defaults to 30 seconds.
[♥] 
[♥]     --headersTimeout MILLIS  how long to wait for the headers before timing
[♥]                              out. defaults to 30 seconds.
[♥] 
[♥]     --maxRedirections N      the maximum number of redirects to follow.
[♥] 
[♥]     --mixin MIXIN            if specified, call the appropriate fetch mixin on the body.
[♥] 
[♥]     -i/--include             include response status, headers and trailers.
[♥] 
[♥]     --logfile FILE           an optional file to write logs to.
[♥] 
[♥]     -o/--output FILE         a file to write the response to. defaults to stdout.
[♥] 
[♥]     -U/--user CREDENTIALS    specify basic auth credentials. ex: '-u user:pass'
[♥] 
```



## what happened to the request wrapper?

a previous version of this client was written as a thin wrapper around
[mikeal/request](https://github.com/mikeal/request); however, request is
no longer maintained, and I saw no reason not to upgrade.

## license

MIT/X11.
