
# twisted_ipython

An [IPython](https://ipython.org/) extension that uses [crochet](https://github.com/itamarst/crochet) to enable running [Twisted](https://twistedmatrix.com/trac/) in IPython and [Jupyter](https://jupyter.org/) notebooks.

## The Problem

Traditionally, the IPython REPL has only truly supported synchronous code. However, IPython [shipped support for running coroutines](https://blog.jupyter.org/ipython-7-0-async-repl-a35ce050f7f7) late last year with support for [asyncio](https://docs.python.org/3/library/asyncio.html), [curio](https://github.com/dabeaz/curio) and [trio](https://github.com/python-trio/trio), which is really cool! Unfortunately, it has some limitations.

In particular, code deemed to be running in an async format is ran by [taking a paused/not-running event loop, running it long enough to execute the async code, and then pausing the loop](https://github.com/ipython/ipython/blob/master/IPython/core/async_helpers.py#L28). This isn't an unreasonable implementation given that IPython was (as far as I know) not originally factored to run async code at all. It does, however, put us in a bind, because if you try to start the Twisted event loop a second time it will [yell at you and refuse](https://github.com/twisted/twisted/blob/8d18e4f83105822a6bad3698eb41ff2f35d56042/src/twisted/internet/error.py#L419). This is because in a typical application an event loop is kept running throughout the lifetime of that process.

## A Partial Solution

[Crochet](https://crochet.readthedocs.io/en/stable/) is a library that runs the Twisted reactor in a thread. This is handy, because our runner implementation ends up being a call to [`ensureDeferred`](https://twistedmatrix.com/documents/current/api/twisted.internet.defer.ensureDeferred.html) wrapped in the [`wait_for`](https://crochet.readthedocs.io/en/stable/api.html#wait-for-blocking-calls-into-twisted) decorator. This means that we can [set up](https://crochet.readthedocs.io/en/stable/api.html#setup) Crochet on extension initialiation, register a small runner to the autoawait magic, and have `%autoawait` support for twisted. In addition, because the loop continues to run in the background, backgrounded tasks will still run once the cell is finished executing. Great!

Loading the module and setting up Twisted autoawait once installed looks like this:


```python
%load_ext twisted_ipython
%autoawait twisted
```

From there we can define a few helpers for our demo:


```python
from twisted.internet import reactor
from twisted.internet.defer import Deferred


# A little helper for demo-ing awaiting and Deferreds
def sleep(t):
    d = Deferred()
    reactor.callLater(t, d.callback, None)
    return d
  
  
# A little helper for demo-ing working display
class Shout:
    def __init__(self, value):
        self.value = value
    def _repr_markdown_(self):
        return f'# {self.value}'
```

and **Check it out: `autoawait` Just Works:**


```python
print('Going to sleep...')

await sleep(1)

Shout('I HAVE AWAKENED!')
```

    Going to sleep...





# I HAVE AWAKENED!



## Running Non-Awaiting Code With `crochet.run_in_reactor`

In addition to being able to run code with `await`ed results in it, it would be nice if we could also safely run Twisted code that interacts with the reactor but *doesn't* use async/await.

Crochet ships with a helper called [`run_in_reactor`](https://crochet.readthedocs.io/en/stable/api.html#run-in-reactor-asynchronous-results) which can decorate wrapper functions so that they can safely interact with the reactor.

I support this with a code magic, ``%%run_in_reactor``. What this magic does is a little scary: It intercepts the python code in the cell as text, detects its indentation level, and generates new python code (as text) that wraps the cell in a decorated function. In addition, it allows for taking the end result of a wrapped block (which must use the `return` keyword unlike regular cells) and making the crochet `EventualResult` object available in the namespace. This makes it possible to interact with eventual results without using async/await.

Using the magic with this feature looks like this:


```python
%%run_in_reactor result

# This runs this non-awaiting code in the correct thread
# and allows access to the returned value via crochet's
# EventualResult

d = sleep(1)

d.addCallback(lambda _: Shout('We did it!'))

return d
```




    <crochet._eventloop.EventualResult at 0x7f7b546b62e8>




```python
# and we can access that result!

result.wait(2)
```




# We did it!



## Install

I'm still working on it, but eventually this will be on pypi, where it can be installed with pip. From there it can be loaded with `%load_ext`.

This library is [available on pypi](https://pypi.org/project/twisted_ipython/) and can be installed into your notebook's environment using [pip](https://pip.pypa.io/en/stable/). For a more concrete example using [Conda](https://docs.conda.io/en/latest/), check out the developer docs below.


# Configuration

As of now, `twisted_ipython` has one configuration option:

* **timeout**: The timeout, in seconds, used for calls to `wait_for` when autoawaiting

You can set the configuration using the `%crochet_config` magic:


```python
%crochet_config show
%crochet_config timeout 5
```

    # Crochet settings:
     - timeout=60
    Setting timeout to 5!



```python
await sleep(10)
```


    ---------------------------------------------------------------------------

    TimeoutError                              Traceback (most recent call last)

    ~/software/jfhbrook/twisted_ipython/twisted_ipython/async_runner.py in twisted_runner(coro)
         16         return ensureDeferred(coro)
         17 
    ---> 18     return run(coro)
    

    ~/anaconda3/envs/twisted_ipython/lib/python3.7/site-packages/wrapt/wrappers.py in __call__(self, *args, **kwargs)
        562 
        563         return self._self_wrapper(self.__wrapped__, self._self_instance,
    --> 564                 args, kwargs)
        565 
        566 class BoundFunctionWrapper(_FunctionWrapperBase):


    ~/anaconda3/envs/twisted_ipython/lib/python3.7/site-packages/crochet/_eventloop.py in wrapper(function, _, args, kwargs)
        508                 eventual_result = run()
        509                 try:
    --> 510                     return eventual_result.wait(timeout)
        511                 except TimeoutError:
        512                     eventual_result.cancel()


    ~/anaconda3/envs/twisted_ipython/lib/python3.7/site-packages/crochet/_eventloop.py in wait(self, timeout)
        237                     "import time.")
        238 
    --> 239         result = self._result(timeout)
        240         if isinstance(result, Failure):
        241             result.raiseException()


    ~/anaconda3/envs/twisted_ipython/lib/python3.7/site-packages/crochet/_eventloop.py in _result(self, timeout)
        199         # have to check manually:
        200         if not self._result_set.is_set():
    --> 201             raise TimeoutError()
        202         self._result_retrieved = True
        203         return self._value


    TimeoutError: 


"Wow that is a heinous traceback!" you're saying to yourself! [It's a known issue](https://github.com/ipython/ipython/issues/9978), and rest assured that it's the correct error just displayed poorly.

# Help / APIs

These help commands work in Jupyter:


```python
%%run_in_reactor??
```

    No Python documentation found for '%autoawait'.
    Use help() to get the interactive help utility.
    Use help(str) for help on the str class.
    


## API documentat

### Additions to the `%autoawait` cell magic

Loading this extension adds the "twisted' runner to the `%autoawait` magic. You can enable twisted support for autoawait by calling `%autoawait twisted`.

### The `%%run_in_reactor` cell magic

Right now, this magic only takes one optional argument, which is the name of a variable to assign the `EventualResult` to. This defaults to `_`.

## Tests

For now, there aren't any tests. However, I plan on using this in practice quite a bit.

## Support

Just to set expectations: I'm just one guy that had an itch to scratch. I'll respond to issues and PRs but I don't expect this project to become a whole thing.

## TODO

* Create a line magic for configuring the timeout used for awaited code (currently set to 60s)
* Set up packaging
* Publish to pypi
* Document how to install and load the extension

## License

Like IPython, this is licensed under a 3-clause BSD license. For more, see `LICENSE.txt`.


