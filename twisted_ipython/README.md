
# twisted_ipython

An [IPython](https://ipython.org/) extension that uses [crochet](https://github.com/itamarst/crochet) to enable running [Twisted](https://twistedmatrix.com/trac/) in IPython and [Jupyter](https://jupyter.org/) notebooks.

## The Short Short Version

Install this package into your Jupyter notebook's kernel. Then, load the extension:

    %load_ext twisted_ipython

and then turn on autoawait for Twisted:

    %autoawait twisted

and with a helper for the demo

```python
from twisted.internet import reactor
from twisted.internet.defer import Deferred


def sleep(t):
    d = Deferred()
    reactor.callLater(t, d.callback, None)
    return d
```

we can now use async/await in cells like so:

```python
print('Going to sleep...')

await sleep(1)

print('I HAVE AWAKENED!')
```

## I Want To Know More!

Check out the much more complete [README.ipynb](https://github.com/jfhbrook/twisted_ipython/blob/master/README.ipynb)!
