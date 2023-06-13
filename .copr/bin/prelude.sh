#!/usr/bin/env bash

copr_home="$(dirname "$(dirname "$(realpath "${BASH_SOURCE[0]}")")")"

export topdir="${topdir:-$(rpmbuild --eval '%{_topdir}')}"
export sourcedir="${sourcedir:-$(rpmbuild --define "_topdir ${topdir}" --eval '%{_sourcedir}')}"
export sourcedir="${sourcedir:-$(rpmbuild --eval '%{_sourcedir}')}"
export downloaddir="${downloaddir:-$(pwd)/downloads}"
export PATH="${copr_home}/bin:${PATH}"

mkdir -p "${topdir}"
mkdir -p "${sourcedir}"
mkdir -p "${downloaddir}"
