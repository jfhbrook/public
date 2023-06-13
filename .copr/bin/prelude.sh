#!/usr/bin/env bash

copr_home="$(dirname "$(dirname "$(readlink "${BASH_SOURCE[0]}")")")"

export builddir="${builddir:-$(rpmbuild --eval '%{_topdir}')}"
export sourcedir="${sourcedir:-$(rpmbuild --eval '%{_sourcedir}')}"
export downloaddir="${downloaddir:-$(pwd)/downloads}"
export PATH="${copr_home}/bin:${PATH}"

mkdir -p "${builddir}"
mkdir -p "${sourcedir}"
mkdir -p "${downloaddir}"
