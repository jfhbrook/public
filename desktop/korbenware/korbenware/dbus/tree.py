# Copyright 2020 Josh Holbrook
#
# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at https://mozilla.org/MPL/2.0/.


class InsertionError(Exception):
    pass


class Node:
    def __init__(self, branches=None):
        self.__attrs_post_init__()
        if branches:
            for path, node in branches.items():
                self.set(path, node)

    def __attrs_post_init__(self):
        self._branches = {}
        self._branches["/"] = self

    def set(self, name, node):
        if type(name) == str:
            path_parts = [part for part in name.split("/") if part]
        else:
            path_parts = list(name)

        if len(path_parts) == 0:
            raise InsertionError(f"Can't insert an empty path!")

        # Insert node into correct position of the tree
        ancestors = [(None, None, self)]
        this = self
        while len(path_parts) > 1:
            slug = path_parts.pop(0)

            parent_full_path, parent_slug, parent = ancestors[-1]
            parent_path = f"/{parent_slug}/{slug}" if parent_slug else f"/{slug}"
            full_path = f"{parent_path}/{slug}" if parent_full_path else f"/{slug}"

            if parent.has(full_path):
                this = parent.get(full_path)
            else:
                # Create a fresh node if necessary to complete the path
                this = Node()

                # Set the property on the parent. TODO: It would be more elegant
                # to set this on the traversal back up at the same place where
                # we set the key in _branches, but this also passes tests and
                # this code is really hairy to begin with
                setattr(parent, slug, this)
            ancestors.append((full_path, slug, this))

        # Retain existing nodes in the tree
        if this.has(f"/{path_parts[0]}"):
            for p, o in this.get(f"/{path_parts[0]}").items():
                node.set(p, o)

        # set last bit
        setattr(this, path_parts[0], node)
        this._branches[f"/{path_parts[0]}"] = node

        # Add inherited branches going upwards on the tree
        this_slug = path_parts[0]
        this = node

        if isinstance(node, Node):
            branches = list(this._branches.keys())
        else:
            branches = []

        while ancestors:
            _, parent_slug, parent = ancestors.pop()
            parent_branches = []

            for child_path in branches:
                # Suppose we have a structure root -> a -> b
                # and we're on node "a"
                # then these branches are "/" (self) and "/b" (node b)
                # this slug is "a"
                # the parent slug is None
                # and the parent itself is the root
                child = this._branches[child_path]

                if child_path == "/":
                    # for branch "/", we want to set the parent branch to "/a"
                    parent_branch = f"/{this_slug}"
                else:
                    # and for branch "/b", we want to set the parent branch to "/a/b"
                    parent_branch = f"/{this_slug}{child_path}"

                # Set the parent branch
                parent._branches[parent_branch] = child

            branches = list(parent._branches.keys())
            this_slug = parent_slug
            this = parent

    def get(self, name):
        return self._branches[name]

    def has(self, name):
        return name in self._branches

    def items(self):
        for k, v in self._branches.items():
            if k != "/":
                yield k, v

    def keys(self):
        for k in self._branches.keys():
            if k != "/":
                yield k

    def values(self):
        for k, v in self._branches.items():
            if k != "/":
                yield v

    def __repr__(self):
        keys = list(self.keys())
        keys.sort()
        return f"{self.__class__.__name__}({keys})"
