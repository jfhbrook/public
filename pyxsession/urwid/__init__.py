import urwid


def quit_on_q(key):
    if key in {'q', 'Q'}:
        raise urwid.ExitMainLoop()
