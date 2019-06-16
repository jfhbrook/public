

TIMEOUT = 30


def twisted_runner(coro):
    """
    A twisted runner for ipython's autoawait.

    This runner uses crochet and ensureDeferred to run a twisted coroutine in
    a blocking manner, as is required by the ipython API.
    """
    from twisted.internet.defer import ensureDeferred
    from crochet import setup, wait_for
    setup()

    run = wait_for(timeout=TIMEOUT)(ensureDeferred)

    return run(coro)


def install():
    """
    "Install" support for using twisted with the autoawait magic in ipython
    (ie, jupyter).

    This function modifies the current instance of ipython so that:

    * `%autoawait twisted` as a magic should Just Work
    * It should also be enabled by default

    What this means is that you can have cells in jupyter that look like:

        from pyxsession.jupyter.install import install

        install()

    and then:

        await twisted_coroutine()

    and have it do the right thing.
    """
    from IPython import get_ipython
    from IPython.core import async_helpers

    async_helpers._twisted_runner = twisted_runner

    ipython = get_ipython()

    setting = (twisted_runner, True)

    ipython.loop_runner_map['twisted'] = setting
    ipython.loop_runner, ipython.autoawait = setting

