#!/usr/bin/env bash


topdir="$(pwd)/target/"
sources="${topdir}SOURCES/"
srpms="${topdir}SRPMS/"
version="$(cat "${spec}"  | grep -E '^Version: ' | sed 's/^Version: //')"

mkdir -p "${sources}"

curl -L "https://github.com/mikefarh/yq/releases/download/v${version}/yq_linux_amd64.tar.gz" -o "${sources}/yq_linux_amd64.tar.gz"

rpmbuild --define "_topdir ${topdir}" -bs "${spec}"

mv "${srpms}"yq*.src.rpm "${outdir}"
rm -rf "${topdir}"
