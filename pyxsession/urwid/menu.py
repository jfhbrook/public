import urwid
import xdg.Menu
from pyxsession.executor import default_executor


class XDGMenu:
    def __init__(menu, xdg_menu):
        menu.xdg_menu = xdg_menu
        menu.selected = None

        class EntryWidget(urwid.TreeWidget):
            def selectable(self):
                return True

            def get_display_text(self):
                entry = self.get_node().get_value().DesktopEntry
                name = entry.getName()
                comment = entry.getComment()
                if comment:
                    return f'{name} - {comment}'
                else:
                    return name

            def load_inner_widget(self):
                # TODO: Does this need to be a button if we can't actually
                # select it?
                button = urwid.Button(self.get_display_text())
                return button

            def keypress(self, size, key):
                key = super().keypress(size, key)
                if key == 'enter':
                    menu.run(self.get_node().get_value().DesktopEntry)
                    raise urwid.ExitMainLoop()
                return key


        class EntryNode(urwid.TreeNode):
            def load_widget(self):
                return EntryWidget(self)


        class MenuWidget(urwid.TreeWidget):
            def get_display_text(self):
                menu = self.get_node().get_value()
                return f'{menu.getName()}:'


        class MenuNode(urwid.ParentNode):
            def load_widget(self):
                return MenuWidget(self)

            def load_child_keys(self):
                entity = self.get_value()
                if isinstance(entity, xdg.Menu.Menu):
                    return list(range(len(list(entity.getEntries()))))
                else:
                    return []

            def load_child_node(self, key):
                child = list(self.get_value().getEntries())[key]
                depth = self.get_depth() + 1
                is_menu = isinstance(child, xdg.Menu.Menu)

                cls = MenuNode if is_menu else EntryNode

                node = cls(child, parent=self, key=key, depth=depth)

                return node

        menu.entry_widget_cls = EntryWidget
        menu.entry_node_cls = EntryNode
        menu.menu_widget_cls = MenuWidget
        menu.menu_node_cls = MenuNode

        menu.root = MenuNode(xdg_menu)

        menu.list_box = urwid.ListBox(urwid.TreeWalker(menu.root))

        menu.view = menu.list_box

    def run(self, entry):
        default_executor.run_xdg_desktop_entry(entry)
