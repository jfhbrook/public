# @jfhbrook/logref

## an implementation of the process.logging pseudo-specification

## huh?

in late 2011, [@mikeal](https://twitter.com/mikeal)
[posted a thread on the node.js mailing list](https://groups.google.com/g/nodejs/c/2NcBM7eXD94/m/jnk5nXkcG5YJ)
where he said:

> I've spent some time rethinking logging.
>
> Logging is strange problem. It needs to be instrumented, to some degree, in all the modules we use, not just in our application code.
>
> For debugging and increased visibility in to production you just want to be notified of the internal workings.
>
> The traditional log4j approach is kind of ridiculous to instrument as a module developer, you don't really have a need for log levels for instance.
>
> Logging is also one of the very few cases that we need a truly process global module that is not in core.
>
> So, i started to think about what the most minimal API for such a logger might bem.
>
> I created an implementation and a draft spec. The idea here is that we define a minimal logger that different people can implement so long as they obey this minimal API contract. Then in my own modules, like request, I'm going to check for `process.logging` and if it's there I'll get myself a log function and use it accordingly.
>
> I'm open to suggestions about the API but keep in mind that the last of features is it's greatest feature. Anything that can be built on top of this API without any breaking changes should not be in the spec portion.
>
> [https://github.com/mikeal/logging](https://github.com/mikeal/logref)
>
> I'm sure there are typos and misspellings, it's quite late and i'm beat. I'll be using this in request starting tomorrow.
>
> -Mikeal

(note that the github repo got moved to mikeal/logref - the link has been
updated.)

as far as I know this never took off and the only module I've seen implement it
outside my own is the now-deprecated [request](https://npm.im/request)
library. but the core insight here is a really good and important one.

as a module author, I want to expose simple logging for debug use cases.
however, as a module author it's also difficult to bring opinions to the
table and nobody wants to ship a whole logger with their module.

on the flip side: as an app writer, I want to be able to log stuff that's
happening inside the modules I'm using, but I want _control_ over what happens
to those logs. in my case, I want to send them to winston, which is ironically
exactly the kind of "traditional log4j approach" mikeal railed against then.

what you really want, then, is a standard - and very lightweight - way to
send logging events from your module to a small logger, and for your app to
declare how these sorts of logs should be handled app-wide. a spicy take,
perhaps, bit mikeal in 2011 was right that this calls for a global.

this post has haunted me in the meantime. just about every project I used
that had request in it was using this hook in one way or another, and it was
one of the few special features I supported when I wrote my own logger around
the same time.

today, I don't really care what other people are using, but I know that I have
this problem in my apps today, and this fits the bill. I'll be adding
process.logging support to my libraries over time and using this to intercept
them in my apps.

## api

mikeal's spec is a little fuzzy. some things are specified that don't quite
have to be and some things aren't specified when the whole thing won't really
work without them. having worked with the original logref off and on for a
_while_, this is where I've arrived when it comes to de facto use.

### api for module authors

inside your module, check to see if `process.logging` is defined, and if
it's defined use it to create a logger for your module:

```js
var log = process.logging ? process.logging('my-cool-module') : function () {};
```

from here, you can call the logging function like so:

```js
log('hello %user', {user: 'world'});
```

process.logging specifies this particular templating language, which I haven't
seen anywhere other than the logref reference implementation. I think this is a
big part of why process.logging failed to catch on with developers - but you
have to start somewhere, and there _is_ a reference implementation.

### api for application authors

on the very first line of your app, define process.logging by importing your
implementation:

```js
process.logging = require('@jfhbrook/logref');
```

the logging framework beyond the API described for module authors is not part
of the logref spec; however certain aspects of that design are tough to
replace given the requirements, and so the structure and events are very
similar.

one major difference, however, is that instead of calling `.stdout()` and
similar to get the logger output, we have `logging.observe` which can be
used to add hooks on every process.logging logger like so:

```js
process.logging.observe(function (logger) {
  // a baby logref logger!
  logger.on('log', function (msg, ctx) {
    console.log(process.logging.format(msg, ctx));
  });
});
```

loggers are simple EventEmitter instances with the additional property of
`logger.name` - as in mikeal's implementation - and similarly use the 'log'
event to emit logs. however, mikeal's implementation also applies formatting to
those messages and re-emits them on a 'msg' event - we don't do that here.

### api for testing

there's a secret method `process.logging.reset()` which will drop all
registered loggers on the floor. this is mostly only useful if you're doing
tests which involve process.logging state.

## formatting, linting, tests, oh my!

I'm using my custom prettier config to do formatting, which you can run
with `npm run format`. I don't have linting working yet. tests are written
in `tap` and may be run with `npm test`. the tests are simple, but so is the
module.

## license

mikeal didn't put a license on the original logref, which I leaned on heavily,
but for what I did here I gave it an MIT license and called it a day.
