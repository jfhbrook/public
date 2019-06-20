import atexit
import crochet
from twisted.internet import reactor
from twisted_ipython.magic import install_autoawait, TwistedMagics

@crochet.run_in_reactor
def _shutdown():
    reactor.stop()

def load_ipython_extension(ipython):
    crochet.setup()

    ipython.register_magics(TwistedMagics)
    install_autoawait(ipython)
    atexit.register(_shutdown)
