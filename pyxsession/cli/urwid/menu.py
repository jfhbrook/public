import urwid
import xdg.Menu
from pyxsession.cli.urwid import on_q, Session


@Session.inject
def menu_session(xdg_menu, session):

    class EntryWidget(urwid.TreeWidget):
        def selectable(self):
            return True

        @session.catch
        def get_display_text(self):
            entry = self.get_node().get_value().DesktopEntry
            name = entry.getName()
            comment = entry.getComment()
            if comment:
                return f'{name} - {comment}'
            else:
                return name

        @session.catch
        def load_inner_widget(self):
            # TODO: Does this need to be a button if we can't actually
            # select it?
            button = urwid.Button(self.get_display_text())
            return button

        @session.catch
        def keypress(self, size, key):
            key = super().keypress(size, key)
            if key == 'enter':
                session.succeed(self.get_node().get_value().DesktopEntry)
            return key


    class EntryNode(urwid.TreeNode):
        @session.catch
        def load_widget(self):
            return EntryWidget(self)


    class MenuWidget(urwid.TreeWidget):
        @session.catch
        def get_display_text(self):
            session = self.get_node().get_value()
            return f'{session.getName()}:'


    class MenuNode(urwid.ParentNode):
        @session.catch
        def load_widget(self):
            return MenuWidget(self)

        @session.catch
        def load_child_keys(self):
            entity = self.get_value()
            if isinstance(entity, xdg.Menu.Menu):
                return list(range(len(list(entity.getEntries()))))
            else:
                return []

        @session.catch
        def load_child_node(self, key):
            child = list(self.get_value().getEntries())[key]
            depth = self.get_depth() + 1
            is_session = isinstance(child, xdg.Menu.Menu)

            cls = MenuNode if is_session else EntryNode

            node = cls(child, parent=self, key=key, depth=depth)

            return node

    session.xdg_menu = xdg_menu
    session.entry_widget_cls = EntryWidget
    session.entry_node_cls = EntryNode
    session.session_widget_cls = MenuWidget
    session.session_node_cls = MenuNode
    session.root = MenuNode(xdg_menu)
    session.list_box = urwid.ListBox(urwid.TreeWalker(session.root))

    session.use(session.list_box)
    session.unhandled_input = on_q

    return session
