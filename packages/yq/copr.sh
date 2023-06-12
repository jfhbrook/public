#!/usr/bin/env bash

builddir="${builddir:-$(rpmbuild --eval '%{_topdir}')}/"
sources="${builddir}SOURCES/"
version="$(cat "${spec}"  | grep -E '^Version: ' | sed 's/^Version: //')"

rpmbuild -bs "${spec}"
