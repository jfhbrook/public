#!/usr/bin/env bash

set -euxo pipefail

# NOTE: This script is generic and can be used for other similar builds.
# TODO: Can/should this get pushed into the Makefile?

scriptdir="${scriptdir:-$(pwd)/scripts}"
builddir="${builddir:-$(rpmbuild --eval '%{_topdir}')}"
name="$(cat "${spec}"  | grep -E '^Name: ' | sed 's/^Name: //')"
version="$(cat "${spec}"  | grep -E '^Version: ' | sed 's/^Version: //')"
buildarch="$(cat "${spec}" | grep -E '^BuildArch: ' | sed 's/^BuildArch: //')"
sources="src/${name}-${version}"

mkdir -p "${builddir}/SOURCES"
mkdir -p "${sources}"

if [ -f ./scripts/download-sources.sh ]; then
  (cd "${sources}" && name="${name}" \
    version="${version}" \
    buildarch="${buildarch}" \
    bash ${scriptdir}/download-sources.sh)
fi
  
(cd src && tar -czf "${builddir}/SOURCES/${name}-${version}-${buildarch}.tar.gz" .)

rpmbuild --define "_topdir ${builddir}" -bs "${spec}"

cp "${builddir}/SRPMS/${name}-${version}"*'.src.rpm' "${outdir}/"
