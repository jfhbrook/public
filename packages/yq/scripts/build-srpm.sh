#!/usr/bin/env bash

set -euxo pipefail

builddir="${builddir:-$(rpmbuild --eval '%{_topdir}')}"
sources="${builddir}/SOURCES"
srpms="${builddir}/SRPMS"
version="$(cat "${spec}"  | grep -E '^Version: ' | sed 's/^Version: //')"

mkdir -p "${sources}"

mkdir -p "src/yq-${version}"

# Note, even though this is a "source rpm", we're downloading pre-compiled
# binaries. That's OK - source vs binary has more to do with the rpm lifecycle
# than whether or not it's text. As long as we mark it as arch-specific in the
# spec, we'll be OK.
(cd "src/yq-${version}" && curl -L "https://github.com/mikefarah/yq/releases/download/v${version}/yq_linux_amd64.tar.gz" | tar -xz)

# rpmbuild expects sources to be in a tarball here
(cd src && tar -czf "${sources}/yq-${version}-x86_64.tar.gz" .)

# build the source rpm
rpmbuild --define "_topdir ${builddir}" -bs "${spec}"

# put the source rpm where copr can find it + do the binary rpms
cp "${srpms}/yq-${version}"*'.src.rpm' "${outdir}/"
