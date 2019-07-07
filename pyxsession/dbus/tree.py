class Node:
    # TODO: Give this a pretty representation
    def __init__(self):
        self._branches = {}
    
    def _set_branch(self, name, node):
        setattr(self, name, node)
        self._branches[name] = node

    def __repr__(self):
        return repr(self._branches)


def insert_into_tree(root, path_parts, leaf):
    path_parts = list(path_parts)
    first_part = path_parts.pop(0)
    try:
        last_part = path_parts.pop()
    except IndexError:
        this_node = leaf
    else:
        this_node = Node()
        for path_part in path_parts:
            this_node._set_branch(path_part, Node())
            this_node = getattr(this_node, path_part)
        setattr(this_node, last_part, leaf)

    if type(root) == dict:
        root[first_part] = this_node
    else:
        setattr(root, first_part, this_node)
