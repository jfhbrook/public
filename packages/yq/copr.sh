#!/usr/bin/env bash


builddir="${builddir:-$(rpmbuild --eval '%{_topdir}')}/"
sources="${builddir}SOURCES/"
version="$(cat "${spec}"  | grep -E '^Version: ' | sed 's/^Version: //')"

mkdir -p "${sources}"

curl -L "https://github.com/mikefarh/yq/releases/download/v${version}/yq_linux_amd64.tar.gz" -o "${sources}/yq_linux_amd64.tar.gz"

rpmbuild -bs "${spec}"
