import crochet
from twisted_ipython.magic import install_autoawait, TwistedMagics


def load_ipython_extension(ipython):
    crochet.setup()

    ipython.register_magics(TwistedMagics)
    install_autoawait(ipython)
