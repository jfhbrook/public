#!/usr/bin/env bash

copr_home="$(dirname "$(dirname "$(realpath "${BASH_SOURCE[0]}")")")"

topdir="${topdir:-$(rpmbuild --eval '%{_topdir}')}"
sourcedir="${sourcedir:-$(rpmbuild --eval '%{_sourcedir}')}"

export topdir
export sourcedir

export downloaddir="${downloaddir:-$(pwd)/downloads}"
export PATH="${copr_home}/bin:${PATH}"

mkdir -p "${topdir}"
mkdir -p "${sourcedir}"
mkdir -p "${downloaddir}"

# Installs jq on the COPR build instance. This will fail locally, but you
# should have this installed anyway.
if ! which jq; then dnf install -y jq; fi
