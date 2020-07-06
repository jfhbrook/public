import pytest

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


def test_complicated_set():
    root = Node()

    a = Node()
    b = Node()
    c = Node()
    d = Node()
    e = Node()
    e_prime = Node()
    f = Node()
    g = Node()
    h = Node()

    root.set("/a", a)
    root.set("/b", b)
    root.set("/c/", c)
    root.set("/a/d", d)
    root.set(["b", "e"], e)
    root.set("/b/f", f)
    root.set("/a/d/g", g)
    root.set("/b/e/h", h)
    root.set("/b/e", e_prime)

    assert root.a is a
    assert root.get("/a") is a
    assert root.b is b
    assert root.get("/b") is b
    assert root.c is c
    assert root.get("/c") is c
    assert root.a.d is d
    assert root.get("/a/d") is d
    assert root.b.e is e_prime
    assert root.get("/b/e") is e
    assert root.b.f is f
    assert root.get("/b/f") is f
    assert root.a.d.g is g
    assert root.get("/a/d/g") is g
    assert root.b.e.h is h
    assert root.get("/b/e/h") is h

    i = Node()
    l = Node()

    i.set("/j/k/l", l)
    root.set("/a/d/g/i", i)

    assert root.a.d.g.i.j.k.l is l
    assert root.get("/a/d/g/i/j/k/l") is l
