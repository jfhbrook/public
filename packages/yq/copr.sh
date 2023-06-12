#!/usr/bin/env bash


builddir="${builddir:-$(rpmbuild --eval '%{_topdir}')}/"
sources="${builddir}SOURCES/"
srpms="${builddir}SRPMS/"
version="$(cat "${spec}"  | grep -E '^Version: ' | sed 's/^Version: //')"

mkdir -p "${sources}"

curl -L "https://github.com/mikefarh/yq/releases/download/v${version}/yq_linux_amd64.tar.gz" -o "${sources}/yq_linux_amd64.tar.gz"

# rpmbuild --define "_topdir ${builddir}" -bs "${spec}"
rpmbuild --define "_topdir ${builddir}" -bs "${spec}"

mv "${srpms}"yq*.src.rpm "${outdir}"
