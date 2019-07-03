from functools import wraps
import urwid


def on_q(run):
    @wraps(run)
    def run_on_q(key):
        if key in {'q', 'Q'}:
            run()
