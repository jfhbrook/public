import pytest

import attr

from korbenware.dbus.tree import Node


def test_simple_set():
    root = Node()

    a = Node()

    root.set("/a", a)

    assert root.a is a
    assert root.get("/a") is a


def test_parallel_set():
    root = Node()

    a = Node()
    b = Node()

    root.set("/a", a)
    root.set("/b", b)

    assert root.a is a
    assert root.get("/a") is a

    assert root.b is b
    assert root.get("/b") is b


def test_child_set():
    root = Node()

    a = Node()
    b = Node()

    root.set("/a", a)
    root.set("/a/b", b)

    assert root.a is a
    assert root.get("/a") is a
    assert root.a.b is b
    assert root.get("/a/b") is b
    assert root.a.get("/b") is b


def test_sparse_set():
    root = Node()

    c = Node()

    root.set("/a/b/c", c)

    assert root.a.b.c is c

    assert root.get("/a").b.c is c
    assert root.get("/a/b").c is c

    assert root.a.get("/b").c is c
    assert root.a.get("/b/c") is c

    assert root.a.b.get("/c") is c


def test_replaced_node():
    root = Node()

    a = Node()
    b = Node()
    c = Node()
    b_prime = Node()

    root.set("/a", a)
    root.a.set("/b", b)
    root.a.b.set("/c", c)

    root.set("/a/b", b_prime)

    assert root.a is a
    assert root.get("/a") is a
    assert root.a.b is b_prime
    assert root.a.get("/b") is b_prime
    assert root.get("/a/b") is b_prime
    assert root.a.b.c is c
    assert root.a.b.get("/c") is c
    assert root.a.get("/b/c") is c
    assert root.get("/a/b/c") is c


def test_inherited_node():
    root = Node()

    c = Node()
    d = Node({"/e": Node()})

    root.set("/a/b/c", c)
    root.set("/a/b/c/d", d)

    assert root.a.b.c.d.has("/e")


class NonNode:
    pass


def test_insert_non_node():
    root = Node()

    b = NonNode()

    root.set("/a/b", b)

    assert root.a.b is b
    assert root.get("/a/b") is b


@attr.s
class AttrNode(Node):
    _branches = attr.ib(type=dict, default=attr.Factory(dict))


def test_insert_attr_node():
    root = AttrNode()

    b = AttrNode()

    root.set('/a/b', b)

    assert root.get('/') is root
    assert root.get('/a/b') is b
    assert root.get('/a').b is b
    assert root.a.b is b
