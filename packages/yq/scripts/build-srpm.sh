#!/usr/bin/env bash

set -euxo pipefail

builddir="${builddir:-$(rpmbuild --eval '%{_topdir}')}"
sources="${sources:-${builddir}/SOURCES}"

# We're REALLY CLOSE. The issue is that the source tarball must be formatted
# in a specific way - that is, we need to stage the files somewhere, and then
# tarball that and move it to wherever we want our sources to be.

# I want the tool to do it, but I also want the staging directory to be
# configured from this script. So that looks like:
# - making the "staging" directory configurable, not the sources
# - configure an output directory, not a spec file
# - create a tmpdir for staging if one isn't specified

# Use the workspace we have on COPR, be debuggable locally
staging_dir="${staging_dir:-$(pwd)/staging}"

# This can be turned into a shippable tool, like rust2rpm or npm2rpm.
# shellcheck disable=SC2154
bash ./scripts/downloader.sh "${spec}.in" --staging-dir "${staging_dir}" --out "$(basedir "${spec}")"

# HOPEFULLY setting _srcrpmdir will get the output to go in the right directory!
# Otherwise I'll need to grep the name/version/arch out and move the file.
# shellcheck disable=SC2154
rpmbuild --define "_topdir ${builddir}" --define "_srcrpmdir ${outdir}" -bs "${spec}"
